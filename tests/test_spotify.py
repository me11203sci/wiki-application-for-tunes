import pytest
from unittest.mock import patch, Mock
import requests

from waft.spotify import *
from waft.datatypes import *


"""
Tests for parse_tracks_from_json()
"""


def test_parse_tracks_from_json_SingleArtist():
    json_data = {
        "tracks": {
            "items": [
                {
                    "name": "Song A",
                    "id": "123",
                    "duration_ms": 100000,
                    "album": {"name": "Album A"},
                    "artists": [{"name": "Artist A"}],
                }
            ]
        }
    }

    result = parse_tracks_from_json(json_data)
    track = result[0]

    assert len(result) == 1
    assert track.title == "Song A"
    assert track.artist == "Artist A"
    assert track.album == "Album A"
    assert track.duration == 100000
    assert track.track_id == "123"


def test_parse_tracks_from_json_MultipleArtists():
    json_data = {
        "tracks": {
            "items": [
                {
                    "name": "Song A",
                    "id": "123",
                    "duration_ms": 100000,
                    "album": {"name": "Album A"},
                    "artists": [
                        {"name": "Artist A"},
                        {"name": "Artist B"},
                    ],
                }
            ]
        }
    }

    result = parse_tracks_from_json(json_data)
    track = result[0]

    assert track.artist == "Artist A and Others"


def test_parse_tracks_from_json_KeyError():
    with pytest.raises(KeyError):
        parse_tracks_from_json({})


def test_parse_tracks_from_json_TypeError():
    with pytest.raises(TypeError):
        parse_tracks_from_json([])


"""
Tests for spotify_search()
"""


@patch("waft.spotify.requests.get")
def test_spotify_search_Success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "tracks": {
            "items": [
                {
                    "name": "Song",
                    "id": "id1",
                    "duration_ms": 123,
                    "album": {"name": "Album"},
                    "artists": [{"name": "Artist"}],
                }
            ]
        }
    }

    mock_get.return_value = mock_response

    results = spotify_search("Song", "token123", limit=1)

    assert len(results) == 1
    assert isinstance(results[0], DisplayedTrack)


@patch("waft.spotify.requests.get")
def test_spotify_search_HttpError(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        spotify_search("Song", "token123", limit=1)


"""
Following two tests implement testing for ValueError, which is in the description for spotify_search(),
however it is not implemented in spotify_search()
"""


"""
def test_spotify_search_ValueErrorSong():
    with pytest.raises(ValueError):
        spotify_search("", "valid_token", limit=5)


def test_spotify_search_ValueErrorToken():
    with pytest.raises(ValueError):
        spotify_search("Doxy", "", limit=5)
        """


"""
Tests for parse_album_data()
"""


def test_parse_album_data_Success():
    json_data = {
        "album": {
            "name": "Album X",
            "images": [{"url": "http://image.url"}],
        }
    }

    album = parse_album_data(json_data)

    assert isinstance(album, Album)
    assert album.album_name == "Album X"
    assert album.image_url == "http://image.url"


def test_parse_album_data_KeyError():
    with pytest.raises(KeyError):
        parse_album_data({})


"""
Tests for parse_artists_data()
"""


def test_parse_artists_data_MultipleArtists():
    json_data = {
        "artists": [
            {"name": "Artist A"},
            {"name": "Artist B"},
        ]
    }

    artists = parse_artists_data(json_data)

    assert len(artists) == 2
    assert all(isinstance(a, Artist) for a in artists)
    assert artists[0].artist_name == "Artist A"


def test_parse_artists_data_KeyError():
    with pytest.raises(KeyError):
        parse_artists_data({})


"""
Tests for parse_track_data()
"""


def test_parse_track_data_success():
    json_data = {
        "duration_ms": 300000,
        "explicit": False,
        "name": "Track Name",
        "track_number": 5,
        "album": {"release_date": "2020-01-01"},
    }

    track = parse_track_data(json_data)

    assert isinstance(track, Track)
    assert track.name == "Track Name"
    assert track.duration_ms == 300000
    assert track.explicit is False
    assert track.release_date == "2020-01-01"
    assert track.track_number == 5


def test_parse_track_data_missing_key():
    with pytest.raises(KeyError):
        parse_track_data({})


"""
Tests for get_metadata()
"""


@patch("waft.spotify.requests.get")
def test_get_metadata_Success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "duration_ms": 100000,
        "explicit": True,
        "name": "Test Song",
        "track_number": 1,
        "album": {
            "name": "Test Album",
            "release_date": "2022-01-01",
            "images": [{"url": "http://img"}],
        },
        "artists": [{"name": "Artist A"}],
    }

    mock_get.return_value = mock_response

    metadata = get_metadata("track123", "token123")

    assert isinstance(metadata, FullMetadata)
    assert metadata.album.album_name == "Test Album"
    assert metadata.track.name == "Test Song"
    assert metadata.artists[0].artist_name == "Artist A"


def test_get_metadata_ValueErrorTrack():
    with pytest.raises(ValueError):
        get_metadata("", "token")


def test_get_metadata_ValueErrorToken():
    with pytest.raises(ValueError):
        get_metadata("track123", "")


@patch("waft.spotify.requests.get")
def test_get_metadata_HttpError(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        get_metadata("track123", "token123")


@patch("waft.spotify.requests.get")
def test_get_metadata_request_RequestException(mock_get):
    mock_get.side_effect = requests.RequestException("Connection error")

    with pytest.raises(requests.RequestException):
        get_metadata("track123", "token123")
