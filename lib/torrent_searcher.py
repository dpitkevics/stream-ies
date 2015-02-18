from bs4 import BeautifulSoup
import os
import re
import requests
from requests.exceptions import RequestException
import subprocess
import sys
import tabulate


class OutColors:
    DEFAULT = '\033[0m'
    BW = '\033[1m'
    LG = '\033[0m\033[32m'
    LR = '\033[0m\033[31m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


class TorrentSearcher:
    host_url = 'http://kickass.to/usearch/'

    def __init__(self):
        pass

    def download_torrent(self, url):
        fname = os.getcwd() + '/' + url.split('title=')[-1] + '.torrent'
        # http://stackoverflow.com/a/14114741/1302018
        try:
            r = requests.get(url, stream=True)
            with open(fname, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        except RequestException as e:
            print('\n' + OutColors.LR + str(e))
            sys.exit(1)

        return fname

    def make_search(self, query):
        url = self.host_url + query + "/"

        try:
            cont = requests.get(url)
        except RequestException as e:
            raise Exception("Connection error")

        if not re.findall(r'Download torrent file', str(cont.content)):
            raise TorrentsNotFoundException("Torrents not found")
        else:
            soup = BeautifulSoup(cont.content)

        al = [s.get_text() for s in soup.find_all('td', {'class':'center'})]

        href = [a.get('href') for a in soup.find_all('a', {'title':'Download torrent file'})]
        size = [t.get_text() for t in soup.find_all('td', {'class':'nobr'}) ]
        title = [ti.get_text() for ti in soup.find_all('a', {'class':'cellMainLink'})]
        age = al[2::5]
        seeders = al[3::5]
        leechers = al[4::5]

        print(size)


class TorrentsNotFoundException(Exception):
    pass