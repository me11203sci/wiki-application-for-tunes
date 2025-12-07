from enum import Enum, auto


######################################################
# Name: Message
# Purpose: Enum to hold all possible messages
# Notes: These are inputs to the update function
######################################################
class Message(Enum):
    START_AUTHENTICATION = auto()
    AUTHENTICATION_SUCCEEDED = auto()
    AUTHENTICATION_FAILED = auto()
