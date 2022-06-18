from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsScene


from os.path import exists

import Arena
import BasicRobot
import BasicAIRobot
import NameInput

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


class RoboArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        self.arena.loadMap("Example_2Player")

        self.robot = BasicRobot.BasicRobot(100, 50, 50, 0, 3)
        self.robotAI1 = BasicAIRobot.BasicAIRobot(850, 50, 50, 180, 2)
        self.robotAI2 = BasicAIRobot.BasicAIRobot(800, 850, 50, 0, 2)
        self.robotAI3 = BasicAIRobot.BasicAIRobot(100, 850, 50, 0, 2)
        self.keys_pressed = set()

        self.scene = QGraphicsScene()
        self.scene = self.arena.add_tiles_to_scene(self.scene)
        self.scene.addItem(self.robot)

        self.initUI()
        self.initSoundrack()

        # Timer for ticks
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def initUI(self):
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        # Painter for all Classes on main Window
        self.painter = QtGui.QPainter()

        self.show()

    def initSoundrack(self):
        # This is the part where we can setup the soundtrack
        soundtrack = 'RoboArena_Soundtrack_Demo.wav'
        self.sound = QtMultimedia.QSoundEffect()
        self.sound.setSource(QtCore.QUrl.fromLocalFile(soundtrack))
        self.sound.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
        self.sound.setVolume(0.3)    # Choose a value between 0 and 1
        self.sound.play()

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def tick(self):
        self.robotAI1.moveAI1(self.keys_pressed)
        self.robotAI2.moveAI2(self.keys_pressed)
        self.robotAI3.moveAI3(self.keys_pressed)
        self.robot.move(self.keys_pressed, self.scene)

        # Here all the objetcs in the game are drawn to the canvas ------

        self.painter.begin(self.label.pixmap())
        self.arena.render(self.painter)
        self.robot.render(self.painter)
        self.painter.end()

        self.painter.begin(self.label.pixmap())
        self.robotAI1.render(self.painter)
        self.painter.end()

        self.painter.begin(self.label.pixmap())
        self.robotAI2.render(self.painter)
        self.painter.end()

        self.painter.begin(self.label.pixmap())
        self.robotAI3.render(self.painter)
        self.painter.end()

        # ---------------------------------------------------------------

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
