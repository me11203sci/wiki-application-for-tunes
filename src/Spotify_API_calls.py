from typing import Dict, List, Any
import requests
from requests.models import Response
from dataclasses import dataclass

@dataclass
class Album:
    """
    Album container.

    Represents basic album information returned from Spotify.

    Attributes
    ----------
    album_name : str
        The name of the album.
    image_url : str
        URL linking to the album cover image on Spotify.
    """
    album_name: str
    image_url: str
    def __init__(self, album_name, image_url):
        self.album_name = album_name
        self.album_url = image_url

@dataclass
class Artist:
    artist_name: str
    def __init__(self, artist_name):
        self.artist_name = artist_name
@dataclass
class Track:
    duration_ms: int
    explicit: bool
    name: str
    release_date: str
    track_number: int
    def __init__(self, duration_ms, explicit, name, release_date, track_number):
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.name = name
        self.release_date = release_date
        self.track_number = track_number

@dataclass
class Full_Metadata:
    album: Album
    artists: List[Artist]
    track: Track
    def __init__(self, album, artists, track):
        self.album = album
        self.artists = artists
        self.track = track

@dataclass
class Displayed_Track:
    """
    Container for displaying simplified Spotify track metadata.

    This dataclass stores a compact, user-facing representation of a Spotify track,
    including its title, primary artist, album name, duration, and track ID. It is
    primarily used after parsing search results or metadata responses to prepare
    structured data for UI display when a user selects their desired track.

    Attributes
    ----------
    title : str
        The track title as shown on Spotify.
    artist : str
        The primary artist's name. May include "and Others" if multiple artists
        contributed to the track.
    album : str
        The album name from which the track originates.
    duration : str
        The track's duration, typically expressed in milliseconds.
    track_id : str
        The unique Spotify track identifier.
    """
    title: str
    artist: str
    album: str
    duration: str
    track_id: str
    def __init__(self, title, artist, album, duration, track_id):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.track_id = track_id


def Parse_Tracks_From_Json(json_object: Dict[str, Any]) -> List[Displayed_Track]:
    """
    Parse Spotify search JSON results into a list of `Displayed_Track` objects.

    This function extracts relevant track metadata from a Spotify `/v1/search` API 
    response and converts each track entry into a `Displayed_Track` instance.  
    It pulls the track name, primary artist (appending "and Others" when multiple 
    artists are present), album name, duration in milliseconds, and track ID.

    Parameters
    ----------
    json_object : Dict[str, Any]
        Raw JSON returned from Spotify's Search API, expected to contain 
        `json_object["tracks"]["items"]`, where each item is a track object.

    Returns
    -------
    List[Displayed_Track]
        A list of parsed `Displayed_Track` objects in the order they appear 
        in the search results.

    Raises
    ------
    KeyError
        If the expected fields (`tracks`, `items`, or nested metadata fields)
        are missing from the input JSON.
    TypeError
        If the structure of the JSON object is not as expected or `json_object`
        is not a dictionary.

    Examples
    --------
    >>> response = Spotify_Search("Free Bird", bearer)
    >>> tracks = Parse_Tracks_From_Json(response)
    >>> print(tracks[0].track_name)
    "Free Bird"
    >>> track_metadata = Get_Metadata(tracks[0].track_id, bearer)
    """
    tracks_list: List[Dict[str, Any]] = json_object["tracks"]["items"]
    ordered_data_list: List[tuple[str, str, str, str]] = []
    for track_object in tracks_list:
        album: Dict[str, Any] = track_object["album"]
        album_name: str = album["name"]
        duration_ms: int = track_object["duration_ms"]
        track_name: str = track_object["name"]
        artists_list: List[Dict[str, Any]] = track_object["artists"]
        main_artist = artists_list[0]
        artist_name = main_artist["name"]
        track_id: str = track_object["id"]
        if len(artists_list) > 1:
            artist_name = artist_name + ' and Others'
        ordered_data_tuple: Displayed_Track = Displayed_Track(
            track_name, artist_name, album_name, duration_ms, track_id)
        ordered_data_list.append(ordered_data_tuple)
    
    return ordered_data_list



