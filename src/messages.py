from textual.message import Message

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
