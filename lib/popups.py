from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class VideoPlayerPopup(Popup):
    def __init__(self, **kwargs):
        popup_layout = BoxLayout(orientation='vertical')

        popup_content = Label(text='Video is now initializing, please wait a little')
        popup_button = Button(text='Close', height='40dp', size_hint_y=None)
        popup_button.bind(on_press=self.dismiss)

        popup_layout.add_widget(popup_content)
        popup_layout.add_widget(popup_button)

        self.title = 'Video initializing...'
        self.content = popup_layout
        self.size = (200, 200)
        self.auto_dismiss = False

        super(VideoPlayerPopup, self).__init__(**kwargs)