def Spotify_Search(query: str, bearer: str, limit: int) -> List[Displayed_Track]:
    """
    Perform a robust Spotify Search API request for tracks using a query string.
    
    This function queries the Spotify Web API's `/v1/search` endpoint with a user-
    provided search query and returns raw JSON search results. It includes defensive
    input validation, HTTP error handling, and network exception handling to improve
    reliability.

    Parameters
    ----------
    query : str
        The track name (e.g., "Let it Be").
    bearer : str
        A valid OAuth Bearer token for the Spotify Web API.

    Returns
    -------
    Dict[str, Any]
        Raw JSON search results returned by the Spotify API.

    Raises
    ------
    ValueError
        If `query` or `bearer` is empty.
    requests.HTTPError
        If the Spotify API returns a non-200 response code.
    requests.RequestException
        For network-related exceptions such as timeouts or connection errors.

    Examples
    --------
    >>> token = "1POdFZRZbvb...qqillRxMr2z"
    >>> results = Spotify_Search("remaster track:Doxy artist:Miles Davis", token)
    >>> for item in results["tracks"]["items"]:
    ...     print(item["name"])
    Doxy
    """
    base_url: str = "https://api.spotify.com/v1/search"
    params: Dict[str, str] = {
        "q": f"track:{query}", # NOTE: For not, this only searches tracks
        "type": "track",
        "limit": str(limit)
    }
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {bearer}"
    }

    response: Response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()  # raises error for non-200 responses

    tracks_list: List[Displayed_Track] = Parse_Tracks_From_Json(response.json())
    return tracks_list

def Get_Metadata(track_id: str, bearer: str) -> Full_Metadata:
    """
    Fetch metadata for a specific Spotify track using its track ID.
    
    This function sends a GET request to the Spotify Web API's track endpoint and 
    returns the raw JSON metadata for the given track. It creates and sends the
    HTTP request and raises an exception if the HTTP status is invalid.

    Parameters
    ----------
    track_id : str
        The Spotify track ID to query (e.g., "11dFghCHEESElKmJXsNCbNl").
    bearer : str
        A valid OAuth Bearer token for the Spotify Web API.

    Returns
    -------
    Full_Metadata
        Custom data type containing album, artist(s), and track data

    Raises
    ------
    ValueError
        If `track_id` or `bearer` is empty.
    requests.HTTPError
        If the Spotify API returns a non-200 status code.
    requests.RequestException
        For network-related errors.

    Examples
    --------
    >>> token = "1POdFZRZbvb...qqillRxMr2z"
    >>> data = Get_Metadata("random_id12345", token)
    >>> print(data["name"])
    "Pink Pony Club"
    """

    # Verify arguments are not empty
    if not track_id:
        raise ValueError("track_id cannot be empty.")
    if not bearer:
        raise ValueError("bearer token cannot be empty.")
    
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {bearer}"
    }

    # Send request and validate HTTP status of response
    response: Response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse album data
    response_json: Dict[str, Any] = response.json()
    album: Dict[str, Any] = response_json["album"]
    album_name: str = album["name"]
    images = album["images"]
    first_image: Dict[str, Any] = images[0]
    image_url: str = first_image["url"]
    album_data: Album = Album(album_name, image_url)

    # Parse artist(s)
    artists = response_json["artists"]
    artists_data: List[Artist] = []
    for artist in artists:
        artist_data: Artist = Artist(artist["name"])
        artists_data.append(artist_data)

    # Parse track
    duration_ms: int = response_json["duration_ms"]
    explicit: bool = response_json["explicit"]
    name: str = response_json["name"]
    release_date: str = album["release_date"] # NOTE: This is from Album. May want to update ER Diagram
    track_number: int = response_json["track_number"]
    track_data: Track = Track(duration_ms, explicit, name, release_date, track_number)
    
    # Combine Data Types
    full_metadata: Full_Metadata = Full_Metadata(album_data, artists_data, track_data)

    return full_metadata