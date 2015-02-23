from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPixmap, QCursor
from PySide import QtCore


class SearchResultWidget(QWidget):

    def __init__(self, main_window, shows):
        self.main_window = main_window
        self.shows = shows
        self.main_layout = QVBoxLayout()

        super(SearchResultWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        for show in self.shows:
            self.main_layout.addWidget(SearchResultItemWidget(self.main_window, show))

        self.setLayout(self.main_layout)


class SearchResultItemWidget(QWidget):

    def __init__(self, main_window, show_data):
        self.main_window = main_window
        self.show_data = show_data
        self.main_layout = QHBoxLayout()

        super(SearchResultItemWidget, self).__init__()

        self.setAutoFillBackground(True)
        self.init_ui()

    def init_ui(self):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(':hover { background-color: #ccc;}')
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        image_label = QLabel()
        image_label.setFixedWidth(128)
        pixmap = QPixmap(self.show_data['image_url'])

        image_label.setPixmap(pixmap)

        self.main_layout.addWidget(image_label)

        self.main_layout.addWidget(SearchResultItemDescriptionWidget(self.show_data))

        self.setLayout(self.main_layout)

    def mousePressEvent(self, event):
        self.main_window.search_result_item_click(self.show_data)


class SearchResultItemDescriptionWidget(QWidget):

    def __init__(self, show_data):
        self.show_data = show_data
        self.main_layout = QVBoxLayout()

        super(SearchResultItemDescriptionWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        show_title = QLabel(self.show_data['name'])

        show_title_font = show_title.font()
        show_title_font.setPointSize(14)
        show_title_font.setBold(True)

        show_title.setFont(show_title_font)

        show_status_label = QLabel("Status: %s" % self.show_data['status'])

        genres_label = QLabel("Genres: %s" % self.show_data['genres'])

        seasons_label = QLabel("Seasons: %s" % self.show_data['seasons'])

        self.main_layout.addWidget(show_title)
        self.main_layout.addWidget(show_status_label)
        self.main_layout.addWidget(genres_label)
        self.main_layout.addWidget(seasons_label)

        self.setLayout(self.main_layout)