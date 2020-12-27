import json
import os
import re
from youtube_title_parse import get_artist_title

# import googleapiclient.discovery
# import googleapiclient.errors
import requests
import youtube_dl
from googleapiclient.discovery import build
# from exceptions import ResponseException


class CreatePlaylist:
    DEVELOPER_KEY = 'AIzaSyBT1NAr3RT8PtquaxymwuzWR8pO4ZcUREs'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    # Step 1: 處理Youtube API的設定
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

    # Step 2: 利用youtube api請求播放清單中影片的資訊，並為所有抓到的歌曲資訊建立dictionary
    def get_videos(self, youtube, playlist_id, page_token=None):

        # 從youtube api取得輸入播放清單的資料結構
        result = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults="50",
            pageToken=page_token
        ).execute()

        # 取得每部影片的url
        for item in result["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item['snippet']['resourceId']["videoId"])

            if video_title == 'Deleted video':  # 若影片被刪除，跳過此輪
                continue

            # 利用youtube_dl及取得的url
            try:
                video = youtube_dl.YoutubeDL({}).extract_info(
                    youtube_url, download=False)
            except:
                pass

            # 存取3個辨識歌曲的變數，分別為取名、專輯名、藝人名
            song_name = video["track"]
            album = video["album"]
            artist = video["artist"]

            if song_name is not None and artist is not None:
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,
                    "album":album,

                    # 利用自定義函數 get_spotify_uri 傳入辨識歌曲的變數，得到該歌曲的spotify uri
                    "spotify_uri": self.get_spotify_uri(song_name, artist)
                }
            elif song_name is None:
                song_name, artist = get_artist_title(video_title)
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,
                    "album":album,

                    # 利用自定義函數 get_spotify_uri 傳入辨識歌曲的變數，得到該歌曲的spotify uri
                    "spotify_uri": self.get_spotify_uri(song_name, artist)
                }
            else:
                print("not found")

    # Step 3: 在spotify建立新歌單
    def create_playlist(self):

        # 將等等要post的data用request_body存起來，轉換成JSON格式
        request_body = json.dumps({
             "name": "Playlist from YT",
             "description": "PBC Project",
             "public": True
        })

        # 向spotify請求建立新歌單
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json.get("id")

    # Step 4: 透過spotify api尋找youtube影片對應的歌曲，並回傳該歌曲的uri
    def get_spotify_uri(self, song_name, artist):

        # 尋找歌曲
        query = "https://api.spotify.com/v1/search?q=track:{}+artist:{}&type=track,artist,album&limit=20&offset=0".format(
            song_name,
            artist,
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]  # 歌曲資訊在spotify api的資料結構中是在items中

        # 若在spotify端有找到，回傳uri，否則輸出False
        if len(songs) != 0:
            uri = songs[0]["uri"]
        else:
            uri = False
            print(uri)
        return uri

    # Step 5: 將歌曲加入新建的播放清單
    def add_song_to_playlist(self):

        self.get_videos(self.youtube, self.playlist_id)

        # 把 all_song_info 中存的uri，全部存到一個list中
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items() if info["spotify_uri"] != False]

        playlist_id = self.create_playlist()

        # 把所有歌曲丟進新歌單
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        # check for valid response status
        # if response.status_code != 200:
        #     raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json
