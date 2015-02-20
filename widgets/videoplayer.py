import os

from types import StringType, BooleanType

from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window

from hachoir_core.error import HachoirError

from lib import downloader
from lib.popups import VideoPlayerPopup
from lib.video import Metadata
from lib.thread import threads


class StreamIesVideoPlayer(VideoPlayer):
    """
    Class for video player specified exactly to Stream-Ies application
    Is extendind built-in Kivy VideoPlayer for ease of use
    """

    video_path = StringType('')
    is_video_download_started = BooleanType(False)
    is_video_download_done = BooleanType(False)

    def __init__(self, **kwargs):
        """
        __init__ method for StreamIesVideoPlayer class
        Initializes video player, starts threaded torrent downloading if it is needed

        :param kwargs:
        :return:
        """

        self.allow_fullscreen = True

        super(StreamIesVideoPlayer, self).__init__(**kwargs)

    def set_up_video_from_torrent(self, torrent_name):
        # Retrieve video path from torrent file
        dl = downloader.Download(torrent_name)
        self.video_path = dl.retrieve_video_file_name()

        # Check if .st file is created, if is, then it means that video download has started
        if os.path.isfile(self.video_path + ".st"):
            self.is_video_download_started = True
            self.set_video_source(self.video_path)

            video_done_file_path = self.video_path + ".dn"
            # Check if .dn file is created, if is not, then it means that video download is not finished yet
            # and download should be continued
            if not os.path.isfile(video_done_file_path):
                threaded_download = downloader.ThreadedDownload(torrent_name=torrent_name, video_player=self)
                threaded_download.setName(torrent_name)
                threaded_download.setDaemon(True)
                threaded_download.start()
                threaded_download.join(0.1)

                threads.append(threaded_download)
            else:
                self.is_video_download_done = True
        else:
            # Start loading video
            threaded_download = downloader.ThreadedDownload(torrent_name=torrent_name, video_player=self)
            threaded_download.setName(torrent_name)
            threaded_download.setDaemon(True)
            threaded_download.start()
            threaded_download.join(0.1)

            threads.append(threaded_download)

    def on_state(self, instance, value):
        """
        Event fired when play/pause button is pressed
        Function checks whether video should be started.
        If video download is not started or metadata is not received, video will not be started and popup will occur

        :param instance:
        :param value:
        :return:
        """

        # If video download is not started, show popup, because we have nothing to show to user
        if not self.is_video_download_started:
            value = 'stop'
            popup = VideoPlayerPopup()
            popup.open()
        else:
            # Check if we get video metadata to verify that video is playable. If we don't, show popup
            try:
                metadata = Metadata(self.video_path)
                metadata.extract_metadata()
            except HachoirError as e:
                value = 'stop'
                popup = VideoPlayerPopup()
                popup.open()

                print(e)

        return super(StreamIesVideoPlayer, self).on_state(instance, value)

    def set_video_source(self, video_path):
        """
        Sets source of video

        :param video_path: str
        :return:
        """

        self.source = video_path

        super(StreamIesVideoPlayer, self)._do_video_load()

    def on_fullscreen(self, instance, value):
        Window.fullscreen = value

        return super(StreamIesVideoPlayer, self).on_fullscreen(instance, value)