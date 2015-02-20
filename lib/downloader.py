import libtorrent as lt
import time
import sys
import os

from settings import DOWNLOAD_DIR, VIDEO_FORMATS

import threading


class Download:
    """
    Download class for downloading torrent files
    """

    torrent_name = None
    video_player = None

    session = None
    handle = None
    info = None

    def __init__(self, torrent_name, video_player=None):
        """
        Init method for Download class - sets local class variables passed in __init__

        :param torrent_name: string
        :param video_player: StreamIesVideoPlayer
        :return:
        """

        self.torrent_name = torrent_name
        self.video_player = video_player

    def set_handle(self):
        """
        Creates torrent session on specified ports.
        Retrieves torrent info and passes next to torrent handle which is prioritized to download pieces in sequence
        :return:
        """

        ses = lt.session()
        ses.listen_on(6881, 6891)

        self.session = ses

        self.info = self.retrieve_torrent_info()
        h = ses.add_torrent({'ti': self.info, 'save_path': DOWNLOAD_DIR})
        h.prioritize_pieces(7)
        h.set_sequential_download(True)

        self.handle = h

    def retrieve_torrent_info(self):
        """
        Returns information of torrent

        :return: libtorrent.torrent_info
        """

        return lt.torrent_info(self.torrent_name)

    def retrieve_video_file_path(self):
        """
        Searches torrent information for directory where all torrents will be downloaded

        :return: string
        """

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
        """
        Retrieves video file name which is saved in local pc
        Searching is through specified directory moving through all the files

        :return: string
        """

        torrent_dir = self.retrieve_video_file_path()

        current_torrent_dir = DOWNLOAD_DIR + torrent_dir

        if not os.path.isdir(current_torrent_dir) or current_torrent_dir == DOWNLOAD_DIR:
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
        """
        Makes actual download of torrent files

        :return:
        """

        # Sets handle if is needed
        if self.handle is None:
            self.set_handle()

        # Looping while handle is not seeding but downloading
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

            # Prints current torrent status
            print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                  (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                   s.num_peers, state_str[s.state]),
            sys.stdout.flush()

            video_path = self.retrieve_video_file_name()
            # Checking if we need to create .st file
            if not os.path.isfile(video_path + ".st"):
                # Checking if we are able to create .st file
                if (s.progress * 100) > 1:
                    open(video_path + ".st", 'a').close()

                    # Setting new video data for our player
                    self.video_player.is_video_download_started = True
                    self.video_player.video_path = video_path
                    self.video_player.set_video_source(video_path)

            time.sleep(1)

        # Download is finished, set new video data for our player and make a .dn file
        self.video_player.is_video_download_done = True
        video_path = self.retrieve_video_file_name()
        open(video_path + ".dn", 'a').close()


class ThreadedDownload(threading.Thread, Download):
    """
    Makes basic download to a threaded download so it will not freeze all program, but will run in background
    """

    def __init__(self, torrent_name, video_player=None):
        """
        Initializes both parent classes as well as creating stop event to stop thread when needed

        :param torrent_name: string
        :param video_player: StreamIesVideoPlayer
        :return:
        """

        threading.Thread.__init__(self)
        Download.__init__(self, torrent_name, video_player)
        self._stop = threading.Event()

    def run(self):
        """
        Starts thread with downloading torrent

        :return:
        """

        self.download_torrent()

    def download_torrent(self):
        """
        Performs actual download by calling parent class download method
        After download, stops thread

        :return:
        """

        super(ThreadedDownload, self).download_torrent()

        self.stop()

    def stop(self):
        """
        Stops current thread

        :return:
        """

        self._stop.set()