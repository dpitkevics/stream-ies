from kivy.app import App

import os
from os.path import expanduser

from types import StringType, BooleanType

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer

from lib import downloader
from lib.popups import VideoPlayerPopup


threads = []


class StreamIesVideoPlayer(VideoPlayer):
    video_path = StringType('')
    is_video_download_started = BooleanType(False)
    is_video_download_done = BooleanType(False)

    def __init__(self, **kwargs):
        self.allow_fullscreen = True

        downloads_directory = expanduser("~") + os.sep + "Downloads" + os.sep
        torrent_name = downloads_directory + "[kickass.to]supernatural.s10e04.hdtv.x264.lol.ettv.torrent"

        dl = downloader.Download(torrent_name)
        self.video_path = dl.retrieve_video_file_name()

        if os.path.isfile(self.video_path + ".st"):
            self.is_video_download_started = True
            self.set_video_source(self.video_path)

            video_done_file_path = self.video_path + ".dn"
            if not os.path.isfile(video_done_file_path):
                threaded_download = downloader.ThreadedDownload(torrent_name)
                threaded_download.setName(torrent_name)
                threaded_download.setDaemon(True)
                threaded_download.start()
                threaded_download.join(0.1)

                threads.append(threaded_download)
            else:
                self.is_video_download_done = True
        else:
            threaded_download = downloader.ThreadedDownload(torrent_name=torrent_name, video_player=self)
            threaded_download.setName(torrent_name)
            threaded_download.setDaemon(True)
            threaded_download.start()
            threaded_download.join(0.1)

            threads.append(threaded_download)

        super(StreamIesVideoPlayer, self).__init__(**kwargs)

    def on_state(self, instance, value):
        print(self._video.source)

        if not self.is_video_download_started:
            value = 'stop'
            popup = VideoPlayerPopup()
            popup.open()

        return super(StreamIesVideoPlayer, self).on_state(instance, value)

    def set_video_source(self, video_path):
        self.source = video_path

        super(StreamIesVideoPlayer, self)._do_video_load()


class MainWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)


class StreamIesApp(App):
    def build(self):
        return MainWidget()

    def on_stop(self):
        for i in range(len(threads)):
            threads[i].stop()


if __name__ == '__main__':
    StreamIesApp().run()