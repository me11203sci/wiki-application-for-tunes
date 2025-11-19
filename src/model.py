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
        state = AppState.UNAUTHENTICATED,
        spotifyAuthenticated = False,
        youtubeAuthenticated = False
    )