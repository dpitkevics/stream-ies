import sys
import urllib

from PySide.QtGui import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,  QLabel, QPixmap
from PySide import QtCore

from lib.series_searcher import SeriesSearcher

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

        widget = QWidget()
        grid_layout = QVBoxLayout(widget)

        for show in shows:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)

            image_label = QLabel()
            image_label.setFixedWidth(128)
            pixmap = QPixmap(show['image_url'])

            image_label.setPixmap(pixmap)

            show_description_widget = QWidget()
            show_description_layout = QVBoxLayout()

            show_title = QLabel(show['name'])

            show_title_font = show_title.font()
            show_title_font.setPointSize(14)
            show_title_font.setBold(True)

            show_title.setFont(show_title_font)

            show_status_label = QLabel("Status: %s" % show['status'])

            genres_label = QLabel("Genres: %s" % show['genres'])

            seasons_label = QLabel("Seasons: %s" % show['seasons'])

            show_description_layout.addWidget(show_title)
            show_description_layout.addWidget(show_status_label)
            show_description_layout.addWidget(genres_label)
            show_description_layout.addWidget(seasons_label)

            show_description_widget.setLayout(show_description_layout)

            item_layout.addWidget(image_label)
            item_layout.addWidget(show_description_widget)

            item_widget.setLayout(item_layout)

            grid_layout.addWidget(item_widget)

        widget.setLayout(grid_layout)

        self.scroll_layout.setWidget(widget)

        print(shows)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()