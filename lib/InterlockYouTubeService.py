from __future__ import unicode_literals
import youtube_dl


class YouTubeService:

    def get_url(self, url, opts):
        with youtube_dl.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, False)
            print(info['formats'])
            exit()
            return info['formats'][0]['url']

    def get_audio_url(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        return self.get_url(url, ydl_opts)

