import soco
from lib.InterlockStandardFormats import InterlockMedia


class SonosService:
    def __init__(self):
        self.speakers = []
        for zone in soco.discover():
            speaker = SonosSpeaker(zone)
            self.speakers.append(speaker)

    def device(self, name):
        for speaker in self.speakers:
            if speaker.speaker_name == name:
                return speaker


class SonosSpeaker:
    def __init__(self, speaker):
        self.service = "sonos"
        self.speaker_name = speaker.player_name
        self.speaker = speaker
        self.product_name = "idk"
        self.type = "speakers"
        self.label = self.speaker_name
        self.id = self.speaker_name.replace("'", "")
        self.ip = speaker.ip_address
        try:
            self.track = speaker.get_current_track_info()
        finally:
            self.track = None

    def __str__(self):
        return "[ INTERLOCK DEVICE | "+self.label+" | SONOS "+self.product_name+" ]"

    def play_uri(self, uri):
        self.speaker.play_uri(uri)

    def pause(self):
        self.speaker.pause()

    def play(self):
        self.speaker.play()

    def stop(self):
        self.speaker.stop()

    def play_audio(self, url, t, i):
        self.play_uri(url)

    def get_media(self):
        track = self.speaker.get_current_track_info()
        print(track)
        return InterlockMedia(None, track['title'], track['album_art'], track['artist'], track['album'])

    def get_state(self):
        return self.speaker.get_current_transport_info()['current_transport_state']

    def volume(self, volume=None):
        if volume is not None:
            self.speaker.volume = volume
        return self.speaker.volume

    def mute(self):
        self.volume(0)




