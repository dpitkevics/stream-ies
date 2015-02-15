from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from lib.downloader import run_download


class StreamIesRoot(BoxLayout):
    pass


class StreamIesApp(App):
    @staticmethod
    def download_click():
        return run_download()


if __name__ == '__main__':
    StreamIesApp().run()