import asyncio
import json
import logging
import logging.config
from dataclasses import asdict
from typing import Callable, Optional

import aio_pika
from aio_pika import Message as PikaMessage
from aio_pika.abc import AbstractIncomingMessage

from easybits_module_interface.models import Message


class ConnectionError(Exception):
    """
    Exception raised when connection to RabbitMQ fails.
    """
    pass


class ConnectionSetup:
    """
    Base class for classes that need to connect to RabbitMQ.

    Provides a :py:obj:`~connection` and :py:obj:`~channel` attribute.

    :param connection: Connection to RabbitMQ

    Example::
        >>> import aio_pika
        >>> connection = await aio_pika.connect("amqp://localhost/", loop=loop)
        >>> setup = ConnectionSetup(connection)
        >>> await setup.connect()
        >>> await setup.channel.declare_queue("test")
        >>> await setup.disconnect()

    """
    def __init__(self, connection):
        self.connection = connection
        self.channel = None
        self.logger = logging.getLogger(__name__)

    def set_logger(self, logger) -> None:
        """
        Set logger for class.

        :param logger: Logger to be used
        :return: None
        """
        self.logger = logger

    async def connect(self, channel_id: Optional[int] = None) -> None:
        """
        Establish a connection (channel) to RabbitMQ.

        :param channel_id: Channel id to use
        :return: None
        :raises ConnectionError: If connection not established
        """
        if self.connection is None or self.connection.is_closed:
            raise ConnectionError("Connection not established")
        self.channel = await self.connection.channel(channel_id)

    async def disconnect(self) -> None:
        """
        Disconnect from RabbitMQ.

        :return: None
        """
        if self.channel is not None and not self.channel.is_closed:
            await self.channel.close()


class Publisher(ConnectionSetup):
    """
    Class to publish messages to RabbitMQ.

    Note: When `exchange != ""` the publisher will declare the exchange if it does not exist.

    :param connection: Connection to RabbitMQ
    :param exchange: Name of exchange to publish messages to

    Example::
        >>> import aio_pika
        >>> from easybits_module_interface import Publisher
        >>> from easybits_module_interface.models import Message
        >>> connection = await aio_pika.connect("amqp://localhost/", loop=loop)
        >>> publisher = Publisher(connection, "test_exchange")
        >>> await publisher.publish(Message.from_dict(**message_dict))
        >>> await publisher.disconnect()
    """
    def __init__(self, connection, exchange):
        super().__init__(connection)
        self.exchange_name = exchange
        self.default_exchange = None

    async def connect(self):
        """
        Establish a connection to RabbitMQ.

        :return: None
        """
        await super().connect()
        if self.exchange_name == "":
            self.logger.warning("No exchange name provided, using default exchange")
            self.default_exchange = self.channel.default_exchange
            return
        # ensure default exchange exists
        self.default_exchange = await self.channel.declare_exchange(
            self.exchange_name, aio_pika.ExchangeType.FANOUT, durable=True
        )

    async def publish(self, message: Message, exchange: Optional[str] = None, queue: str = ""):
        """
        Publish a message to RabbitMQ.

        Internally, establishes a connection via a new channel, and publishes the message to the desired target.
        Converts :py:obj:`~message` to a dictionary, then to a JSON string and finally to a byte string.
        If :py:obj:`~exchange` is empty, the message will be published to the Publisher's default exchange.

        **Note**: <u>Please do not publish messages to the default exchange & default queue,
                  always provide a queue or exchange name.</u>

        Values for :py:obj:`~exchange`:
            - None: Use the default exchange of the module
            - "": Use the RMQ default exchange
            - "exchange_name": Use the exchange with the given name

        :param message: Message to be published
        :param exchange: Name of exchange to publish message to
        :param queue: Name of queue to publish message to
        :return: None
        """
        if self.channel is None or self.channel.is_closed:
            await self.connect()

        if exchange is None:
            ex = self.default_exchange
        elif exchange == "":
            ex = self.channel.default_exchange
        else:
            ex = await self.channel.get_exchange(exchange)

        msg_body = json.dumps(asdict(message)).encode('utf-8')
        pika_msg = PikaMessage(body=msg_body)
        await ex.publish(
            pika_msg,
            routing_key=queue
        )


