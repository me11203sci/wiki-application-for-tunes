""""""
from dataclasses import dataclass, replace

from textual.message import Message

from messages import Authenticating, UpdateStatus


@dataclass(frozen=True)
class ApplicationModel:
    """A struct-like representation of the state of the application."""

    authenticating: bool
    status_message: str


def update(model: ApplicationModel, message: Message) -> ApplicationModel:
    """TODO."""

    match message:
        case UpdateStatus(text=text):
            return replace(model, status_message=text)
        case Authenticating(state=state):
            return replace(model, authenticating=state)
        case _:
            return model
