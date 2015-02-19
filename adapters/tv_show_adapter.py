from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton

from main import StreamIesApp


class TvShowAdapterButton(ListItemButton):

    adapter = None

    def on_menu_selection(self, index):
        series_name = self.adapter.data[index]

        app = StreamIesApp.get_running_app()
        widget = app.interface_manager.retrieve_active_widget()
        widget.show_episodes_in_list_view(series_name)


class TvShowAdapter(ListAdapter):

    def on_selection_change(self, *args):
        if self.cls.adapter is None:
            self.cls.adapter = self

        super(TvShowAdapter, self).on_selection_change(args)