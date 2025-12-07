"""Custom Textual widgets used throughout the `waft` application.

This module defines user interface components.
"""

from textual.widgets import Static

from model import ApplicationModel


class Logo(Static):
    """Widget for displaying the WAFT application logo or splash text."""

    def on_mount(self) -> None:
        """Load and display the logo text.

        Reads the contents of ``splashtext.txt`` from the working
        directory and stores it in ``self.content`` for rendering.
        """

        with open("splashtext.txt", "r", encoding="utf-8") as file:
            self.content = file.read()


class StatusBar(Static):
    """
    Widget for displaying the global status message.

    The status bar reflects the ``status_message`` field of the
    application model and is updated via calls to
    :meth:`render_from_model`.
    """

    def on_mount(self):
        """Initialize static widget properties.

        The widget is styled with a ``Status`` border title and is marked
        as non-focusable to prevent accidental input capture during text
        navigation.
        """

        self.border_title = "Status"
        self.can_focus = False

    def render_from_model(self, model: ApplicationModel) -> None:
        """Update the displayed status text using the application model.

        Parameters
        ----------
        model : ApplicationModel
            The current T.E.A. model providing the status message to display.
        """

        self.update(model.status_message)
