from kivy.app import App

import os
from os.path import expanduser

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer

from lib import downloader


threads = []


class StreamIesVideoPlayer(VideoPlayer):

    def __init__(self, **kwargs):
        downloads_directory = expanduser("~") + os.sep + "Downloads" + os.sep
        torrent_name = downloads_directory + "[kickass.to]supernatural.s10e04.hdtv.x264.lol.ettv.torrent"

        dl = downloader.Download(torrent_name)
        video_path = dl.retrieve_video_file_name()

        if os.path.isfile(video_path + ".st"):
            self.source = video_path

            video_done_file_path = video_path + ".dn"
            if not os.path.isfile(video_done_file_path):
                threaded_download = downloader.ThreadedDownload(torrent_name)
                threaded_download.setName(torrent_name)
                threaded_download.setDaemon(True)
                threaded_download.start()
                threaded_download.join(0.1)

                threads.append(threaded_download)
        else:
            threaded_download = downloader.ThreadedDownload(torrent_name=torrent_name, video_player=self)
            threaded_download.setName(torrent_name)
            threaded_download.setDaemon(True)
            threaded_download.start()
            threaded_download.join(0.1)

            threads.append(threaded_download)

        super(StreamIesVideoPlayer, self).__init__(**kwargs)

    def on_state(self, instance, value):
        # if value == 'play':
        #     downloads_directory = expanduser("~") + os.sep + "Downloads" + os.sep
        #     torrent_name = downloads_directory + "[kickass.to]supernatural.s10e04.hdtv.x264.lol.ettv.torrent"
        #
        #     if threading.activeCount() < 2:
        #         if not os.path.isfile(self.source):
        #             threaded_download = downloader.ThreadedDownload(torrent_name=torrent_name, video_player=self)
        #             self.play = False
        #         else:
        #             threaded_download = downloader.ThreadedDownload(torrent_name)
        #
        #         threaded_download.setName(torrent_name)
        #         threaded_download.start()

        return super(StreamIesVideoPlayer, self).on_state(instance, value)


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