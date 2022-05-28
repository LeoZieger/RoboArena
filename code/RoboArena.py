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

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        # self..arena.init_matrix_from_map("maps/test.json")
        # self.arena.init_matrix_from_map(map_filepath)
        self.arena.init_matrix_from_map_with_PROMT()

        self.robot = BasicRobot.BasicRobot(50, 50, 50, 10)

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        # Painter for all Classes on main Window
        self.painter = QtGui.QPainter(self.label.pixmap())

        # Timer for ticks
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def tick(self):
        self.arena.render(self.painter)
        self.robot.render(self.painter)

        self.robot.move()
        self.update()


app = QtWidgets.QApplication(sys.argv)
window = RoboArena()
window.show()
app.exec_()
