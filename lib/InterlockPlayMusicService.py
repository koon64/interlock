from gmusicapi import Mobileclient
from lib.InterlockStandardFormats import InterlockMedia


class PlayMusicService:
    def __init__(self, oauth_login):
        self.api = Mobileclient()
        # self.api.perform_oauth()
        self.api.oauth_login(oauth_login)

    def get_url(self, track_id):
        return self.api.get_stream_url(track_id)

    def get_library(self):
        return self.api.get_all_songs()

    def search(self, query, limit=5):
        results = self.api.search(query, limit)
        return results

    def create_track_objs(self, tracks):
        track_objs = []
        for track in tracks:
            title = track['title']
            image = track['albumArtRef'][0]['url']
            artist = track['artist']
            seconds = int(track['durationMillis']) / 1000
            track_obj = InterlockMedia(None, title, image, artist, play_music_id=track['id'], play_music_class=self,
                                       duration_seconds=seconds)
            track_objs.append(track_obj)
        return track_objs

# * 33e20d31e6917cc5
# * 3ec27c8be2fdc591
# * 30fc30516c436e9d
# * ios:F357B6D5-4E54-4EAE-BD08-60002923CF9C
# * 330e23c32a716bdd

