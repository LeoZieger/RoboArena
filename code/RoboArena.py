import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import Arena
import BasicRobot

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


class RoboArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.arena = Arena.Arena()
        self.robot = BasicRobot.BasicRobot(50, 50, 50, 10)

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def tick(self):
        self.painter = QtGui.QPainter(self.label.pixmap())
        self.arena.render(self.painter)
        self.robot.render(self.painter)
        self.painter.end()
        self.robot.x += 1
        self.update()


app = QtWidgets.QApplication(sys.argv)
window = RoboArena()
window.show()
app.exec_()
