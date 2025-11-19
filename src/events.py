from enum import Enum, auto
from credentialStorage import KeyStorage

######################################################
# Name: Event
# Purpose: Enum to hold all possible event types
# Notes: These are outputs of the update function
######################################################
class Event(Enum):
    INVALID_MESSAGE = auto()
    AUTHENTICATE_SPOTIFY = auto()
    AUTHENTICATE_YOUTUBE = auto()
    AUTHENTICATION_FAILED = auto()
    STORE_KEYS = auto()

######################################################
# Name: handleEvents
# Description: Event handler that will handle events 
#       that have been returned when updating the model
# Input: Event of type enum Event
# Output: N/A
# Notes: Events could be handled a different way, so
#       this is subject to change. Each section of the
#       switch case statement should contain different
#       API calls and other services.
######################################################
def handleEvents(evnt: Event):
    match evnt:
        case Event.INVALID_MESSAGE:

        case Event.AUTHENTICATE_SPOTIFY:

        case Event.AUTHENTICATE_YOUTUBE:

        case Event.AUTHENTICATION_FAILED:

        case Event.STORE_KEYS:

