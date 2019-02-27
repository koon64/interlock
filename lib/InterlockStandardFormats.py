import random


class InterlockSong:
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


class InterlockMediaService:
    def __init__(self, name, label, icon, media_type):
        self.name = name
        self.label = label
        self.icon = icon
        self.type = media_type


class InterlockAlbum:
    def __init__(self, name, artist, image, year=None):
        self.name = name
        self.image = image
        self.artist = artist
        self.year = year
        self.songs = []

    def __str__(self):
        year = " (" + str(self.year) + ")" if self.year is not None else ""  # displays the year if it is not null
        return "[ INTERLOCK ALBUM | "+self.artist+" | "+self.name+year+" | "+str(len(self.songs))+" songs ]"

    def add_song(self, song):
        if type(song) is InterlockSong:
            self.songs.append(song)

    def add_songs(self, songs):
        for song in songs:
            self.add_song(song)


class InterlockPlaylist:
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.thumbnails = []

    def __str__(self):
        return "[ INTERLOCK PLAYLIST | "+self.name+" | "+str(len(self.songs))+" songs ]"

    def add_song(self, song, dont_refresh_thumbnails=False):
        if type(song) is InterlockSong:
            self.songs.append(song)
            if not dont_refresh_thumbnails:
                self.refresh_thumbnails()

    def add_songs(self, songs):
        for song in songs:
            self.add_song(song, True)
        self.refresh_thumbnails()

    def refresh_thumbnails(self):
        self.thumbnails = []
        song_count = len(self.songs)
        print(self.songs)
        if song_count > 0:
            # shuffles the songs before the loop
            if song_count > 3:
                songs = self.songs
                random.shuffle(songs)
            for i in range(0, 4):
                if song_count == 1:
                    self.thumbnails.append(self.songs[0].image)
                elif song_count == 2 or song_count == 3:
                    j = 0 if i % 2 == 0 else 1  # if it is even then it uses the 0th image else 1st
                    self.thumbnails.append(self.songs[j].image)
                    # todo: fix this please
                    # if song_count == 3:
                    #     self.thumbnails[3] = self.songs[2].image
                else:
                    self.thumbnails.append(self.songs[i].image)

