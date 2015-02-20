from kivy.app import App

from types import DictionaryType, StringType

from kivy.uix.boxlayout import BoxLayout

from lib.thread import threads
from lib.torrent_searcher import TorrentSearcher
from lib.series_searcher import SeriesSearcher


class VideoPlayerWidget(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)


class MainWidget(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)


class SearchBarWidget(BoxLayout):

    torrent_searcher = None
    series_searcher = None

    def __init__(self, **kwargs):
        self.torrent_searcher = TorrentSearcher()
        self.series_searcher = SeriesSearcher()

        BoxLayout.__init__(self, **kwargs)

    def do_search(self, query):
        shows = self.series_searcher.search_shows_by_query(query)

        list_view = self.ids.search_result_list

        list_view.adapter.data = []
        for show in shows:
            list_view.adapter.data.extend((show['name'],))
            list_view.adapter.set_add_series_id(show['name'], show['showid'])

        list_view._trigger_reset_populate()


class TvShowWidget(BoxLayout):

    show_data = None

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

    def set_show_data(self, show_data):
        self.show_data = show_data

    def update_list_view(self):
        list_view = self.ids.show_season_list

        list_view.adapter.data = []
        for season in self.show_data:
            list_view.adapter.data.extend(('Season ' + str(season.number),))

        list_view._trigger_reset_populate()

    def show_episodes_in_list_view(self, season):
        season_number = int(season.replace('Season ', ''))

        season_object = [s for s in self.show_data if s.number is season_number][0]

        list_view = self.ids.show_season_list

        list_view.adapter.cls.on_menu_selection = list_view.adapter.cls.show_episode

        list_view.adapter.data = []
        for episode in season_object.episodes:
            item_title = '%s Season %d Episode %d - %s' % (season_object.show_title, season_object.number, episode.seasonnum, episode.title)
            list_view.adapter.data.extend((item_title,))
            list_view.adapter.add_episode_search_string(item_title, episode)

        list_view._trigger_reset_populate()


class InterfaceManager(BoxLayout):

    forms = DictionaryType({})
    active_widget_key = StringType('')
    active_widget = None
    loaded_kvs = []

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.forms = {}

        self.load_forms()

    def load_forms(self):
        self.add_form('main', MainWidget)
        self.add_form('video_player', VideoPlayerWidget)
        self.add_form('tv_show', TvShowWidget)

        self.switch_form('main')

    def add_form(self, key, form):
        self.forms[key] = form

    def switch_form(self, key):
        self.clear_widgets()

        self.active_widget_key = key

        class_object = self.forms[key]()

        self.add_widget(class_object)

        self.active_widget = class_object

        return self

    def retrieve_active_widget(self):
        return self.active_widget


class LayoutWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(LayoutWidget, self).__init__(**kwargs)


class StreamIesApp(App):
    interface_manager = None

    def build(self):
        layout_widget = LayoutWidget()

        self.interface_manager = layout_widget.ids.interface_manager

        return layout_widget

    def on_stop(self):
        for i in range(len(threads)):
            threads[i].stop()


if __name__ == '__main__':
    app = StreamIesApp()
    app.run()