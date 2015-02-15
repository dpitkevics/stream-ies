import libtorrent as lt
import time
from os.path import expanduser

from settings import DOWNLOAD_DIR


def run_download():
    downloads_directory = expanduser("~") + "\\Downloads\\"

    torrent_name = downloads_directory + "[kickass.so]supernatural.s10e12.hdtv.x264.lol.ettv.torrent"

    ses = lt.session()
    ses.listen_on(6881, 6891)

    e = lt.bdecode(open(torrent_name, 'rb').read())
    info = lt.torrent_info(e)

    params = {
        'save_path': DOWNLOAD_DIR,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'ti': info
    }
    h = ses.add_torrent(params)
    h.set_sequential_download(True)

    print(h)

    while not h.is_seed():
        s = h.status()

        state_str = ['queued', 'checking', 'downloading metadata',
                     'downloading', 'finished', 'seeding', 'allocating']
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
              (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
               s.num_peers, state_str[s.state])

        time.sleep(1)