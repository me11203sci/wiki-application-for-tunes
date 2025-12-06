""""""
from textual.widgets import Static

from model import ApplicationModel


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
