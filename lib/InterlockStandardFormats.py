class InterlockMedia:
    def __init__(self, url, title, image, artist=None, album=None, play_music_id=None, play_music_class=None,
                 duration_seconds=0):
        self.url = url
        self.title = title
        self.image = image
        self.artist = artist
        self.album = album
        self.play_music_id = play_music_id
        self.play_music_class = play_music_class
        self.duration = duration_seconds

    def has_url(self):
        if self.url is not None:
            return True
        else:
            return False

    def get_url(self):
        if self.play_music_id is not None and self.play_music_class is not None:
            url = self.play_music_class.get_url(self.play_music_id)
            self.url = url
            return url

    def jsonify(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "image": self.image
        }

