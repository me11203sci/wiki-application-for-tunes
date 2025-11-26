import uuid
from db import write_tracks, write_albums, write_artists, write_files
from events import publish

# ---------- Create Track ----------

def create_track(title: str):
    track_id = str(uuid.uuid4())

    write_tracks.insert_one({"trackId": track_id, "title": title})

    publish("TrackCreated", {
        "trackId": track_id,
        "title": title,
    })

    return track_id


# ---------- Add Track To Album ----------

def add_track_to_album(track_id, album_id, track_number):
    album = write_albums.find_one({"albumId": album_id})
    track = write_tracks.find_one({"trackId": track_id})

    publish("TrackAddedToAlbum", {
        "trackId": track_id,
        "trackTitle": track["title"],
        "albumId": album_id,
        "albumTitle": album["title"],
        "albumYear": album.get("year"),
        "trackNumber": track_number,
    })


# ---------- Add File ----------

def add_file(track_id, format, bitrate):
    file_id = str(uuid.uuid4())

    write_files.insert_one({
        "fileId": file_id,
        "trackId": track_id,
        "format": format,
        "bitrate": bitrate
    })

    publish("FileAdded", {
        "fileId": file_id,
        "trackId": track_id,
        "format": format,
        "bitrate": bitrate
    })

    return file_id


# ---------- Link Artist ----------

def link_artist(track_id, artist_id):
    artist = write_artists.find_one({"artistId": artist_id})
    track = write_tracks.find_one({"trackId": track_id})

    publish("ArtistLinked", {
        "trackId": track_id,
        "trackTitle": track["title"],
        "artistId": artist_id,
        "artistName": artist["name"],
    })

