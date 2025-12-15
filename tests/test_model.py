"""
Unit tests for the functions in src/waft/model.py
"""

import pytest
from pathlib import Path
from textual.message import Message

from waft.model import ApplicationModel, update
from waft.messages import UpdateStatus, Authenticating, SearchRequest, UrlSelected
from waft.datatypes import DisplayedTrack, YoutubeResult

"""
Helper function to create base model of ApplicationModel to test against
"""


def make_base_model() -> ApplicationModel:
    return ApplicationModel(
        active_token="token",
        api_key="api",
        authenticating=False,
        developer_key="dev",
        downloads_folder=Path("/tmp"),
        search_query=("", ""),
        search_results=[],
        selection=None,
        suggestion_results=[],
        status_message="",
        valid_credentials=False,
    )


"""
Tests for update()
"""


def test_update_UpdateStatus():
    model = make_base_model()
    message = UpdateStatus(text="Testing...")

    new_model = update(model, message)

    assert isinstance(new_model, ApplicationModel)
    assert new_model.status_message == "Testing..."
    assert model.status_message == ""
    assert new_model is not model


def test_update_Authenticating():
    model = make_base_model()
    message = Authenticating(state=True)

    new_model = update(model, message)

    assert isinstance(new_model, ApplicationModel)
    assert new_model.authenticating is True
    assert model.authenticating is False
    assert new_model is not model


def test_update_SearchRequest():
    model = make_base_model()
    message = SearchRequest(query="Test", mode="spotify")

    new_model = update(model, message)

    assert isinstance(new_model, ApplicationModel)
    assert new_model.search_query == ("Test", "spotify")
    assert model.search_query == ("", "")
    assert new_model is not model


def test_update_Other():
    model = make_base_model()
    message = UrlSelected(index=0)

    new_model = update(model, message)

    assert isinstance(new_model, ApplicationModel)
    assert new_model is model
