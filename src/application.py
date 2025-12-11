"""Core application module for the `waft` Textual interface.

This module defines the top-level :class:`Application` class, which manages
The Elm Architecture model and coordinates user interface updates in
response to Textual events.
"""

from dataclasses import replace
from typing import Optional, Tuple

from textual.app import App
from textual.css.query import NoMatches

from authentication import get_spotify_access_token
from keyring import retrieve_credentials
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
        """Initialize the model state with default values on startup."""
        super().__init__()

        self.model: ApplicationModel = ApplicationModel(
            active_token="",
            authenticating=False,
            status_message="...",
            valid_credentials=False,
        )

    async def on_mount(self) -> None:
        """Initialize application state and load the initial screen.

        This method is called once when the Textual application finishes
        mounting. It initializes the T.E.A. model.
        """

        credential_result: Optional[Tuple[str, str, str]] = retrieve_credentials()

        authentication_result: Optional[str] = None
        token: str = ""

        if credential_result is not None:
            authentication_result = self.run_worker(
                get_spotify_access_token(credential_result[0], credential_result[1]),
                exclusive=True,
            ).result

            token = authentication_result if authentication_result else token

        self.model = replace(
            self.model,
            active_token=token,
            valid_credentials=(authentication_result is not None),
        )

        if self.model.valid_credentials:
            self.push_screen(SpotifySearchScreen())
        else:
            self.push_screen(IntitialAuthenticationScreen())

        self.app.post_message(UpdateStatus("Welcome."))

    async def on_update_status(self, message: UpdateStatus) -> None:
        """Handle a status-message update event.

        Used to re-render the ``StatusBar`` widget.

        Parameters
        ----------
        message : UpdateStatus
            The TEA message containing the new status text.

        Notes
        -----
        - Make sure that screen contains ``StatusBar``, otherwise this function will
          do nothing
        """

        self.model = update(self.model, message)

        try:
            status_widget: StatusBar = self.screen.query_one(StatusBar)
            status_widget.render_from_model(self.model)
        except NoMatches:
            pass

    async def on_authenticating(self, message: Authenticating) -> None:
        """Handle authentication-state updates.

        Updates state model to reflect whether a authentication request
        has been submitted, disabling parts of the user interface and
        rebuffing duplicate requests if so.
        """

        self.model = update(self.model, message)

        if isinstance(self.screen, IntitialAuthenticationScreen):
            self.screen.render_from_model(self.model)

    async def on_valid_credentials(self) -> None:
        """Transition to Spotify A.P.I. search screen after successful validation."""

        self.pop_screen()
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
