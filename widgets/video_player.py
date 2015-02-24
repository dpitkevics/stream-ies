import os
from types import BooleanType, StringType

from PySide.QtGui import QWidget, QPushButton, QGridLayout, QFileDialog, QDialog, QListWidget, QVBoxLayout
from PySide import QtCore
from PySide.phonon import Phonon

from lib.torrent_searcher import TorrentSearcher
from lib.downloader import Download, ThreadedDownload
from lib.thread import threads


class VideoPlayerWidget(QWidget):

    video_path = StringType('')

    is_video_download_started = BooleanType(False)
    is_video_download_done = BooleanType(False)

    is_playing = BooleanType(False)

    def __init__(self, episode, parent=None):
        super(VideoPlayerWidget, self).__init__(parent)

        self.episode = episode

        self.set_up_video_from_torrent()

        self.media = Phonon.MediaObject(self)

        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(400, 400)

        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)

        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)

        self.button_change_state = QPushButton('Play', self)
        self.button_mimes = QPushButton('Show Mimetypes', self)

        self.slider = Phonon.VolumeSlider(self)
        self.slider.setAudioOutput(self.audio)

        layout = QGridLayout(self)
        layout.addWidget(self.video, 0, 0, 1, 2)
        layout.addWidget(self.button_change_state, 1, 0)
        layout.addWidget(self.button_mimes, 1, 1)
        layout.addWidget(self.slider, 2, 0, 1, 2)
        layout.setRowStretch(0, 1)

        self.media.stateChanged.connect(self.handle_state_changed)
        self.button_change_state.clicked.connect(self.handle_button_choose)
        self.button_mimes.clicked.connect(self.handle_button_mimes)

    def set_up_video_from_torrent(self):
        torrent_searcher = TorrentSearcher()

        torrent_query = TorrentSearcher.parse_item_title(self.episode)

        result_torrents = torrent_searcher.make_search(torrent_query)

        real_torrent_href = result_torrents['href'][0]
        torrent_name = torrent_searcher.download_torrent(real_torrent_href)

        downloader = Download(torrent_name)

        self.video_path = downloader.retrieve_video_file_name()

        if os.path.isfile(self.video_path + ".st"):
            video_done_file_path = self.video_path + ".dn"
            if not os.path.isfile(video_done_file_path):
                threaded_download = ThreadedDownload(torrent_name=torrent_name, video_player=self)
                threaded_download.setName(torrent_name)
                threaded_download.setDaemon(True)
                threaded_download.start()
                threaded_download.join(0.1)

                threads.append(threaded_download)
            else:
                self.is_video_download_done = True
        else:
            # Start loading video
            threaded_download = ThreadedDownload(torrent_name=torrent_name, video_player=self)
            threaded_download.setName(torrent_name)
            threaded_download.setDaemon(True)
            threaded_download.start()
            threaded_download.join(0.1)

            threads.append(threaded_download)

    def set_video_source(self, video_path):
        self.media.setCurrentSource(Phonon.MediaSource(video_path))

    def handle_button_choose(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            self.media.play()

    def handle_button_mimes(self):
        dialog = MimeDialog(self)
        dialog.exec_()

    def handle_state_changed(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button_change_state.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.button_change_state.setText('Play')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ('ERROR: could not play: %s' % source)
                print ('  %s' % self.media.errorString())


class MimeDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Mimetypes')
        listbox = QListWidget(self)
        listbox.setSortingEnabled(True)
        backend = Phonon.BackendCapabilities
        listbox.addItems(backend.availableMimeTypes())
        layout = QVBoxLayout(self)
        layout.addWidget(listbox)
        self.resize(300, 500)