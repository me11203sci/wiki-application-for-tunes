""" """

from typing import List

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Input

from model import ApplicationModel
from messages import Authenticating, UpdateStatus
from widgets import Logo, StatusBar


class IntitialAuthenticationScreen(Screen):
    """"""

    BINDING_GROUP_TITLE: str | None = "Initial Authentication Screen"
    BINDINGS: List[Binding] = [
        Binding(key="<c-q>", action="app.quit", description="Quit the application"),
        Binding(key="<tab>", action="app.focus_next", description="Focus next"),
        Binding(
            key="<enter>",
            action="app.submit_authentication",
            description="Submit authentication requests",
        ),
    ]

    def render_from_model(self, model: ApplicationModel) -> None:
        """"""

        self.query_one("#client_id_box", Input).disabled = model.authenticating
        self.query_one("#client_secret_box", Input).disabled = model.authenticating
        self.query_one("#youtube_key_box", Input).disabled = model.authenticating

    async def on_input_submitted(self) -> None:
        """TODO."""

        if self.app.model.authenticating:
            return

        # Poll input values.
        client_id: str = self.query_one("#client_id_box", Input).value
        client_secret: str = self.query_one("#client_secret_box", Input).value
        api_key: str = self.query_one("#youtube_key_box", Input).value

        # .
        if not (client_id and client_secret and api_key):
            self.app.post_message(UpdateStatus("Please provide valid credentials."))
            return

        # .
        self.app.post_message(Authenticating(True))

        self.app.post_message(UpdateStatus("Submitting authentication requests..."))

        # await

    def compose(self) -> ComposeResult:
        """"""

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
