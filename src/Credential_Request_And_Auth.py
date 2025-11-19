import requests
import base64

def get_spotify_access_token(client_id: str, client_secret: str) -> str:
    # Spotify token URL
    TOKEN_URL = "https://accounts.spotify.com/api/token"

    # Encode client ID and secret
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    resp = requests.post(TOKEN_URL, headers=headers, data=data)
    resp.raise_for_status() # NOTE: Exception could be raised here, caller is responsible for error handling logic

    token_response = resp.json()
    access_token = token_response["access_token"]

    return access_token

def authenticate_spotify_access_token(access_token: str) -> bool:
    search_url = "https://api.spotify.com/v1/search"
    search_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    search_params = {
        "q": "Beatles",     # search query
        "type": "track",    # search for tracks
        "limit": 5          # number of results
    }

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    search_resp.raise_for_status()
    search_results = search_resp.json()

    if search_results["tracks"]["items"]:
        return True
    else:
        return False