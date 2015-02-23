import sys

from PySide.QtGui import QApplication

from windows.main_window import MainWindow

__version__ = '0.0.1'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()