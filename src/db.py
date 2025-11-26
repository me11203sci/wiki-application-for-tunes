from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["musicdb"]

# Write model collections
write_tracks = db["write_tracks"]
write_albums = db["write_albums"]
write_artists = db["write_artists"]
write_files = db["write_files"]

# Read model projections
track_detail_view = db["track_detail_view"]
album_detail_view = db["album_detail_view"]
artist_tracks_view = db["artist_tracks_view"]
file_detail_view = db["file_detail_view"]
