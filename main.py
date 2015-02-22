import sys
import urllib

from PySide.QtGui import QMainWindow, QApplication, QWidget, QGridLayout, QHBoxLayout, QPushButton, QLabel, QImage, QPixmap
from PySide import QtCore

from lib.series_searcher import SeriesSearcher

__version__ = '0.0.1'

from windows.streamies_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.search_button.clicked.connect(self.search_button_click)

    def search_button_click(self):
        query = self.search_query.text()

        series_searcher = SeriesSearcher()
        shows = series_searcher.search_shows_by_query(query)

        widget = QWidget()
        grid_layout = QGridLayout(widget)

        for show in shows:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)

            image_label = QLabel()
            pixmap = QPixmap(show['image_url'])

            image_label.setPixmap(pixmap)

            button = QPushButton(show['name'])

            item_layout.addWidget(image_label)
            item_layout.addWidget(button)

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