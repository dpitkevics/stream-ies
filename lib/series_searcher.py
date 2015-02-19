from urllib2 import quote
import requests
from types import IntType, StringType, DictionaryType

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

    def search_shows_by_query(self, query):
        xml = requests.get(self.BASE_URL % ('search', 'show', quote(query)))

        xmltree = etree.fromstring(xml.content)

        shows = []
        for element in xmltree:
            show_data = {}
            for show_row in element:
                show_data[show_row.tag] = show_row.text
            else:
                shows.append(show_data)

        return shows

    def search_show_data_by_id(self, show_id):
        xml = requests.get(self.BASE_URL % ('episode_list', 'sid', quote(show_id)))

        xmltree = etree.fromstring(xml.content)

        show_data = []
        for element in xmltree:
            if element.tag == 'Episodelist':
                for season in element:
                    if season.tag == 'Season':
                        season_number = int(season.attrib['no'])

                        season_object = Season(season_number=season_number)
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
    number = IntType(0)
    episodes = []

    def __init__(self, season_number):
        self.episodes = []
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