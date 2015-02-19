from urllib2 import quote
import requests

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