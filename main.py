import sys
from PySide import QtGui

app = QtGui.QApplication(sys.argv)

wid = QtGui.QWidget()
wid.resize(250, 150)
wid.setWindowTitle('Stream-Ies')
wid.show()

sys.exit(app.exec_())