from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton

from lib.series_searcher import SeriesSearcher


class SearcherAdapterButton(ListItemButton):

    adapter = None

    def on_menu_selection(self, index):
        series_name = self.adapter.data[index]

        series_searcher = SeriesSearcher()
        series_searcher.search_show_data_by_id(self.adapter.series_ids[series_name])


class SearcherAdapter(ListAdapter):

    series_ids = {}

    def set_add_series_id(self, key, value):
        self.series_ids[key] = value

    def on_selection_change(self, *args):
        if self.cls.adapter is None:
            self.cls.adapter = self

        super(SearcherAdapter, self).on_selection_change(args)