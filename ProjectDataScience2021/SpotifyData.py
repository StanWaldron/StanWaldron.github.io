import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd

# In order to collect information about the number 1's over the years, I used
# a package called spotipy. Below I gain authentication for the Spotify API.

cid = '892be7f5ff2145f6b96e570a6b6c1c2b'
secret = 'b0cb7107631b4641ac010e890e8deee6'

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# This function takes a playlist as an input - I found a playlist that contained
# all of the no.1's from 1953 onwards and then extracted the audio audio_features
# from each track


def call_playlist(creator, playlist_id):

    # set up the features I would like after having looked at the possibilities
    # what these mean can be found here https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features

    playlist_features_list = ["artist", "album", "track_name",  "track_id", "danceability", "energy", "key", "loudness",
                              "mode", "speechiness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]

    playlist_df = pd.DataFrame(columns=playlist_features_list)

    # keep spotify iterating over the whole playlist as limit is automaticall set to 50, but this has more than 1300

    playlist = sp.user_playlist_tracks(creator, playlist_id)
    tracks = playlist['items']
    while playlist['next']:
        playlist = sp.next(playlist)
        tracks.extend(playlist['items'])

    # loop through the tracks in the playlist

    for track in tracks:

        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]

        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index=[0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)

    # Finally, return the dataframe

    return playlist_df

# Function to find the release date of the tracks so that I can compare it to other time series data
# Spotify doesn't initially provide the release date, which is tied to the album_id, with the track, so we have to find that by using spotify's search function and taking the first value that comes up


def find_album_release(name):
    album_ids = []
    album_releases = []
    for x in name:
        x = x.replace("'", "")      # Remove the quotes from album name
        results = sp.search(q="album:" + x, type="album")
        if not results["albums"]["items"]:
            # Some items returned no search results, especially older tracks
            album_ids.append('')
            album_releases.append('')
        else:
            album_id = results['albums']['items'][0]['uri']
            album_ids.append(album_id)
            album_releases.append(sp.album(album_id)['release_date'])
    return album_releases

# Finally, we call the functions and export the results.ArithmeticError


final = call_playlist('spotify', '5GEf0fJs9xBPr5R4jEQjtw')
finalalbums = find_album_release(final['album'])
final['album_id'] = finalalbums
final['release_date'] = finalalbums
final.to_csv(r'C:\Users\Stan\Desktop\FinalData2.csv')

# I now have a dataframe that has all the info I need to begin comparisons
# Shortomings of the data: only album release, not when it was no.1
# Some not correctly parsed, so lost about 200 as spotify couldn't find the album, especially the older ones
# The search through the album results meant that sometimes albums came back as the remastered version, this can skew time data
