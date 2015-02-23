import sys

from PySide.QtGui import QMainWindow, QApplication

from lib.series_searcher import SeriesSearcher
from widgets.search_result_widget import SearchResultWidget

__version__ = '0.0.1'

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

        self.scroll_layout.setWidget(SearchResultWidget(shows))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()