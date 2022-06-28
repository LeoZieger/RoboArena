from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem


from os.path import exists

import Arena
from HumanControlledRobot import HumanControlledRobot
from AIControlledRobot import AIControlledRobot
import NameInput
import BasePowerup
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
RANDOM_X = random.randint(100, 900)
RANDOM_Y = RANDOM_X



class RoboArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        self.arena.loadMap("Example_2Player")

        self.robot = HumanControlledRobot(100, 50, 50, 0, 3)

        # HIER LASSE JUNGE
        self.powerup = BasePowerup.BasePowerup(RANDOM_X, RANDOM_Y, 20)

        self.robotAI1 = AIControlledRobot(500, 500, 50, 0, 2, n=1)
        self.robotAI2 = AIControlledRobot(800, 850, 50, 0, 2, n=2)
        self.robotAI3 = AIControlledRobot(100, 850, 50, 0, 2, n=3)

        self.AI_robots = []
        self.AI_robots.append(self.robotAI1)
        self.AI_robots.append(self.robotAI2)
        self.AI_robots.append(self.robotAI3)

        self.mapborder_top = QGraphicsRectItem(0, 0,
                                               Arena.ARENA_HEIGHT, 5)
        self.mapborder_left = QGraphicsRectItem(-5, 0,
                                                5, Arena.ARENA_HEIGHT)
        self.mapborder_bottom = QGraphicsRectItem(0, Arena.ARENA_HEIGHT,
                                                  Arena.ARENA_WIDTH, 5)
        self.mapborder_right = QGraphicsRectItem(Arena.ARENA_WIDTH, 0,
                                                 5, Arena.ARENA_HEIGHT)

        self.keys_pressed = set()

        # All objects where we want to enforce detection need to be in the scene
        self.scene = QGraphicsScene()

        self.scene = self.arena.add_tiles_to_scene(self.scene)
        self.scene.addItem(self.robot)
        self.scene.addItem(self.mapborder_top)
        self.scene.addItem(self.mapborder_left)
        self.scene.addItem(self.mapborder_bottom)
        self.scene.addItem(self.mapborder_right)
        self.scene.addItem(self.powerup)

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

        self.robot.move(self.scene)
        self.robot.reactToUserInput(self.keys_pressed)
#       self.robot.collisionWithPowerup(self.powerup)

        for ai_r in self.AI_robots:
            ai_r.move(QGraphicsScene())
            ai_r.followPoints()
            ai_r.inform_brain(self.arena, self.robot)

        # Here all the objetcs in the game are drawn to the canvas ------

        self.painter.begin(self.label.pixmap())
        self.arena.render(self.painter)
        self.robot.render(self.painter)
        self.powerup.render(self.painter)
        self.painter.end()

        for ai_r in self.AI_robots:
            self.painter.begin(self.label.pixmap())
            ai_r.render(self.painter)
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

    def closeEvent(self, event):
        print("Alle Threads werden auf stop gesetzt!")
        for ai_r in self.AI_robots:
            ai_r.stopAllThreads()
