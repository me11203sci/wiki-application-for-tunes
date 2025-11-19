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
    events: Event[] = []

    if (model.state == AppState.UNAUTHENTICATED):
        if (msg == Message.START_AUTHENTICATION):
            events.append(Event.AUTHENTICATE_SPOTIFY)
            events.append(Event.AUTHENTICATE_YOUTUBE)

            model.state = AppState.AUTHENTICATING
        else:
            events.append(Event.INVALID_MESSAGE)

    elif (model.state == AppState.AUTHENTICATING):
        if (msg == Message.AUTHENTICATION_SUCCEEDED):
            events.append(Event.STORE_KEYS)

            model.state = AppState.AUTHENTICATED
            model.spotifyAuthenticated = True
            model.youtubeAuthenticated = True
        elif (msg == Message.AUTHENTICATION_FAILED):
            events.append(Event.AUTHENTICATION_FAILED)

            model.state = AppState.UNAUTHENTICATED
        else:
            events.append(Event.INVALID_MESSAGE)

    return model, events