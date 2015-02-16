import libtorrent as lt
import time
import sys
import os

from settings import DOWNLOAD_DIR, VIDEO_FORMATS

import threading


class Download:
    torrent_name = None
    video_player = None

    session = None
    handle = None
    info = None

    def __init__(self, torrent_name, video_player=None):
        self.torrent_name = torrent_name
        self.video_player = video_player

    def set_handle(self):
        ses = lt.session()
        ses.listen_on(6881, 6891)

        self.session = ses

        self.info = self.retrieve_torrent_info()
        h = ses.add_torrent({'ti': self.info, 'save_path': DOWNLOAD_DIR})
        h.prioritize_pieces(7)
        h.set_sequential_download(True)

        self.handle = h

    def retrieve_torrent_info(self):
        return lt.torrent_info(self.torrent_name)

    def retrieve_video_file_path(self):
        info = self.retrieve_torrent_info()

        dir_name = ''

        for f in info.files():
            file_path = f.path
            file_path_parts = file_path.split(os.sep)

            if len(file_path_parts) > 1:
                dir_name = file_path_parts[0]
            else:
                dir_name = ''

        return dir_name

    def retrieve_video_file_name(self):
        torrent_dir = self.retrieve_video_file_path()

        current_torrent_dir = DOWNLOAD_DIR + torrent_dir
        if not os.path.isdir(current_torrent_dir):
            video_path = DOWNLOAD_DIR
        else:
            matches = []
            for root, dirnames, filenames in os.walk(current_torrent_dir):
                matches.extend(os.path.join(root, filename) for filename in filenames if filename.lower().endswith(VIDEO_FORMATS))

            if len(matches) > 1:
                raise Exception("More than one video matched")

            video_path = matches[0]

        return video_path

    def download_torrent(self):
        if self.handle is None:
            self.set_handle()

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

            video_path = self.retrieve_video_file_name()
            if not os.path.isfile(video_path + ".st"):
                if (s.progress * 100) > 1:
                    open(video_path + ".st", 'a').close()

                    self.video_player.source = video_path

            time.sleep(1)

        video_path = self.retrieve_video_file_name()
        open(video_path + ".dn", 'a').close()


class ThreadedDownload(threading.Thread, Download):
    def __init__(self, torrent_name, video_player=None):
        threading.Thread.__init__(self)
        Download.__init__(self, torrent_name, video_player)
        self._stop = threading.Event()

    def run(self):
        self.download_torrent()

    def download_torrent(self):
        super(ThreadedDownload, self).download_torrent()

        self.stop()

    def stop(self):
        self._stop.set()