class Consumer(ConnectionSetup):
    """
    Class to consume messages from RabbitMQ.

    :param connection: Connection to RabbitMQ

    Example::
        >>> import aio_pika
        >>> from easybits_module_interface import Consumer
        >>> from easybits_module_interface.models import Message
        >>> connection = await aio_pika.connect("amqp://localhost/", loop=loop)
        >>> consumer = Consumer(connection)
        >>> consumer.add_callback("test_queue", callback)
        >>> await consumer.run()
        >>> await consumer.disconnect()
    """
    def __init__(self, connection):
        super().__init__(connection)
        self.queue = None
        self.callback_map = {}

    @staticmethod
    def __callback_wrapper(fun):
        """
        Wraps input :py:obj:`~fun` (callbacks) so that signature matches :py:obj:`~pika`s consumption call.
        Internally builds :py:obj:`~models.Message` from incoming message body, and passes it to :py:obj:`~fun`.

        This way the callback can use Message class to interact with the message instead of handling a dictionary.

        :param fun: Function to be decorated
        :return: wrapped :py:obj:`~fun`
        """
        async def inner(msg: AbstractIncomingMessage):
            message = Message.from_dict(**json.loads(msg.body.decode('utf-8')))
            await fun(message)
            await msg.ack()

        return inner

    def add_callback(self, queue: str, callback: Callable[[Message], None], exchange: str = None, is_durable: bool = True):
        """
        Add a callback to be called when a message is received on :py:obj:`~queue`.

        :param queue: Name of queue to consume messages from
        :param callback: Callback function
        :param exchange: Name of exchange to bind queue to
        :param is_durable: Whether to create a durable queue or not
        """
        self.callback_map[queue] = (self.__callback_wrapper(callback), exchange, is_durable)

    async def run(self):
        """
        Run the consumer.

        This will start the consumer, i.e. register configured callbacks under the
        desired queues.
        In case the startup process fails, the consumer will be closed
        and the occurred exception will be raised.

        **Note:** Register callbacks using :py:obj:`~add_callback` before calling this method.
        """
        try:
            await self.connect()
            await self.channel.set_qos(prefetch_count=1)
            for queue_name, (callback, exchange_name, is_durable) in self.callback_map.items():
                queue = await self.channel.declare_queue(queue_name, durable=is_durable)
                if exchange_name is not None:
                    exchange = await self.channel.declare_exchange(
                        exchange_name, aio_pika.ExchangeType.FANOUT, durable=True
                    )
                    await queue.bind(exchange, queue_name)
                await queue.consume(callback, no_ack=False)

            self.logger.info("LISTENING TO {}".format(' '.join(self.callback_map.keys())))
            await asyncio.Future()
        except Exception as e:
            self.logger.exception("Exception in consumer")
            raise e
        finally:
            await self.disconnect()


