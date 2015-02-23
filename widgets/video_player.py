from PySide.QtGui import QWidget, QPushButton, QGridLayout, QFileDialog, QDialog, QListWidget, QVBoxLayout
from PySide import QtCore
from PySide.phonon import Phonon

from lib.torrent_searcher import TorrentSearcher


class VideoPlayerWidget(QWidget):

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

        self.button_choose = QPushButton('Choose File', self)
        self.button_mimes = QPushButton('Show Mimetypes', self)

        self.slider = Phonon.VolumeSlider(self)
        self.slider.setAudioOutput(self.audio)

        layout = QGridLayout(self)
        layout.addWidget(self.video, 0, 0, 1, 2)
        layout.addWidget(self.button_choose, 1, 0)
        layout.addWidget(self.button_mimes, 1, 1)
        layout.addWidget(self.slider, 2, 0, 1, 2)
        layout.setRowStretch(0, 1)

        self.media.stateChanged.connect(self.handle_state_changed)
        self.button_choose.clicked.connect(self.handle_button_choose)
        self.button_mimes.clicked.connect(self.handle_button_mimes)

    def set_up_video_from_torrent(self):
        torrent_searcher = TorrentSearcher()

        torrent_query = TorrentSearcher.parse_item_title(self.episode)
        print(torrent_query)

        result_torrents = torrent_searcher.make_search(torrent_query)

        real_torrent_href = result_torrents['href'][0]
        torrent_name = torrent_searcher.download_torrent(real_torrent_href)

        print(torrent_name)

    def handle_button_choose(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.ExistingFile)

            if dialog.exec_() == QDialog.Accepted:
                path = dialog.selectedFiles()[0]
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()
            dialog.deleteLater()

    def handle_button_mimes(self):
        dialog = MimeDialog(self)
        dialog.exec_()

    def handle_state_changed(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button_choose.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.button_choose.setText('Choose File')
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