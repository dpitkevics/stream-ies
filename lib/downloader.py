import libtorrent as lt
import time
import sys
import os

from settings import DOWNLOAD_DIR

import threading


class ThreadedDownload(threading.Thread):
    torrent_name = None
    video_player = None

    session = None
    handle = None
    info = None

    def __init__(self, torrent_name, video_player=None):
        super(ThreadedDownload, self).__init__()
        self._stop = threading.Event()

        self.torrent_name = torrent_name
        self.video_player = video_player

    def set_handle(self):
        ses = lt.session()
        ses.listen_on(6881, 6891)

        self.session = ses

        self.info = lt.torrent_info(self.torrent_name)
        h = ses.add_torrent({'ti': self.info, 'save_path': DOWNLOAD_DIR})
        h.prioritize_pieces(7)
        h.set_sequential_download(True)

        self.handle = h

    def run(self):
        self.download_torrent()

    def download_torrent(self):
        if self.handle is None:
            self.set_handle()

        video_path = DOWNLOAD_DIR + os.sep + "Supernatural S10E04 HDTV x264-LOL[ettv]" + os.sep + "supernatural.1004.hdtv-lol.mp4"

        while not self.handle.is_seed():
            s = self.handle.status()

            state_str = ['queued',
                         'checking',
                         'downloading metadata',
                         'downloading',
                         'finished',
                         'seeding',
                         'allocating',
                         'checking fastresume']
            print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                  (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                   s.num_peers, state_str[s.state]),
            sys.stdout.flush()

            if not os.path.isfile(video_path + ".st"):
                if (s.progress * 100) > 1:
                    open(video_path + ".st", 'a').close()

                    self.video_player.source = video_path

            time.sleep(1)

        open(video_path + ".dn", 'a').close()
        self._stop.set()
