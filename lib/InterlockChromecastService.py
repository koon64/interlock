import pychromecast
from lib.InterlockStandardFormats import InterlockSong
import random


class ChromecastService:
    def __init__(self):
        chromecasts = pychromecast.get_chromecasts()
        self.chromecasts = []
        for chromecast in chromecasts:
            device = ChromecastDevice(chromecast)
            self.chromecasts.append(device)

    def device(self, device_id):
        return next(cc for cc in self.chromecasts if cc.id == device_id)


class ChromecastDevice:
    def __init__(self, chromecast):
        self.device = chromecast
        self.label = chromecast.device.friendly_name
        self.id = self.label
        self.product_name = chromecast.device.model_name
        self.service = "chromecast"
        if self.product_name == "Google Home Hub" or self.product_name == "Chromecast":
            self.type = "display"
        elif self.product_name == "Chromecast Audio":
            self.type = "speakers"
        self.device.wait()
        self.mc = self.device.media_controller
        self.media_service = None

    def __str__(self):
        return "[ INTERLOCK DEVICE | "+self.product_name+" | "+self.label+" | "+str(self.media_service)+" ]"

    def play_media(self, url, type, title=None, image=None):
        self.mc.play_media(url, type, title, image)

    def play_audio(self, url, title=None, image=None):
        self.play_media(url, 'audio/mp3', title, image)

    def play(self):
        if self.mc is not None:
            self.mc.play()

    def pause(self):
        if self.mc is not None:
            self.mc.pause()

    def stop(self):
        if self.mc is not None:
            self.mc.stop()

    def volume(self, volume=None):
        if volume is not None:
            if volume is int:
                volume = int(volume)
                if 0 <= volume <= 100:
                    volume /= 100
                    self.device.set_volume(volume)
        else:
            return self.device.status.volume_level

    def mute(self):
        self.volume(0)

    def get_state(self):
        # todo: fix this, return PLAYING or PAUSED or STOPPED
        status = self.media_service.get_state()
        print(status)
        return status

    def set_media_service(self, service):
        self.media_service = service
        print('music service is not')
        print('serivce', service)

    def get_media(self):
        if self.media_service is not None:
            track = self.media_service.get_track()
            print(self.label + 'is working, playing: ', track)
            return track
        else:
            print(self.label+'\'s media service is not set')
            return None

    def get_media_old(self):
        if self.mc is not None:
            status = self.mc.status
            print(status)
            title = status.title
            if title is not None:
                if len(status.images) != 0:
                    image_obj = status.images[0]
                    image = image_obj.url
                else:
                    image = None
                return InterlockSong(None, title, image)
            return None
        return None

