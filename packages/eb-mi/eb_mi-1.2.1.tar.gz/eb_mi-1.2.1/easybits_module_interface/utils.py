import logging
from typing import Dict, Union

from easybits_module_interface.models import Message, MessageTypes

logger = logging.getLogger()


def with_error_response(error_message: Union[str, Dict], exception_type) -> Message:
    """
    Decorator to handle exceptions and return an error message.

    :param error_message: The error message to return.
    :type error_message: str | Dict
    :param exception_type: The exception type to catch.
    :type exception_type: Exception
    :return: The error message.


    Example:
        >>> from easybits_module_interface.utils import with_error_response
        >>> from easybits_module_interface.models import Message
        >>> @with_error_response('An error occurred: {error}', Exception)
        >>> def process_message(message: Message) -> Message:
        ...     raise Exception('Something went wrong')
        >>> message = Message()
        >>> message.message.incoming = 'Hello'
        >>> message.meta.language = 'en'
        >>> message = process_message(message)
        >>> message.message.outgoing
        'An error occurred: Something went wrong'
    """
    def decorator(func):
        def wrapper(message: Message, *args, **kwargs) -> Message:
            """
            Wrapper function to handle exceptions and return an error message.

            :param message: The original message object.
            :param args: The arguments.
            :param kwargs: The keyword arguments.
            :return: The error message.
            """
            try:
                return func(message, *args, **kwargs)
            except exception_type as ex:
                logger.error(f'Error while processing message: {ex}')
                em = error_message
                if isinstance(em, dict):
                    em = em.get(message.meta.language, 'en')
                message.message.outgoing = em.replace('{error}', str(ex))
                message.meta.type = MessageTypes.OUTGOING_MESSAGE.value
                return message
        return wrapper
    return decorator


def with_error_response_cls(error_message: Union[str, Dict], exception_type) -> Message:
    """
    Decorator to handle exceptions and return an error message.

    **Note:** This decorator is used for class methods.

    :param error_message: The error message to return.
    :type error_message: str | Dict
    :param exception_type: The exception type to catch.
    :type exception_type: Exception
    :return: The error message.


    Example:
        >>> from easybits_module_interface.utils import with_error_response_cls
        >>> from easybits_module_interface.models import Message
        >>> class MyClass:
        ...     @with_error_response_cls('An error occurred: {error}', Exception)
        ...     def process_message(self, message: Message) -> Message:
        ...         raise Exception('Something went wrong')
        >>> message = Message()
        >>> message.message.incoming = 'Hello'
        >>> message.meta.language = 'en'
        >>> message = MyClass().process_message(message)
        >>> message.message.outgoing
        'An error occurred: Something went wrong'
    """
    def decorator(func):
        def wrapper(self, message: Message, *args, **kwargs) -> Message:
            """
            Wrapper function to handle exceptions and return an error message.

            :param self: The class instance.
            :param message: The original message object.
            :param args: The arguments.
            :param kwargs: The keyword arguments.
            :return: The error message.
            """
            try:
                return func(self, message, *args, **kwargs)
            except exception_type as ex:
                logger.error(f'Error while processing message: {ex}')
                em = error_message
                if isinstance(em, dict):
                    em = em.get(message.meta.language, 'en')
                message.message.outgoing = em.replace('{error}', str(ex))
                message.meta.type = MessageTypes.OUTGOING_MESSAGE.value
                return message
        return wrapper
    return decorator
