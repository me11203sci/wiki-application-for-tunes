from fastapi import FastAPI
from src.commands import (
    create_track,
    add_track_to_album,
    add_file,
    link_artist
)
from src.queries import (
    get_track,
    get_album,
    get_artist_tracks
)
from src.events import subscribe
from src.projections import (
    on_track_created,
    on_track_added_to_album,
    on_file_added,
    on_artist_linked
)

# Register event handlers
subscribe("TrackCreated", on_track_created)
subscribe("TrackAddedToAlbum", on_track_added_to_album)
subscribe("FileAdded", on_file_added)
subscribe("ArtistLinked", on_artist_linked)

app = FastAPI()

# ----------- READ SIDE -------------

@app.get("/tracks/{track_id}")
def read_track(track_id: str):
    return get_track(track_id)

@app.get("/albums/{album_id}")
def read_album(album_id: str):
    return get_album(album_id)

@app.get("/artists/{artist_id}/tracks")
def read_artist_tracks(artist_id: str):
    return get_artist_tracks(artist_id)


# ----------- WRITE SIDE -------------

@app.post("/tracks")
def api_create_track(data: dict):
    return {"trackId": create_track(data["title"])}

@app.post("/albums/{album_id}/tracks/{track_id}")
def api_add_track_to_album(album_id: str, track_id: str, data: dict):
    add_track_to_album(track_id, album_id, data["trackNumber"])
    return {"status": "ok"}

@app.post("/files")
def api_add_file(data: dict):
    file_id = add_file(data["trackId"], data["format"], data["bitrate"])
    return {"fileId": file_id}

@app.post("/tracks/{track_id}/artists/{artist_id}")
def api_link_artist(track_id: str, artist_id: str):
    link_artist(track_id, artist_id)
    return {"status": "ok"}
