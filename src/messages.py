"""Message definitions for the `waft` application's T.E.A. event flow.

This module defines custom Textual message subclasses used to communicate
state changes to the application's update loop.

Messages
--------
Authenticating
    Indicates that an authentication workflow has started or ended.
UpdateStatus
    Carries text for updating the application's status display.
"""

from textual.message import Message


class Authenticating(Message):
    """Message indicating a change to the authentication workflow state.

    This message is emitted when the application begins or ends an
    authentication sequence. Used to disable ::Input:: fields and thwart
    duplicate successive authentication requests.
    """

    def __init__(self, state: bool) -> None:
        """
        Construct an authentication message.

        Parameters
        ----------
        state : bool
            Whether authentication is currently active.
        """

        super().__init__()
        self.state = state


class UpdateStatus(Message):
    """Message containing updated status text for the application.

    This message is dispatched when a screen or widget needs to update the
    text displayed in the global status bar. It carries the new message
    content, leaving rendering and model updates to the application controller.
    """

    def __init__(self, text: str) -> None:
        """Construct a status-update message.

        Parameters
        ----------
        text : str
            The status text to present to the user.
        """

        super().__init__()
        self.text = text


class ValidCredentials(Message):
    """TODO."""

    def __init__(self) -> None:  # pylint: disable=useless-parent-delegation
        """TODO."""
        super().__init__()
