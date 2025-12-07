"""Core application module for the `waft` Textual interface.

This module defines the top-level :class:`Application` class, which manages
The Elm Architecture model and coordinates user interface updates in
response to Textual events.
"""

from textual.app import App

from messages import Authenticating, UpdateStatus
from model import ApplicationModel, update
from screens import IntitialAuthenticationScreen, SpotifySearchScreen
from widgets import StatusBar


class Application(App):
    """Manages/Updates the application state based on Textual events.

    All ::Messages:: have corresponding handlers as member functions of this
    class, as it loops.
    """

    ALLOW_SELECT = False
    CSS_PATH = "../styles/main.tcss"

    def __init__(self) -> None:
        """TODO."""
        super().__init__()
        self.model: ApplicationModel = ApplicationModel(
            authenticating=False,
            status_message="Welcome!",
        )

    def on_mount(self) -> None:
        """Initialize application state and load the initial screen.

        This method is called once when the Textual application finishes
        mounting. It initializes the T.E.A. model.
        """

        self.push_screen(IntitialAuthenticationScreen())

        status_widget = self.screen.query_one(StatusBar)
        status_widget.render_from_model(self.model)

    async def on_update_status(self, message: UpdateStatus) -> None:
        """Handle a status-message update event.

        Used to re-render the ``StatusBar`` widget.

        Parameters
        ----------
        message : UpdateStatus
            The TEA message containing the new status text.
        """

        self.model = update(self.model, message)
        status_widget: StatusBar = self.screen.query_one(StatusBar)
        status_widget.render_from_model(self.model)

    async def on_authenticating(self, message: Authenticating) -> None:
        """Handle authentication-state updates.

        Upates state model to reflect whether a authentication request
        has been submitted, disabling parts of the user interface and
        rebuffing duplicate requests if so.
        """

        self.model = update(self.model, message)

        if isinstance(self.screen, IntitialAuthenticationScreen):
            self.screen.render_from_model(self.model)

    async def on_valid_credentials(self) -> None:
        """TODO."""
        self.push_screen(SpotifySearchScreen())

    async def action_submit_authentication(self) -> None:
        """Trigger authentication submission workflow.

        Invoked either by key bindings or by footer button that
        map to the ``submit_authentication`` action.
        """

        # Calls the same internal function as the footer binding defined
        # in the screen.
        if isinstance(self.screen, IntitialAuthenticationScreen):
            await self.screen.on_input_submitted()
