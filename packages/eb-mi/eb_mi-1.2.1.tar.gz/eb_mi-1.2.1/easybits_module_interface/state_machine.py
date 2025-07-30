import logging
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union

logger = logging.getLogger()


@dataclass
class Transition:
    """Data class to store information about a transition.

    """
    #: The original state of the transition
    from_state: str
    #: The target state of the transition.
    to_state: str
    #: Validator for incoming message, returns True if message is valid, else False
    validator: Union[bool, Callable[[Any], bool]]
    #: Callback to call in case the transition is successful
    success: Optional[Callable[[Any], None]] = None
    #: Callback to call in case the transition is unsuccessful
    failure: Optional[Callable[[Any], None]] = None


@dataclass
class TransitionResult:
    """Data class representation of a transition result."""
    #: The side-effect action that can be triggered for this resulting transition
    action: Optional[Callable[[Any], None]]
    #: The resulting state of a transition
    state: Optional[str]

    def __call__(self, *args, **kwargs):
        if self.action is not None:
            return self.action(*args, **kwargs)


class IllegalTransitionError(Exception):
    """Exception class to signalize adding an illegal transition to a state machine"""


class StateMachine:
    """Implementation of directed graph for state machine.

    Example:
        >>> machine = StateMachine()
        >>> transition = Transition(
        ...     from_state='A',
        ...     to_state='B',
        ...     validator=lambda x: 'foo' in x,
        ...     success=lambda: 0,
        ...     failure=lambda: -1
        ... )
        >>> machine.define_transition(transition)
        >>> res = machine.make_transition('A', 'my message foo')
        >>> assert res.state == 'B'
        >>> assert res.action() == 0
    """
    def __init__(self):
        self._transitions: List[Transition] = []

    def _validate_transition(self, transition: Transition) -> None:
        """Validation method to add a new transition into the state machine.

        :param transition: The transition to add to the state machine
        :raises IllegalTransitionError: in case there is already a transition for
                                        the provided states registered.
        """
        for existing_transition in self._transitions:
            is_illegal_transition = (
                existing_transition.from_state == transition.from_state
                and existing_transition.to_state == transition.to_state
            )
            if is_illegal_transition:
                raise IllegalTransitionError(
                    f'There is already a transition existing with'
                    f'from_state={transition.from_state} and '
                    f'to_state={transition.to_state}'
                )

    def define_transition(self, transition: Transition) -> None:
        """Method to register transitions between states.

        :param transition: The transition to add
        """
        self._validate_transition(transition)
        self._transitions.append(transition)

    def make_transition(self, current_state: str, payload: str) -> Optional[TransitionResult]:
        """Method to perform transitions

        :param current_state: the current state inside the state machine.
        :param payload: The payload to validate the transition on.
        :returns: A :py:obj:`~.TransitionResult` if a transition is available else None/
        """
        transition = list(filter(lambda x: x.from_state == current_state, self._transitions))
        if not transition:
            logger.error(f"No transition defined from {current_state}")
            return

        transition = transition[0]
        is_success = transition.validator

        if callable(transition.validator):
            is_success = transition.validator(payload)

        if is_success:
            return TransitionResult(action=transition.success, state=transition.to_state)
        return TransitionResult(action=transition.failure, state=None)
