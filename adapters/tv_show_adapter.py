from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton

from lib.series_searcher import SeriesSearcher
from main import StreamIesApp


class TvShowAdapterButton(ListItemButton):

    adapter = None

    def on_menu_selection(self, index):
        series_name = self.adapter.data[index]

        # series_searcher = SeriesSearcher()
        # data = series_searcher.search_show_data_by_id(self.adapter.series_ids[series_name])

        app = StreamIesApp.get_running_app()
        widget = app.interface_manager.retrieve_active_widget()
        widget.show_episodes_in_list_view(series_name)
        # app.interface_manager.switch_form('tv_show')
        #
        # widget = app.interface_manager.retrieve_active_widget()
        # widget.set_show_data(data)
        # widget.update_list_view()


class TvShowAdapter(ListAdapter):

    def on_selection_change(self, *args):
        if self.cls.adapter is None:
            self.cls.adapter = self

        super(TvShowAdapter, self).on_selection_change(args)