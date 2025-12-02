"""
credential_request_and_auth — A small module for obtaining and validating
Spotify API tokens.

This module provides functions to: (1) retrieve an access token for the
Spotify Web API using the Client Credentials flow, and (2) verify whether
a given access token is valid by making a test API call. It is designed
for backend or utility scripts where you need to programmatically interact
with Spotify's API.

Functions
---------
get_spotify_access_token
    Request and return a Spotify access token using client credentials.
authenticate_spotify_access_token
    Check if a Spotify access token works by performing a sample search.

Notes
-----
- The "get_spotify_access_token" function raises "requests.HTTPError" for
  non-success responses. Caller should handle all Exceptions.
- The "authenticate_spotify_access_token" function assumes the token has
  the necessary scopes to perform a simple search.
"""

import base64
from typing import Any, Dict
from requests.models import Response
import requests


def get_spotify_access_token(client_id: str, client_secret: str) -> str:
    """
    Obtain an access token for the Spotify Web API using client credentials.

    This function sends a request to Spotify's token endpoint with the provided
    "client_id" and "client_secret", and returns a valid bearer token that can
    be used for subsequent API calls. The caller is responsible for handling
    any HTTP errors or exceptions that occur during token retrieval.

    Parameters
    ----------
    client_id : str
        The Spotify Client ID associated with your application.
    client_secret : str
        The Spotify Client Secret associated with your application.

    Returns
    -------
    access_token : str
        A Spotify access token (Bearer token) valid for API authentication.

    Raises
    ------
    requests.HTTPError
        If the HTTP request to retrieve the token fails (non-2xx status code).

    Examples
    --------
    >>> token = get_spotify_access_token("my_client_id", "my_client_secret")
    >>> isinstance(token, str)
    True
    """
    # Spotify token URL
    token_url = "https://accounts.spotify.com/api/token"

    # Encode client ID and secret
    auth_str: str = f"{client_id}:{client_secret}"
    utf8_auth_str: bytes = auth_str.encode("utf-8")
    b64_auth_str: str = base64.b64encode(utf8_auth_str).decode("utf-8")

    # Headers for HTTP request
    headers: Dict[str, str] = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Data for HTTP request
    data: Dict[str, str] = {"grant_type": "client_credentials"}

    # Post HTTP request
    resp: Response = requests.post(token_url, headers=headers, data=data,
                                   timeout=20)
    resp.raise_for_status()  # Caller is responsible for error handling

    # Parse HTTP response
    token_response: Dict[str, Any] = resp.json()
    access_token: str = token_response["access_token"]

    return access_token


def authenticate_spotify_access_token(access_token: str) -> bool:
    """
    Validate a Spotify access token by making a test search request.

    This function sends a "search" request to the Spotify Web API using the
    provided "access_token" and checks whether the call succeeds and returns
    at least one track. It is useful for verifying that the token is valid
    and has the necessary scope to make API calls. The caller is responsible
    for handling any HTTP errors or exceptions that occur during request.

    Parameters
    ----------
    access_token : str
        A Spotify API access token (Bearer token) to be validated.

    Returns
    -------
    bool
        "True" if the token is valid and returns search results, "False"
        otherwise.

    Raises
    ------
    requests.HTTPError
        If the HTTP request fails (non-2xx response).

    Examples
    --------
    >>> valid = authenticate_spotify_access_token("BQD...your_token_here...")
    >>> isinstance(valid, bool)
    True
    """
    search_url: str = "https://api.spotify.com/v1/search"
    search_headers: Dict[str, str] = {
        "Authorization": f"Bearer {access_token}"
    }
    search_params: Dict[str, str] = {
        "q": "Beatles",  # search query
        "type": "track",  # search for tracks
        "limit": 5,  # number of results
    }

    # Submit HTTP request
    search_resp: Response = requests.get(
        search_url, headers=search_headers, params=search_params, timeout=20
    )
    search_resp.raise_for_status()
    search_results: Dict[str, Any] = search_resp.json()

    # Parse results
    return bool(search_results["tracks"]["items"])
