from PySide.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCursor
from PySide import QtCore


class SeasonListWidget(QWidget):

    def __init__(self, main_window, show_data):
        self.main_window = main_window
        self.show_data = show_data
        self.main_layout = QVBoxLayout()

        super(SeasonListWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        for season in self.show_data:
            season_label = QLabel('Season %s' % season.number)

            season_label_font = season_label.font()
            season_label_font.setPointSize(14)
            season_label_font.setBold(True)

            season_label.setFont(season_label_font)

            self.main_layout.addWidget(season_label)
            self.main_layout.addWidget(EpisodeListWidget(self.main_window, self.main_layout, season))

        self.setLayout(self.main_layout)


class EpisodeListWidget(QWidget):

    def __init__(self, main_window, layout, season):
        self.main_window = main_window
        self.main_layout = layout
        self.season = season

        super(EpisodeListWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        for episode in self.season.episodes:
            self.main_layout.addWidget(EpisodeWidget(self.main_window, episode))


class EpisodeWidget(QWidget):

    def __init__(self, main_window, episode):
        self.main_window = main_window
        self.episode = episode
        self.main_layout = QHBoxLayout()

        super(EpisodeWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(':hover { background-color: #ccc;}')
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        season_label = QLabel("Episode %s" % self.episode.seasonnum)
        self.main_layout.addWidget(season_label)
        episode_label = QLabel(self.episode.title)

        self.main_layout.addWidget(episode_label)

        self.setLayout(self.main_layout)

    def mousePressEvent(self, event):
        self.main_window.episode_click(self.episode)