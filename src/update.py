from typing import Tuple

from model import Model, AppState
from messages import Message
from events import Event


######################################################
# Name: update
# Description: Updates the application model based on messages
# Input: One message and the application model object
# Output: Updated model object and list of events
# Notes: This function will change the model state, and
#       some model values and will return the new model
#       object, along with a events to process
######################################################
def update(msg: Message, model: Model):
    events: list[Event] = []

    match model.state:
        case AppState.UNAUTHENTICATED:
            if msg == Message.START_AUTHENTICATION:
                events.append(Event.AUTHENTICATE_SPOTIFY)
                events.append(Event.AUTHENTICATE_YOUTUBE)

                model.state = AppState.AUTHENTICATING
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.AUTHENTICATING:
            if msg == Message.AUTHENTICATION_SUCCEEDED:
                events.append(Event.STORE_KEYS)

                model.state = AppState.AUTHENTICATED
                model.spotifyAuthenticated = True
                model.youtubeAuthenticated = True
            elif msg == Message.AUTHENTICATION_FAILED:
                events.append(Event.AUTHENTICATION_FAILED)

                model.state = AppState.UNAUTHENTICATED
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.AUTHENTICATED:
            if msg == Message.CONTINUE_TO_PROMPT:
                events

                model.state = AppState.PROMPT_FOR_SEARCH
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.PROMPT_FOR_SEARCH:
            if msg == Message.DATABASE_QUERY_SENT:
                events

                model.state = AppState.SEARCHING_DATABASE
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.SEARCHING_DATABASE:
            if msg == Message.DATABASE_QUERY_SUCCEEDED:
                events

                model.state = AppState.DATABASE_SUCCEEDED
            elif msg == Message.DATABASE_QUERY_FAILED:
                events

                model.state = AppState.DATABASE_FAILED
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.DATABASE_SUCCEEDED:
            if msg == Message.SPOTIFY_SEARCH_STARTED:
                events

                model.state = AppState.SEARCHING_SPOTIFY
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.DATABASE_FAILED:
            if msg == Message.DATABASE_QUERY_RETRY:
                events

                model.state = AppState.PROMPT_FOR_SEARCH
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.SEARCHING_SPOTIFY:
            if msg == Message.SPOTIFY_SEARCH_SUCCEEDED:
                events

                model.state = AppState.SPOTIFY_SUCCEEDED
            elif msg == Message.SPOTIFY_SEARCH_FAILED:
                events

                model.state = AppState.SPOTIFY_FAILED
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.SPOTIFY_SUCCEEDED:
            if msg == Message.YOUTUBE_SEARCH_STARTED:
                events

                model.state = AppState.SEARCHING_YOUTUBE
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.SPOTIFY_FAILED:
            if msg == Message.SPOTIFY_SEARCH_RETRY:
                events

                model.state = AppState.SEARCHING_SPOTIFY
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.SEARCHING_YOUTUBE:
            if msg == Message.YOUTUBE_SEARCH_SUCCEEDED:
                events

                model.state = AppState.YOUTUBE_SUCCEEDED
            elif msg == Message.YOUTUBE_SEARCH_FAILED:
                events

                model.state = AppState.YOUTUBE_FAILED
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.YOUTUBE_SUCCEEDED:
            if msg == Message.DATABASE_SUBMIT_SENT:
                events

                model.state = AppState.SUBMITTING_TO_DATABASE
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.YOUTUBE_FAILED:
            if msg == Message.YOUTUBE_SEARCH_RETRY:
                events

                model.state = AppState.SEARCHING_YOUTUBE
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.SUBMITTING_TO_DATABASE:
            if msg == Message.DATABASE_SUBMIT_SUCCEEDED:
                events

                model.state = AppState.PROMPT_DOWNLOAD
            else:
                events.append(Event.INVALID_MESSAGE)

        case AppState.PROMPT_DOWNLOAD:
            if msg == Message.FILE_DOWNLOAD_STARTED:
                events

                model.state = AppState.PROMPT_FOR_SEARCH
            else:
                events.append(Event.INVALID_MESSAGE)

    return model, events
