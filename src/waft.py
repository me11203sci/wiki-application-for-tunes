"""Execution entry point for the `waft` application.

Todo.
"""

from dataclasses import dataclass, replace
from typing import List

from textual.message import Message
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Input, Static


@dataclass(frozen=True)
class ApplicationModel:
    """A struct-like representation of the state of the application."""

    authenticating: bool
    status_message: str


class Authenticating(Message):
    """TODO."""

    def __init__(self, state: bool) -> None:
        """TODO."""

        super().__init__()
        self.state = state


class UpdateStatus(Message):
    """TODO."""

    def __init__(self, text: str) -> None:
        """TODO."""

        super().__init__()
        self.text = text


def update(model: ApplicationModel, message: Message) -> ApplicationModel:
    """TODO."""

    match message:
        case UpdateStatus(text=text):
            return replace(model, status_message=text)
        case Authenticating(state=state):
            return replace(model, authenticating=state)
        case _:
            return model


class Logo(Static):
    """TODO."""

    def on_mount(self) -> None:
        """"""

        with open("splashtext.txt", "r") as file:
            self.content = file.read()


class StatusBar(Static):
    """TODO."""

    def on_mount(self):
        """"""

        self.border_title = "Status"
        self.can_focus = False


    def render_from_model(self, model: ApplicationModel) -> None:
        """"""

        self.update(model.status_message)


class IntitialAuthenticationScreen(Screen):
    """TODO."""

    BINDING_GROUP_TITLE: str | None = "Initial Authentication Screen"
    BINDINGS: List[Binding] = [
        Binding(key="<c-q>", action="app.quit", description="Quit the application"),
        Binding(key="<tab>", action="app.focus_next", description="Focus next"), # TODO
        Binding(key="<enter>", action="app.submit_authentication", description="Submit authentication requests"), # TODO
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
        if not(client_id and client_secret and api_key):
            self.app.post_message(UpdateStatus("Please provide valid credentials."))
            return

        # .
        self.app.post_message(Authenticating(True))

        self.app.post_message(UpdateStatus("Submitting authentication requests..."))
        print(f"{client_id}, {client_secret}, {api_key}")

        # await 


    def compose(self) -> ComposeResult:
        """"""

        client_id_box = Input(id="client_id_box", placeholder="Client ID")
        client_secret_box = Input(id="client_secret_box", placeholder="Client Secret", password=True)
        youtube_key_box = Input(id="youtube_key_box", placeholder="YouTube API Key")

        client_id_box.border_title = "Client ID"
        client_secret_box.border_title = "Client Secret"
        youtube_key_box.border_title = "YouTube API Key"

        status_bar = StatusBar()

        yield Horizontal(
            Vertical(
                Logo(id="logo"),
                client_id_box,
                client_secret_box,
                youtube_key_box
            )
        )
        yield status_bar
        yield Footer(show_command_palette=False)


class Application(App):
    """Manages/Updates the application state based on Textual events."""

    ALLOW_SELECT = False
    CSS_PATH = "../styles/main.tcss"


    def on_mount(self) -> None:
        """"""

        self.model = ApplicationModel(
            authenticating=False,
            status_message="Welcome!",
        )
        self.push_screen(IntitialAuthenticationScreen())

        status_widget = self.screen.query_one(StatusBar)
        status_widget.render_from_model(self.model)


    async def on_update_status(self, message: UpdateStatus) -> None:
        """"""

        self.model = update(self.model, message)
        status_widget = self.screen.query_one(StatusBar)
        status_widget.render_from_model(self.model)


    async def on_authenticating(self, message: Authenticating) -> None:
        """"""

        self.model = update(self.model, message)
        self.screen.render_from_model(self.model)


    async def action_submit_authentication(self) -> None:
        """"""

        await self.screen.on_input_submitted()


if __name__ == "__main__":
    application: App = Application()
    application.run()
