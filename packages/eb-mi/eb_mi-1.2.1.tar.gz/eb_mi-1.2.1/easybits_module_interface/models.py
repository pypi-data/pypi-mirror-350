from copy import deepcopy
from dataclasses import dataclass, field, fields, make_dataclass
from enum import Enum
from typing import Dict, List, Optional, Union


class BaseDataClass:
    """
    Base class for dataclasses with a from_dict method.
    """
    @classmethod
    def get_model_kwargs(cls, kwargs: Dict) -> Dict:
        """
        Getter for kwargs based on the fields of the class.

        :param kwargs: kwargs to filter
        :return: filtered kwargs
        """
        field_names = [field.name for field in fields(cls)]
        kwargs_out = deepcopy(kwargs)
        for f in kwargs.keys():
            if f not in field_names:
                kwargs_out.pop(f, None)
        return kwargs_out

    @classmethod
    def from_dict(cls, **kwargs):
        """
        Safe method to create an instance from given kwargs.

        :param kwargs: object as kwargs
        :return: instance of the class
        """
        return cls(**cls.get_model_kwargs(kwargs))


class DynamicFieldsDataClass(BaseDataClass):
    """
    Base class for dataclasses with dynamic fields.

    Example:
        >>> @dataclass
        ... class MyFoo(DynamicFieldsDataClass):
        ...     foo: str
        ...
        >>> obj = MyFoo.from_dict(foo='string', bar=1)
        >>> obj.foo
        'string'
        >>> obj.bar
        1
        >>> asdict(obj)
        {'foo': 'string', 'bar': 1}
        >>> MyFoo(foo='string', bar=1)
        AttributeError: 'MyFoo' object has no attribute 'bar'
    """
    @classmethod
    def from_dict(cls, **kwargs):
        """
        Creates a new dataclass with the fields provided in the kwargs.

        New fields are added to the class definition as Optional[str].

        :param kwargs: object as kwargs
        :return: new dataclass instance
        """
        field_names = [field.name for field in fields(cls)]
        new_fields = [(k, Optional[str], None) for k, v in kwargs.items() if k not in field_names]
        dynamic_cls = make_dataclass(cls.__name__, new_fields, bases=(cls,))
        return dynamic_cls(**kwargs)


class MessageTypes(Enum):
    SYSTEM_MESSAGE_PARSER = 'system_message_parser'
    SYSTEM_MESSAGE_CONTROLLER = 'system_message_controller'
    SYSTEM_MESSAGE_DATASINK = 'system_message_datasink'
    INCOMING_MESSAGE = 'incoming_message'
    OUTGOING_MESSAGE = 'outgoing_message'
    OUTGOING_MESSAGE_IMAGE = 'outgoing_message_image'
    OUTGOING_MESSAGE_AUDIO = 'outgoing_message_audio'


class SystemMessageEvents(Enum):
    CONFIGURE_MODULE = 'configure_module'
    SAVE = 'save'
    DELETE = 'delete'
    CONFIGURE_PROXY_MODE = 'configure_proxy_mode'
    # deprecated, kept for backward compatibility
    UPDATE_COLLECTION = 'update_collection'
    UPDATE_COLLECTION_DATA = 'update_collection_data'


@dataclass
class MessageMeta(DynamicFieldsDataClass):
    """
    Meta data for messages.

    This class is dynamic, meaning using the from_dict method
    will create a new dataclass with the fields provided in the kwargs.

    This is useful to add more meta data to the message without
    changing the class definition.
    """
    #: type of message
    type: MessageTypes
    #: event type of message
    event: Optional[str] = None
    #: internal ID of communication channel
    communicationChannelId: Optional[str] = None
    #: type identifier of the controller used for communication
    controller: Optional[str] = None
    #: ID of the user can be used for tracking/state management
    internalUserId: Optional[str] = None
    #: ID of the bot used for communication
    botId: Optional[str] = None

    #: [Optional] configured language of bot used inside modules to generate responses
    language: Optional[str] = None
    #: [Optional] internal tracking ID of the message
    messageId: Optional[str] = None


@dataclass
class UserMessage(BaseDataClass):
    """
    Object to describe message content aka a UserMessage
    """
    #: content of incoming message
    incoming: Optional[str] = None
    #: content of incoming file
    incoming_file: Optional[str] = None
    #: content of outgoing message
    outgoing: Optional[str] = None


