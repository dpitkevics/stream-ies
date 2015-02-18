from kivy.app import App

from types import DictionaryType, StringType

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from lib.thread import threads
from lib.kv import KvLoader
from lib.torrent_searcher import TorrentSearcher


class VideoPlayerWidget(BoxLayout, KvLoader):

    def __init__(self, **kwargs):
        KvLoader.__init__(self)
        BoxLayout.__init__(self, **kwargs)


class MainWidget(BoxLayout, KvLoader):

    def __init__(self, **kwargs):
        KvLoader.__init__(self)
        BoxLayout.__init__(self, **kwargs)

        torrent_searcher = TorrentSearcher()
        torrent_searcher.make_search("supernatural")


class InterfaceManager(BoxLayout):

    forms = DictionaryType({})
    active_widget_key = StringType('')

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.forms = {}

    def add_form(self, key, form):
        self.forms[key] = form

    def switch_form(self, key):
        self.clear_widgets()
        if self.active_widget_key != '':
            Builder.unload_file('kv/' + self.forms[self.active_widget_key].__class__.__name__)

        self.active_widget_key = key

        class_object = self.forms[key]()
        self.add_widget(class_object)

        return self


class StreamIesApp(App):
    interface_manager = None

    def build(self):
        self.interface_manager = InterfaceManager(orientation='vertical')
        self.interface_manager.add_form('main', MainWidget)
        self.interface_manager.add_form('video_player', VideoPlayerWidget)

        return self.interface_manager.switch_form('main')

    def on_stop(self):
        for i in range(len(threads)):
            threads[i].stop()


if __name__ == '__main__':
    StreamIesApp().run()