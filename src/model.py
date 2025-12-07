from dataclasses import dataclass
from enum import Enum, auto


######################################################
# Name: AppState
# Purpose: Enum to hold all possible model states
# Notes: N/A
######################################################
class AppState(Enum):
    UNAUTHENTICATED = auto()
    AUTHENTICATING = auto()
    AUTHENTICATED = auto()
    PROMPT_FOR_SEARCH = auto()
    SEARCHING_DATABASE = auto()
    DATABASE_FAILED = auto()
    DATABASE_SUCCEEDED = auto()
    SEARCHING_SPOTIFY = auto()
    SPOTIFY_FAILED = auto()
    SPOTIFY_SUCCEEDED = auto()
    SEARCHING_YOUTUBE = auto()
    YOUTUBE_FAILED = auto()
    YOUTUBE_SUCCEEDED = auto()
    SUBMITTING_TO_DATABASE = auto()
    PROMPT_DOWNLOAD = auto()


######################################################
# Name: Model
# Purpose: Dataclass to hold current application state
# Notes: N/A
######################################################
@dataclass
class Model:
    state: AppState
    spotifyAuthenticated: bool
    youtubeAuthenticated: bool


######################################################
# Name: initialModel
# Description: Creates the model object
# Input: N/A
# Output: N/A
# Notes: To be called when initializing the application
######################################################
def initialModel() -> Model:
    return Model(
        state=AppState.UNAUTHENTICATED,
        spotifyAuthenticated=False,
        youtubeAuthenticated=False,
    )
