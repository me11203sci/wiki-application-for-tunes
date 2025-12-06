from textual.app import App

from model import ApplicationModel, update
from widgets import StatusBar
from messages import Authenticating, UpdateStatus
from screens import IntitialAuthenticationScreen

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
