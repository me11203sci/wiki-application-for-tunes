"""User interface screens for the `waft` application.

This module defines the interactive screens used throughout the `waft`
application. Each screen is responsible for rendering widgets, collecting
user input, and emitting TEA messages that drive global state updates in
the application.
"""

from asyncio import gather
from typing import Optional, Tuple

# from textual.widgets.option_list import Option
from rich.columns import Columns
from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Input, OptionList, Select, Static

from authentication import get_spotify_access_token
from keyring import store_credentials
from messages import Authenticating, UpdateStatus, ValidCredentials
from model import ApplicationModel
from widgets import Logo, StatusBar

# from rich.table import Table
# from rich.progress_bar import ProgressBar
# from rich.padding import Padding


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
        # NOTE: TODO add youtube api key authentication.
        result: Tuple[Optional[str]] = await gather(
            get_spotify_access_token(client_id, client_secret)
        )

        self.app.post_message(Authenticating(False))

        if result[0] is None:
            self.app.post_message(UpdateStatus("Invalid credentials."))
            return

        store_credentials(client_id, client_secret, api_key)
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

        client_id_box = Input(
            classes="credentials_input", id="client_id_box", placeholder="Client ID"
        )
        client_secret_box = Input(
            classes="credentials_input",
            id="client_secret_box",
            placeholder="Client Secret",
            password=True,
        )
        youtube_key_box = Input(
            classes="credentials_input",
            id="youtube_key_box",
            placeholder="YouTube API Key",
        )

        client_id_box.border_title = "Client ID"
        client_secret_box.border_title = "Client Secret"
        youtube_key_box.border_title = "YouTube API Key"

        status_bar = StatusBar()

        yield Horizontal(
            Vertical(
                Logo(id="logo"),
                client_id_box,
                client_secret_box,
                youtube_key_box,
                classes="initial_screen_alignment",
            ),
            classes="initial_screen_alignment",
        )
        yield status_bar
        yield Footer(show_command_palette=False)


class SpotifySearchScreen(Screen):
    """Screen for the Spotify A.P.I. search view.

    This screen presents a minimal user interface for entering or initiating search
    queries against the Spotify A.P.I.
    """

    BINDING_GROUP_TITLE: str | None = "Spotify A.P.I. Search Screen"
    BINDINGS = [
        Binding(key="<c-q>", action="app.quit", description="Quit the application"),
    ]

    def compose(self) -> ComposeResult:
        """Construct and yield the widgets that make up the screen layout.

        Yields
        ------
        ComposeResult
            An iterable container of Textual widgets, including the
            credential input fields, the application logo, the status
            bar, and the footer.
        """

        search_bar: Horizontal = Horizontal(
            Input(placeholder="Search", id="search_input"),
            Button("", id="search_button"),
            id="search_bar",
        )
        header_text: Columns = Columns(
            [
                Text("Title", justify="left"),
                Text("Album", justify="left"),
                Text("Duration", justify="right"),
            ],
            expand=True,
            equal=False,
        )
        search_results: Vertical = Vertical(
            Static(header_text),
            OptionList(id="search_results"),
            id="search_results_view",
        )
        downloads: OptionList = OptionList(id="downloads_view")
        search_mode: Select = Select(
            ((mode, mode) for mode in ["Track"]),  # NOTE: Add Album search in future.
            allow_blank=False,
            compact=True,
            id="search_mode",
        )

        search_bar.border_title = "[1] ─ Search"
        search_results.border_title = "[2] ─ Search Results"
        downloads.border_title = "[3] ─ Progress"

        status_bar: StatusBar = StatusBar()

        yield Container(
            Horizontal(
                Vertical(
                    Horizontal(search_bar, search_mode, id="search_header"),
                    search_results,
                ),
                downloads,
            )
        )
        yield status_bar
        yield Footer(show_command_palette=False)

    # def on_mount(self):
    #     b = Table.grid(
    #         expand=True,
    #     )
    #     # NOTE: Changing the ratios is a guess and check, so have fun changing it...
    # b.add_column(
    #     "Title", justify="left", ratio=90, no_wrap=True, overflow="ellipsis"
    # )
    # b.add_column(
    #     "Album", justify="left", ratio=160, no_wrap=True, overflow="ellipsis"
    # )
    # b.add_column(
    #     "Duration", justify="right", ratio=50, no_wrap=True, overflow="ellipsis"
    # )
    # b.add_row(
    #     "[b]505[/b]", "Favourite Worst Nightmare (Standard Version)", "4:13"
    # )
    # b.add_row("Arctic Monkeys")
    # a: OptionList = self.query_one("#search_results", OptionList)
    # a.add_option(b)
    #
    # d = Table.grid(expand=True)
    # e: ProgressBar = ProgressBar(total=one,)
    # d.add_column(
    #     "Metadata", justify="left", ratio=50, no_wrap=True, overflow="ellipsis"
    # )
    # d.add_column("Progress", justify="center", ratio=50, no_wrap=True)
    # d.add_row("[b]505[/b]")
    # d.add_row("Arctic Monkeys", Padding(e, (0, 2)))
    # d.add_row("Favourite Worst Nightmare (Standard Version)")
    # c: OptionList = self.query_one("#downloads_view", OptionList)
    # c.add_option(d)


class AudioSource(ModalScreen):
    """Modal dialog for selecting or entering an audio source U.R.L.

    This screen is used to collect a YouTube source U.R.L. or allow the user to choose
    from a list of suggested matches.
    """

    BINDING_GROUP_TITLE: str | None = "Audio Source Selection Screen"
    BINDINGS = [
        Binding(key="<c-q>", action="app.quit", description="Quit the application"),
        Binding(
            key="esc",
            action="app.cancel_source_select",
            description="Quit the application",
        ),
    ]

    def compose(self) -> ComposeResult:
        """Construct and yield the widgets that make up the screen layout.

        Yields
        ------
        ComposeResult
            An iterable container of Textual widgets, including the U.R.L. input field
            and a list of suggestion options.
        """
        url_field: Input = Input(id="url_field")
        source_suggestions: OptionList = OptionList()
        url_field.border_title = "Provide YouTube URL:"
        source_suggestions.border_title = "Suggestions (press <tab> to focus)"

        yield Horizontal(Vertical(url_field, source_suggestions))
