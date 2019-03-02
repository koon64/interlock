from gmusicapi import Mobileclient
from lib.InterlockStandardFormats import *
from re import compile


class PlayMusicService:
    def __init__(self, oauth_login):
        self.api = Mobileclient()
        # self.api.perform_oauth()
        self.api.oauth_login(oauth_login)
        self.information = InterlockMediaService('play_music', 'Google Play Music', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Play_music_triangle.svg/2000px-Play_music_triangle.svg.png', 'music')

    def get_url(self, track_id):
        return self.api.get_stream_url(track_id)

    def get_library(self):
        return self.api.get_all_songs()

    def remove_special_characters(self, string):
        regex = compile('[^a-zA-Z]')
        return regex.sub('', string).lower()

    def get_albums(self):
        library = self.get_library()
        albums = {}
        for song in library:
            album_name = song['album']
            if album_name != "":
                if album_name in albums:
                    albums[album_name].append(song)
                else:
                    albums[album_name] = []
        return_albums = []
        for album_name in albums:
            album = albums[album_name]
            if len(album) > 0:
                first_song_reference = album[0]
                album_image = first_song_reference['albumArtRef'][0]['url']
                album_artist = first_song_reference['artist']
                album_year = first_song_reference['year']
                album_obj = InterlockAlbum(album_name, album_artist, album_image, album_year)
                song_objs = self.create_track_objs(album)
                album_obj.add_songs(song_objs)
                return_albums.append(album_obj)
        return return_albums

    def get_album(self, album_name):
        album_name = self.remove_special_characters(album_name)
        albums = self.get_albums()
        album = None
        for alb in albums:
            if self.remove_special_characters(alb.name) == album_name:
                album = alb
        return album

    def get_playlist(self, playlist_name):
        playlist_name = self.remove_special_characters(playlist_name)
        playlist = None
        playlists = self.get_playlists()
        for pl in playlists:
            if self.remove_special_characters(pl.name) == playlist_name:
                playlist = pl
        return playlist

    def get_playlists(self):
        playlists = self.api.get_all_user_playlist_contents()
        playlist_objs = []
        for playlist in playlists:
            playlist_obj = InterlockPlaylist(playlist['name'])
            song_objs = self.create_track_objs(playlist['tracks'], True)
            playlist_obj.add_songs(song_objs)
            playlist_objs.append(playlist_obj)
        return playlist_objs

    def search(self, query, limit=5):
        results = self.api.search(query, limit)
        return results

    def create_track_objs(self, tracks, playlist_track=False):
        track_objs = []
        for track in tracks:
            if playlist_track:
                orig_track = track
                if "track" in orig_track:
                    track = orig_track['track']
                    track_id = orig_track['trackId']
                else:
                    track = None
            else:
                track_id = track['id']
            if track is not None:
                title = track['title']
                image = track['albumArtRef'][0]['url']
                artist = track['artist']
                album_position = track['trackNumber']
                seconds = int(track['durationMillis']) / 1000
                track_obj = InterlockSong(None, title, image, artist, play_music_id=track_id, play_music_class=self,
                                          duration_seconds=seconds,album_position=album_position)
                track_objs.append(track_obj)
        return track_objs

# * 33e20d31e6917cc5
# * 3ec27c8be2fdc591
# * 30fc30516c436e9d
# * ios:F357B6D5-4E54-4EAE-BD08-60002923CF9C
# * 330e23c32a716bdd

