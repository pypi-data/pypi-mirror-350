from typing import Dict
from unittest import IsolatedAsyncioTestCase, mock

from easybits_module_interface.models import Message, MessageTypes


class BaseModuleTestCase(IsolatedAsyncioTestCase):
    """
    Base class for module tests.

    Inherit from this class to perform tests onto your module's callback method.

    Example:
        Suppose you've developed a module that echos the users input.
        The following snippet will test two cases

        #. success: An incoming message is provided, we echo the user input
        #. failure: No incoming message is provided, we respond with a default error message

            >>> class EchoModuleTestCase(BaseModuleTestCase):
            ...     def setUp(self):
            ...         super().setUp()
            ...         self.instance = EchoModule()
            ...
            ...     async def test_success(self):
            ...         await self.perform_test({'message': {'incoming': 'hello world!'}}, 'hello world')
            ...
            ...     async def test_failure(self):
            ...         await self.perform_test({'message': {'incoming': ''}}, 'Something went wrong.')
    """
    def setUp(self):
        super().setUp()

        pika_mock = mock.patch('easybits_module_interface._internal.aoi_pika', mock.AsyncMock(), create=True)
        self.addCleanup(pika_mock.stop)
        self.pika_mock = pika_mock.start()

        pub_entity_mock = mock.Mock(return_value=mock.Mock(publish=mock.AsyncMock()))
        pub_mock = mock.patch('easybits_module_interface._internal.Publisher', pub_entity_mock)
        self.addCleanup(pub_mock.stop)
        self.pub_mock = pub_mock.start()

    @property
    def default_message(self) -> Dict:
        """
        Property of default message dictionary.

        Hint:
            You can override this property to provide a custom default message.

        :returns: default message dictionary
        """
        return {
            "meta": {
                "type": MessageTypes.INCOMING_MESSAGE.value,
                "botId": 1,
                "event": None,
                "messageId": None,
                "controller": None,
                "internalUserId": 1,
                "communicationChannelId": 1
            },
            "config": None,
            "message": None,
            "context": None,
        }

    def _build_message(self, message: Dict, message_type: MessageTypes = MessageTypes.INCOMING_MESSAGE) -> Dict:
        """
        Extends default content to a given message.

        :param message: Message dictionary
        :returns: extended message containing default ``meta`` data
        """
        default_message = self.default_message.copy()
        default_message['meta']['type'] = message_type.value
        if 'meta' in message:
            default_message['meta'].update(message.pop('meta'))
        if 'config' in message and default_message['config'] is not None:
            default_message['config'].update(message.pop('config'))
        if 'message' in message and default_message['message'] is not None:
            default_message['message'].update(message.pop('message'))
        if 'context' in message and default_message['context'] is not None:
            default_message['context'].update(message.pop('context'))

        default_message.update(message)
        return default_message

    async def perform_test(self, message: Dict, expected_message_content: str) -> None:
        """
        Helper method to perform a test on the ``callback`` method of a module implementation.

        :param message: a message dictionary containing the required atttributes
        :param expected_message_content: The expected content of ``message.outgoing``
        :returns: None
        """
        assert self.instance is not None, 'You must assign a module to self.instance.'
        await self.instance.callback(Message.from_dict(**self._build_message(message)))

        self.pub_mock.return_value.publish.assert_called_once()
        self.assertEqual(
            self.pub_mock.return_value.publish.call_args_list[0][0][0].message.outgoing,
            expected_message_content
        )

    async def perform_responded_test(self):
        """Test case to test whether a module processes relevant messages."""
        assert self.instance is not None, 'You must assign a module to self.instance.'
        message = self._build_message({'message': {'incoming': 'Hi!'}})
        await self.instance.callback(Message.from_dict(**self._build_message(message)))

        # at least 1 call to publish
        self.assertGreaterEqual(self.pub_mock.return_value.publish.call_count, 1)

    async def perform_ignored_test(self):
        """Test case to test whether a module ignores irrelevant messages."""
        assert self.instance is not None, 'You must assign a module to self.instance.'
        message = self._build_message({}, MessageTypes.OUTGOING_MESSAGE)
        await self.instance.callback(Message.from_dict(**self._build_message(message)))

        self.pub_mock.return_value.publish.assert_not_called()

    async def test_compatibility(self):
        """Test to validate compatibility of module implementation."""
        if self.__class__ is BaseModuleTestCase:
            self.skipTest('Not required for base class.')
        self.pub_mock.return_value.publish.reset_mock()
        await self.perform_ignored_test()
        self.pub_mock.return_value.publish.reset_mock()
        await self.perform_responded_test()
