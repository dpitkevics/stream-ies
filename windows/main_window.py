from PySide.QtGui import QMainWindow

from lib.series_searcher import SeriesSearcher
from widgets.search_result_widget import SearchResultWidget
from widgets.show_result_widget import SeasonListWidget
from widgets.video_player import VideoPlayerWidget

from windows.streamies_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.search_button.clicked.connect(self.search_button_click)
        self.search_query.returnPressed.connect(self.search_button_click)

    def search_button_click(self):
        query = self.search_query.text()

        series_searcher = SeriesSearcher()
        shows = series_searcher.search_shows_by_query(query)

        self.scroll_layout.setWidget(SearchResultWidget(self, shows))

    def search_result_item_click(self, show_data):
        series_searcher = SeriesSearcher()
        data = series_searcher.search_show_data_by_id(show_data['showid'])

        self.scroll_layout.setWidget(SeasonListWidget(self, data))

    def episode_click(self, episode):
        video_player = VideoPlayerWidget(episode)

        self.scroll_layout.setWidget(video_player)
