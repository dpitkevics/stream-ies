from urllib2 import quote
import requests
from types import IntType, StringType
import urllib
import os
from PIL import Image

from lib.cache import cache_it
from settings import RESOURCES_DIR

try:
    from lxml import etree

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree

            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")


class SeriesSearcher:
    BASE_URL = 'http://services.tvrage.com/feeds/%s.php?%s=%s'

    def __init__(self):
        pass

    @cache_it
    def search_shows_by_query(self, query):
        xml = requests.get(self.BASE_URL % ('search', 'show', quote(query)))

        xmltree = etree.fromstring(xml.content)

        shows = []
        for element in xmltree:
            show_data = {}
            for show_row in element:
                show_data[show_row.tag] = show_row.text
            else:
                show_data['image_url'] = self.retrieve_image_url(show_data['link'])
                shows.append(show_data)

        return shows

    @cache_it
    def retrieve_image_url(self, show_url):
        request = requests.get(show_url)

        html = request.content
        html = html[html.index('http://images.tvrage.com/shows/'):]
        image_url = html[:html.index('\'>')]

        image_path = RESOURCES_DIR + "images" + os.sep + "uploads" + os.sep + image_url.replace('/', '_').replace(':', '_')
        urllib.urlretrieve(image_url, image_path)

        im = Image.open(image_path)
        image_path_png = image_path.replace('.jpg', '.png')
        im.save(image_path_png, 'PNG')

        im_small = Image.open(image_path_png)
        im_small.thumbnail((128, 128), Image.ANTIALIAS)
        im_small.save(image_path_png)

        os.remove(image_path)

        return image_path_png

    @cache_it
    def search_show_data_by_id(self, show_id):
        xml = requests.get(self.BASE_URL % ('episode_list', 'sid', quote(show_id)))

        xmltree = etree.fromstring(xml.content)

        show_data = []
        show_name = xmltree[0].text

        for element in xmltree:
            if element.tag == 'Episodelist':
                for season in element:
                    if season.tag == 'Season':
                        season_number = int(season.attrib['no'])

                        season_object = Season(show_title=show_name, season_number=season_number)
                        for episode in season:
                            episode_object = Episode(season_object)
                            for episode_row in episode:
                                if episode_row.tag == 'seasonnum':
                                    value = int(episode_row.text)
                                else:
                                    value = episode_row.text
                                setattr(episode_object, episode_row.tag, value)
                            else:
                                season_object.add_episode(episode_object)

                        show_data.append(season_object)
                        del season_object

        return show_data


class Season:
    show_title = StringType('')
    number = IntType(0)
    episodes = []

    def __init__(self, show_title, season_number):
        self.episodes = []
        self.show_title = show_title
        self.number = season_number

    def add_episode(self, episode):
        self.episodes.append(episode)


class Episode:
    epnum = IntType(0)
    seasonnum = IntType(0)
    prodnum = IntType(0)
    airdate = StringType('')
    link = StringType('')
    title = StringType('')

    season = None

    def __init__(self, season):
        self.season = season

    def __str__(self):
        return self.title