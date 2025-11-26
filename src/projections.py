from db import (
    track_detail_view,
    album_detail_view,
    artist_tracks_view,
    file_detail_view,
)

# ---------- Track Created ----------

def on_track_created(event):
    track_id = event["trackId"]
    track_doc = {
        "trackId": track_id,
        "title": event["title"],
        "artists": [],
        "files": [],
        "album": None,
        "trackNumber": None,
    }
    track_detail_view.insert_one(track_doc)


# ---------- Track Added To Album ----------

def on_track_added_to_album(event):
    track_id = event["trackId"]
    album = {
        "albumId": event["albumId"],
        "title": event["albumTitle"],
        "year": event["albumYear"],
    }

    # Update track_detail_view
    track_detail_view.update_one(
        {"trackId": track_id},
        {"$set": {"album": album, "trackNumber": event.get("trackNumber")}}
    )

    # Update album_detail_view
    album_detail_view.update_one(
        {"albumId": event["albumId"]},
        {"$push": {"tracks": {
            "trackId": track_id,
            "title": event["trackTitle"],
            "trackNumber": event["trackNumber"]
        }}},
        upsert=True
    )


# ---------- File Added ----------

def on_file_added(event):
    file_detail_view.insert_one(event)

    track_detail_view.update_one(
        {"trackId": event["trackId"]},
        {"$push": {"files": {
            "fileId": event["fileId"],
            "format": event["format"],
            "bitrate": event["bitrate"]
        }}}
    )


# ---------- Artist Linked To Track ----------

def on_artist_linked(event):
    # read model: track_detail_view
    track_detail_view.update_one(
        {"trackId": event["trackId"]},
        {"$push": {"artists": {
            "artistId": event["artistId"],
            "name": event["artistName"]
        }}}
    )

    # read model: artist_tracks_view
    artist_tracks_view.update_one(
        {"artistId": event["artistId"]},
        {"$push": {"tracks": {
            "trackId": event["trackId"],
            "title": event["trackTitle"],
        }}},
        upsert=True
    )
