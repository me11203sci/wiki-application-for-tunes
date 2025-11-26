from db import (
    track_detail_view,
    album_detail_view,
    artist_tracks_view,
)

def get_track(track_id):
    return track_detail_view.find_one({"trackId": track_id})

def get_album(album_id):
    return album_detail_view.find_one({"albumId": album_id})

def get_artist_tracks(artist_id):
    return artist_tracks_view.find_one({"artistId": artist_id})