class ModuleInterface:
    """
    Base class for module implementations.

    :param connection: Connection to RabbitMQ
    :param exchange: Name of exchange to publish messages to
    :param default_consumer_queue: Name of queue to consume messages from

    Example::
        >>> import aio_pika
        >>> import asyncio
        >>> from easybits_module_interface import ModuleInterface
        >>> from easybits_module_interface.models import Message
        >>> class MyModule(ModuleInterface):
        ...     async def callback(self, message: Message):
        ...         print(message)
        >>> connection = await aio_pika.connect("amqp://localhost/", loop=loop)
        >>> module = MyModule(connection, "test_exchange", "test_queue")
        >>> await module.run()
        >>> try:
        >>>     await asyncio.Future()
        >>> finally:
        >>>     await module.shutdown()

        Or as a system_message only module:
        >>> class MyModule(ModuleInterface):
        ...     def __init__(self, connection):
        ...         super().__init__(connection, "", None)
        ...         self.add_callback("system_messages_my_module", self.callback)
        ...
        ...     async def callback(self, message: Message):
        ...         print(message)
        ...
        >>> connection = await aio_pika.connect("amqp://localhost/", loop=loop)
        >>> module = MyModule(connection)
    """
    def __init__(
            self, connection, exchange: Optional[str] = None,
            default_consumer_queue: Optional[str] = None
    ) -> None:
        #: Provide placeholder for logger
        self.logger = None

        #: default connection to message broker
        self.__connection = connection

        #: consumer entity to consume incoming messages
        self.__consumer = Consumer(self.__connection)

        if default_consumer_queue is not None:
            #: add default callback for default queue
            self.__consumer.add_callback(default_consumer_queue, self.callback)

        #: publisher entity to publish outgoing messages
        self.__publisher = Publisher(self.__connection, exchange)

        #: initializing the default logger
        self.init_logger('module_interface')

    def __new__(cls, *args, **kwargs):
        # guard against instantiating the base class
        if cls is ModuleInterface:
            raise TypeError(
                f"only children of '{cls.__name__}' may be instantiated"
            )
        return super().__new__(cls)

    def init_logger(self, name: str) -> None:
        """
        Initialize logger for module implementation.

        :param name: Name of logger
        :return: None
        """
        name = f'{name.lower()}.interface'

        self.logger = logging.getLogger(name)
        self.__consumer.set_logger(self.logger)
        self.__publisher.set_logger(self.logger)

    def add_callback(self, queue: str, callback, exchange=None, is_durable=True) -> None:
        """
        Add a callback to be called when a message is received on :py:obj:`~queue`.

        :param queue: Name of queue to consume messages from
        :param callback: Callback function
        :param exchange: Name of exchange to bind queue to
        :param is_durable: Whether to create a durable queue or not
        :return: None
        """
        self.__consumer.add_callback(queue, callback, exchange, is_durable)

    async def run(self) -> None:
        """
        Run the module.

        This will start the consumer and wait for it to finish.
        """
        await self.__publisher.connect()
        await self.__consumer.run()

    async def shutdown(self) -> None:
        """
        Shutdown the module.
        """
        await self.__consumer.disconnect()
        await self.__publisher.disconnect()
        await self.__connection.close()
        self.logger.info("Shutting down")

    async def publish(self, message: Message, exchange: str = None, queue: str = "") -> None:
        """
        Publish a message to RabbitMQ.

        If :py:obj:`~exchange` is empty, the message will be published to the Publisher's default exchange.
        If :py:obj:`~queue` is empty, the message will be published to the RMQ default queue.

        :param message: Message to be published
        :param exchange: Name of exchange to publish message to
        :param queue: Name of queue to publish message to
        :return: None
        """
        await self.__publisher.publish(message, exchange, queue)

    async def callback(self, message: Message) -> None:
        """
        Callback function to be implemented by module implementations.

        :param message: Message received from consumer queue
        :return: None
        """
        raise NotImplementedError("Callback not implemented")


async def boostrap_module_class(module_implementation, **config) -> None:
    """
    Main entry point for module implementations, aka application loop.

    :param module_implementation: ModuleInterface implementation (as class)
    :param config: Configuration dictionary
    :return: None

    ================  =============  =============
    Key               Type           Description
    ================  =============  =============
    logger            dict           Logger configuration
    logger.level      str            Logger level
    logger.path       str            Path to logger configuration file
    logger.name       str            Name of logger
    ================= =============  =============
    broker            dict           Broker configuration
    broker.uri        str            Broker uri
    """
    logger_config = config.get('logger', None)
    broker_config = config.get('broker', None)

    assert 'uri' in broker_config, 'broker uri required!'

    logger_name = None
    if logger_config is not None:
        logging.basicConfig()
        if 'level' in logger_config:
            logging.getLogger().setLevel(logger_config['level'])

        if 'path' in logger_config:
            # set up logger from file
            logging.config.fileConfig(logger_config['path'])

        # create logger
        logger_name = logger_config.get('name', 'module_interface')
        _ = logging.getLogger(name=logger_name)

    connection = await aio_pika.connect_robust(broker_config['uri'])
    module = module_implementation(connection)
    module.init_logger(logger_name)
    return module


async def main(module_implementation, **config) -> None:
    """
    Main entry point for module implementations, aka application loop.

    :param module_implementation: ModuleInterface implementation (as class)
    :param config: Configuration dictionary
    :return: None

    ================  =============  =============
    Key               Type           Description
    ================  =============  =============
    logger            dict           Logger configuration
    logger.level      str            Logger level
    logger.path       str            Path to logger configuration file
    logger.name       str            Name of logger
    ================= =============  =============
    broker            dict           Broker configuration
    broker.uri        str            Broker uri
    """
    module = await boostrap_module_class(module_implementation, **config)
    try:
        await module.run()
    except Exception as e:
        module.logger.error(e)
    finally:
        module.logger.info("MAIN Shutting down")
        await module.shutdown()
