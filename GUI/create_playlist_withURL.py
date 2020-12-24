import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl
from googleapiclient.discovery import build
# from exceptions import ResponseException


# playlist_id = input("Enter youtube playlist id: ")
# playlist_full_url = input("Enter youtube playlist id: ").split('list=')
# playlist_id = playlist_full_url[1]


class CreatePlaylist:
    DEVELOPER_KEY = 'AIzaSyBT1NAr3RT8PtquaxymwuzWR8pO4ZcUREs'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def __init__(self, spotify_id, spotify_token, playlist_id):
        # self.songs = []
        self.youtube = build(
            CreatePlaylist.YOUTUBE_API_SERVICE_NAME,
            CreatePlaylist.YOUTUBE_API_VERSION,
            developerKey=CreatePlaylist.DEVELOPER_KEY
        )
        self.all_song_info = {}
        self.playlist_id = playlist_id
        self.spotify_id = spotify_id
        self.spotify_token = spotify_token

    # Step 2: Grab Our Liked Videos & Create a Dictionary of Important Songs
    def get_videos(self, youtube, playlist_id, page_token=None):

        """Grab Our Liked Videos & Create A Dictionary Of Important Song Information"""
        result = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults="50",
            pageToken=page_token
        ).execute()

        # collect each video and get important information
        for item in result["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item['snippet']['resourceId']["videoId"])

            if video_title == 'Deleted video':  # 若影片被刪除，跳過此輪
                continue

            # use youtube_dl to collect the song name & artist name
            try:
                video = youtube_dl.YoutubeDL({}).extract_info(
                    youtube_url, download=False)
            except:
                pass

            song_name = video["track"]
            album = video["album"]
            artist = video["artist"]

            if song_name is not None and artist is not None:
                # save all important info and skip any missing song and artist
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,
                    "album":album,

                    # add the uri, easy to get song to put into playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)
                }
            else:
                print("not found")

    # Step 3: Create A New Playlist
    def create_playlist(self):
        """Create A New Playlist"""
        # 將等等要post的data用request_body存起來，轉換成JSON格式
        request_body = json.dumps({
             "name": "Playlist from YT",
             "description": "PBC Project",
             "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json.get("id")

    # Step 4: Search For the Song
    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?q=track:{}+artist:{}&type=track,artist,album&limit=20&offset=0".format(
            song_name,
            artist,
            

        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        if len(songs) != 0:
            uri = songs[0]["uri"]
        else:
            uri = False
            print(uri)
        return uri

    # Step 5: Add this song into the new Spotify playlist
    def add_song_to_playlist(self):
        """Add all liked songs into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.get_videos(self.youtube, self.playlist_id)

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items() if info["spotify_uri"] != False]

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        # check for valid response status
        # if response.status_code != 200:
        #     raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    with open('all_secrets.txt', 'r') as secrets:
        spotify_id = secrets.readline().strip('\n')
        spotify_token = secrets.readline().strip('\n')
        playlist_id = secrets.readline().strip('\n')
        secrets.close()

    print(spotify_id, spotify_token, playlist_id)
    cp = CreatePlaylist(spotify_id, spotify_token, playlist_id)
    cp.add_song_to_playlist()
    print("OK!")