@dataclass
class ContextProvider(BaseDataClass):
    """
    Configuration for a context provider
    """
    #: name of resulting key in context
    key: str = ""
    #: name of the context provider to use
    provider_name: str = ""


@dataclass
class AvailableModule(BaseDataClass):
    """
    Module config template
    """
    #: Internal ID
    id: int
    #: verbose identifier of module
    name: str
    #: description of module
    description: str
    #: indicates that the module supports reengagement
    supports_reengagement: bool = False
    #: Layout of configuration values
    configuration_layout: Optional[Dict] = None
    #: List of supported context providers by the module
    supported_context_providers: Optional[List] = None
    #: Indicates if the module is allowed to be used
    #:   without any pre-selection process
    is_passive: bool = False
    # The following attributes are commented out, as they
    # are only used in the client applications.
    #: Indicates if the module is available to be used
    #is_published: bool = True
    #: Indicates if the module is visible for users
    #is_visible: bool = True
    #: Indicates if the module is the default module
    #    that is used during the default module prediction
    #    phase of the parser.
    is_default: bool = False
    #: String of comma separated intentions that the module supports
    intentions: Optional[str] = None


@dataclass
class BotModule(BaseDataClass):
    """
    Configuration for a bot specific module.
    """
    #: internal identifier of bot module
    id: int
    #: instance of :py:obj:`~.AvailableModule`
    module: AvailableModule = None
    #: indicates that the module is active
    is_active: bool = False
    #: indicates that the module uses reengagement
    has_reengagement: bool = False
    #: list of instances of :py:obj:`~.ContextProvider` \
    #  that are used to extract context from incoming messages
    context_providers: List[ContextProvider] = field(default_factory=list)
    #: configuration values for the module
    configuration_values: Dict = field(default_factory=dict)
    #: configuration values for the parser
    parser_configuration: Dict = field(default_factory=dict)
    #: desired reengagement message
    reengagement_message: str = None
    #: Timeout in minutes for reengagement message
    reengagement_timeout_minutes: int = None

    @property
    def name(self):
        return self.module.name

    @property
    def intentions(self):
        return self.module.intentions

    @classmethod
    def from_dict(cls, **kwargs):
        """
        Creates an instance from given kwargs

        :param kwargs: object as kwargs
        :return: :py:obj:`~.BotModule` instance
        """
        module = kwargs.pop('module', None)
        context_providers = kwargs.pop('context_providers', [])

        return super().from_dict(
            **kwargs,
            module=AvailableModule.from_dict(**module) if module else None,
            context_providers=[ContextProvider.from_dict(**c) for c in context_providers]
        )


@dataclass
class ConfigureModuleContext(BaseDataClass):
    """
    Integration config template
    """
    id: str = None
    #: name of the integration
    name: str = None
    #: list of instances of :py:obj:`~.ContextProvider`
    context_providers: List[ContextProvider] = field(default_factory=list)
    #: indicates that the integration is ready to consume messages
    is_active: bool = False
    #: indicates that the integration supports reengagement
    re_engagement: bool = False

    #: layout of configuration values
    configuration_layout: Optional[Dict] = None
    #: indicates that the module supports reengagement
    supports_reengagement: bool = False
    #: description of module
    description: str = None


@dataclass
class Message(BaseDataClass):
    #: message meta data
    meta: MessageMeta
    #: extracted context from incoming message
    context: Optional[Union[Dict, ConfigureModuleContext]] = None
    #: message content
    message: Optional[UserMessage] = None
    #: configuration values forwarded to the module
    config: Optional[Dict] = None

    @classmethod
    def from_dict(cls, **kwargs):
        """
        Creates an instance from given kwargs

        :param kwargs: object as kwargs
        :return: :py:obj:`~.Message` instance
        """
        meta_data = kwargs.pop('meta', None)
        if meta_data is not None:
            meta_data = MessageMeta.from_dict(**meta_data)
        message = kwargs.pop('message', None)
        if message is not None:
            message = UserMessage.from_dict(**message)

        context = kwargs.pop('context', None)
        is_configure_module_message = (
            meta_data
            and meta_data.type == MessageTypes.SYSTEM_MESSAGE_PARSER.value
            and meta_data.event in [
                SystemMessageEvents.SAVE.value,
                SystemMessageEvents.DELETE.value,
            ]
        )
        if is_configure_module_message:
            context = AvailableModule.from_dict(**context)

        config = kwargs.pop('config', None)

        return super().from_dict(
            context=context,
            meta=meta_data,
            message=message,
            config=config,
        )
