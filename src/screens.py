"""User interface screens for the `waft` application.

This module defines the interactive screens used throughout the `waft`
application. Each screen is responsible for rendering widgets, collecting
user input, and emitting TEA messages that drive global state updates in
the application.
"""

from asyncio import gather
from typing import Tuple

from requests.models import HTTPError
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Input, Static

from authentication import get_spotify_access_token
from messages import Authenticating, UpdateStatus, ValidCredentials
from model import ApplicationModel
from widgets import Logo, StatusBar


class IntitialAuthenticationScreen(Screen):
    """Screen for collecting initial authentication credentials.

    This screen presents three input fields—client ID, client secret,
    and a YouTube API key—along with keyboard bindings and a status bar.
    """

    BINDING_GROUP_TITLE: str | None = "Initial Authentication Screen"
    BINDINGS = [
        Binding(key="<c-q>", action="app.quit", description="Quit the application"),
        Binding(key="<tab>", action="app.focus_next", description="Focus next"),
        Binding(
            key="<enter>",
            action="app.submit_authentication",
            description="Submit authentication requests",
        ),
    ]

    def render_from_model(self, model: ApplicationModel) -> None:
        """Update widget states based on the current TEA model.

        Parameters
        ----------
        model : ApplicationModel
            The global application state used to determine which inputs
            should be enabled or disabled.
        """

        self.query_one("#client_id_box", Input).disabled = model.authenticating
        self.query_one("#client_secret_box", Input).disabled = model.authenticating
        self.query_one("#youtube_key_box", Input).disabled = model.authenticating

    async def on_input_submitted(self) -> None:
        """Fire when a user hits <enter>/<c-m> or clicks the button in the ::Footer::.

        Notes
        -----
        Authentication itself is performed outside this screen; the
        screen only gathers inputs and dispatches messages.
        """

        # I only used the `mypy` ignore because all solutions I could think of
        # created cyclical imports.
        if self.app.model.authenticating:  # type: ignore[attr-defined]
            return

        # Poll input values.
        client_id: str = self.query_one("#client_id_box", Input).value
        client_secret: str = self.query_one("#client_secret_box", Input).value
        api_key: str = self.query_one("#youtube_key_box", Input).value

        # Check that all credentials are provided, prompt user otherwise.
        if not (client_id and client_secret and api_key):
            self.app.post_message(UpdateStatus("Please provide valid credentials."))
            return

        # Disable input fields and block new requests.
        self.app.post_message(Authenticating(True))

        self.app.post_message(UpdateStatus("Submitting authentication requests..."))

        # Authentication logic (do so asynchronously).
        try:
            result: Tuple[str] = await gather(
                get_spotify_access_token(client_id, client_secret)
            )
            print(result)
        except HTTPError as exception:
            print(exception)
            self.app.post_message(UpdateStatus("Invalid credentials."))

        self.app.post_message(Authenticating(False))
        self.app.post_message(ValidCredentials())
        self.app.post_message(UpdateStatus("Success."))

    def compose(self) -> ComposeResult:
        """Construct and yield the widgets that make up the screen layout.

        Yields
        ------
        ComposeResult
            An iterable container of Textual widgets, including the
            credential input fields, the application logo, the status
            bar, and the footer.
        """

        client_id_box = Input(id="client_id_box", placeholder="Client ID")
        client_secret_box = Input(
            id="client_secret_box", placeholder="Client Secret", password=True
        )
        youtube_key_box = Input(id="youtube_key_box", placeholder="YouTube API Key")

        client_id_box.border_title = "Client ID"
        client_secret_box.border_title = "Client Secret"
        youtube_key_box.border_title = "YouTube API Key"

        status_bar = StatusBar()

        yield Horizontal(
            Vertical(Logo(id="logo"), client_id_box, client_secret_box, youtube_key_box)
        )
        yield status_bar
        yield Footer(show_command_palette=False)


class SpotifySearchScreen(Screen):
    """Screen for the Spotify A.P.I. search view.

    This screen presents a minimal user interface for entering or initiating search
    queries against the Spotify A.P.I.
    """

    BINDING_GROUP_TITLE: str | None = "Spotify A.P.I. Search Screen"

    def compose(self) -> ComposeResult:
        """Construct and yield the widgets that make up the screen layout.

        Yields
        ------
        ComposeResult
            An iterable container of Textual widgets, including the
            credential input fields, the application logo, the status
            bar, and the footer.
        """

        status_bar = StatusBar()
        yield Static("Hi :D")
        yield status_bar
        yield Footer(show_command_palette=False)
