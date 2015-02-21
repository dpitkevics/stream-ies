from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton

from main import StreamIesApp
from lib.torrent_searcher import TorrentSearcher


class TvShowAdapterButton(ListItemButton):

    adapter = None

    def on_menu_selection(self, index):
        self.show_episode_list(index)

    def show_episode_list(self, index):
        app = StreamIesApp.get_running_app()
        widget = app.interface_manager.retrieve_active_widget()
        widget.show_episodes_in_list_view(index+1)

    def show_episode(self, index):
        series_name = self.adapter.data[index]
        print(series_name)
        torrent_query = self.adapter.episode_search_strings[series_name]

        torrent_searcher = TorrentSearcher()
        result_torrents = torrent_searcher.make_search(torrent_query)

        real_torrent_href = result_torrents['href'][0]
        torrent_name = torrent_searcher.download_torrent(real_torrent_href)

        app = StreamIesApp.get_running_app()
        app.interface_manager.switch_form('video_player')

        video_player_widget = app.interface_manager.retrieve_active_widget()
        video_player_widget.ids.video_player.set_up_video_from_torrent(torrent_name)


class TvShowAdapter(ListAdapter):

    episode_search_strings = {}
    season_data = []

    def add_episode_search_string(self, item_title, episode):
        self.episode_search_strings[item_title] = self.parse_item_title(episode)

    @staticmethod
    def parse_item_title(episode):
        if episode.season.number < 10:
            season_number = '0' + str(episode.season.number)
        else:
            season_number = str(episode.season.number)

        if episode.seasonnum < 10:
            episode_number = '0' + str(episode.seasonnum)
        else:
            episode_number = str(episode.seasonnum)

        search_string = '%s S%sE%s' % (episode.season.show_title, season_number, episode_number)

        return search_string

    def on_selection_change(self, *args):
        if self.cls.adapter is None:
            self.cls.adapter = self

        super(TvShowAdapter, self).on_selection_change(args)