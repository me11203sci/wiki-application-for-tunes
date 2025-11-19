import requests
from typing import Any, Dict
from requests.models import Response
import base64

def get_spotify_access_token(client_id: str, client_secret: str) -> str:
    """
    Obtain an access token for the Spotify Web API using the Client Credentials flow.

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
        A Spotify access token string (Bearer token) valid for API authentication.

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
    TOKEN_URL = "https://accounts.spotify.com/api/token"

    # Encode client ID and secret
    auth_str: str = f"{client_id}:{client_secret}"
    b64_auth_str: str = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    # Headers for HTTP request
    headers: Dict[str, str] = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data for HTTP request
    data: Dict[str, str] = {
        "grant_type": "client_credentials"
    }

    # Post HTTP request
    resp: Response = requests.post(TOKEN_URL, headers=headers, data=data)
    resp.raise_for_status() # NOTE: Exception could be raised here, caller is responsible for error handling logic

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
        "q": "Beatles",     # search query
        "type": "track",    # search for tracks
        "limit": 5          # number of results
    }

    # Submit HTTP request
    search_resp: Response = requests.get(search_url, headers=search_headers, params=search_params)
    search_resp.raise_for_status()
    search_results: Dict[str, Any] = search_resp.json()

    # Parse results
    if search_results["tracks"]["items"]:
        return True
    else:
        return False