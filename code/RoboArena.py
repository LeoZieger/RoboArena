from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer

import sys
from os.path import exists

import Arena
import BasicRobot
import NameInput

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


class RoboArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()
        

        self.arena.loadMap("MyFirstMap")
        self.robot = BasicRobot.BasicRobot(50, 50, 50, 10, 3)
        self.keys_pressed = set()



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

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def tick(self):
      
     

        self.robot.move(self.keys_pressed)
        self.painter = QtGui.QPainter(self.label.pixmap())
        self.arena.render(self.painter)
        self.robot.render(self.painter)
        self.painter.end()

        self.update()

    def loadMapByPrompt(self):
        popup = NameInput.NameInput()
        ok = popup.exec_()
        name = popup.textValue()

        while ok and (name == ""
                      or len(name.split(" ")) > 1
                      or not exists("maps/" + name + ".json")
                      ):
            popup.close()
            ok = popup.exec_()
            name = popup.textValue()
        popup.close()

        self.arena.loadMap(name)

    def loadMap(self, name):
        self.arena.loadMap(name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RoboArena()
    window.show()
    app.exec_()
