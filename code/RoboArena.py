import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

class RoboArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def tick(self):
        pass


app = QtWidgets.QApplication(sys.argv)
window = TestArena()
window.show()
app.exec_()
