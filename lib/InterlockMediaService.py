import threading
import time
from lib.InterlockStandardFormats import InterlockSong


class Command:
    def __init__(self, function_name, args=None):
        self.function_name = function_name
        self.args = args


class MediaService:
    def __init__(self):
        print("initialzing music service")
        self.service = threading.Thread(target=self.listener)
        self.command = None
        self.device = None
        self.active = False
        self.queue = []
        self.queue_position = None
        self.duration = 0
        self.current_track_position = 0
        self.playing = False
        self.paused = False

    def start(self):
        print("starting")
        if self.device is not None:
            print("starting service")
            self.active = True
            self.service.start()
        else:
            raise Exception('Media Provider has not been set')

    def pause(self):
        print("pausing")
        self.paused = True
        self.device.pause()

    def stop(self):
        self.active = False
        self.device.stop()

    def listener(self):
        while self.active:
            if self.command is not None:
                self.run(self.command)
            if self.current_track_position >= self.duration and self.current_track_position != 0:
                self.next()
            if self.playing and not self.paused:
                self.current_track_position += 1
            time.sleep(1)
        exit()

    def set_output(self, device):
        self.device = device

    def play(self, media=None):
        self.paused = False
        if media is not None:
            if type(media) == InterlockSong:
                media = [media]
            elif type(media) == list:
                if type(media[0]) == str:
                    new_media = []
                    for url in media:
                        new_media.append(InterlockSong(url, 'Unknown', 'Unknown'))
                    media = new_media
            elif type(media) == str:
                media = [InterlockSong(media, 'Unknown', 'Unknown')]
            self.queue = media
            self.queue_position = 0
            item = media[0]
            self.play_media(item)
        else:
            self.device.play()

    def play_media(self, item):
        if self.device is not None:
            print("playing ", item.title)
            if not item.has_url():
                item.get_url()
            url = item.url
            self.duration = item.duration
            self.current_track_position = 0
            self.playing = True
            try:
                self.play_to_device(url)
            except:
                print("STILL GIVING A FUCKING ERROR")

    def play_to_device(self, url):
        if self.device.service == "sonos":
            print("trying to play", url)
            self.device.play_uri(url)
        elif self.device.service == "chromecast":
            self.device.play_audio(url)

    def next(self):
        if not self.at_end():
            print("playing next song")
            self.queue_position += 1
            item = self.queue[self.queue_position]
            self.play_media(item)
            return item

    def at_end(self):
        queue_length = len(self.queue)
        if queue_length == self.queue_position + 1:
            pass

    def get_queue(self):
        return self.queue

    def queue_media(self, number):
        if number in self.queue:
            item = self.queue[number]
            self.play_media(item)
            return item

    def run(self, command):
        if command is not None:
            if type(command) == Command:
                if command.function_name == "pause":
                    self.device.pause()



