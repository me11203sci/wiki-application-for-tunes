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

    CONTINUE_TO_PROMPT = auto()

    DATABASE_QUERY_SENT = auto()
    DATABASE_QUERY_FAILED = auto()
    DATABASE_QUERY_SUCCEEDED = auto()
    DATABASE_QUERY_RETRY = auto()

    SPOTIFY_SEARCH_STARTED = auto()
    SPOTIFY_SEARCH_FAILED = auto()
    SPOTIFY_SEARCH_SUCCEEDED = auto()
    SPOTIFY_SEARCH_RETRY = auto()

    YOUTUBE_SEARCH_STARTED = auto()
    YOUTUBE_SEARCH_FAILED = auto()
    YOUTUBE_SEARCH_SUCCEEDED = auto()
    YOUTUBE_SEARCH_RETRY = auto()

    DATABASE_SUBMIT_SENT = auto()
    DATABASE_SUBMIT_FAILED = auto()
    DATABASE_SUBMIT_SUCCEEDED = auto()

    FILE_DOWNLOAD_STARTED = auto()
    FILE_DOWNLOAD_FAILED = auto()
    FILE_DOWNLOAD_SUCCEEDED = auto()
