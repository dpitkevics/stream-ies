import os

from types import StringType, BooleanType

from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.logger import Logger

from hachoir_core.error import HachoirError

from lib import downloader
from lib.popups import VideoPlayerPopup
from lib.video import Metadata
from lib.thread import threads


class StreamIesVideoPlayer(Video):
    """
    Class for video player specified exactly to Stream-Ies application
    Is extendind built-in Kivy VideoPlayer for ease of use
    """

    video_path = StringType('')
    is_video_download_started = BooleanType(False)
    is_video_download_done = BooleanType(False)

    is_playing = BooleanType(False)

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

    # def on_fullscreen(self, instance, value):
    #     Window.fullscreen = value
    #
    #     return super(StreamIesVideoPlayer, self).on_fullscreen(instance, value)

    def toggle_video_state(self):

        if self.is_playing:
            self.state = 'pause'
            self.is_playing = False

            self.ids.play_button.text = 'Play'
        else:
            self.state = 'play'
            self.is_playing = True

            self.ids.play_button.text = 'Pause'

    def toggle_fullscreen_state(self):
        self.on_fullscreen(True)

    def on_fullscreen(self, value):
        window = self.get_parent_window()
        if not window:
            Logger.warning('VideoPlayer: Cannot switch to fullscreen, '
                           'window not found.')
            if value:
                self.fullscreen = False
            return
        if not self.parent:
            Logger.warning('VideoPlayer: Cannot switch to fullscreen, '
                           'no parent.')
            if value:
                self.fullscreen = False
            return

        if value:
            self._fullscreen_state = state = {
                'parent': self.parent,
                'pos': self.pos,
                'size': self.size,
                'pos_hint': self.pos_hint,
                'size_hint': self.size_hint,
                'window_children': window.children[:]}

            # remove all window children
            for child in window.children[:]:
                window.remove_widget(child)

            # put the video in fullscreen
            if state['parent'] is not window:
                state['parent'].remove_widget(self)
            window.add_widget(self)

            # ensure the video widget is in 0, 0, and the size will be
            # reajusted
            self.pos = (0, 0)
            self.size = (100, 100)
            self.pos_hint = {}
            self.size_hint = (1, 1)
        else:
            state = self._fullscreen_state
            window.remove_widget(self)
            for child in state['window_children']:
                window.add_widget(child)
            self.pos_hint = state['pos_hint']
            self.size_hint = state['size_hint']
            self.pos = state['pos']
            self.size = state['size']
            if state['parent'] is not window:
                state['parent'].add_widget(self)