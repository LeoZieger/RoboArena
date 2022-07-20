from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia
from PyQt5.QtCore import QTimer, QThreadPool
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QDesktopWidget

import time
from os.path import exists
import copy

import Arena
from HumanControlledRobot import HumanControlledRobot
from AIControlledRobot import AIControlledRobot
import NameInput

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
UPDATE_TIME = 16


class RoboArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()
        self.arena.loadMap("Example_2Player")

        # hreadPool where each AI starts their Threads in
        self.threadpool = QThreadPool.globalInstance()

        self.robot = HumanControlledRobot(100, 50, 50, 0, 3)

        self.robotAI1 = AIControlledRobot(500, 500, 50,
                                          0, 2, copy.copy(self.arena),
                                          self.threadpool,
                                          n=1)
        self.robotAI2 = AIControlledRobot(800, 850, 50,
                                          0, 2, copy.copy(self.arena),
                                          self.threadpool,
                                          n=2)
        self.robotAI3 = AIControlledRobot(100, 850, 50,
                                          0, 2, copy.copy(self.arena),
                                          self.threadpool,
                                          n=3)

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

        self.bullets = []

        self.keys_pressed = set()

        # All objects where we want to enforce detection need to be in the scene
        self.scene = QGraphicsScene()
        self.scene.setBspTreeDepth(0)

        self.buildScene()

        self.initUI()
        self.initSoundrack()

        # Timer for ticks

        self.clock = 0
        self.clock_time = 0
        self.t_accumulator = 0

        self.timer = QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.tick)
        self.t_last = time.time_ns() // 1_000_000
        self.timer.start(1)

    def buildScene(self):
        # removing all 'old' items in the scene (with wrong idx)
        for it in self.scene.items():
            self.scene.removeItem(it)

        self.scene.setBspTreeDepth(0)

        self.arena.add_tiles_to_scene(self.scene)

        self.scene.addItem(self.robot)

        for ai_r in self.AI_robots:
            self.scene.addItem(ai_r)

        for b in self.bullets:
            self.scene.addItem(b)

        self.scene.addItem(self.mapborder_top)
        self.scene.addItem(self.mapborder_left)
        self.scene.addItem(self.mapborder_bottom)
        self.scene.addItem(self.mapborder_right)

    def getTimeInSec(self):

        return self.clock_time / 1000

    def getFPS(self):

        return int(self.clock / self.getTimeInSec())

    def initUI(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centerWindowOnScreen()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        # Painter for all Classes on main Window
        self.painter = QtGui.QPainter()

        self.show()

    def centerWindowOnScreen(self):
        outerRect = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        outerRect.moveCenter(centerOfScreen)
        self.move(outerRect.topLeft())

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
        delta_time = time.time_ns() // 1_000_000 - self.t_last

        self.clock += 1
        self.clock_time += delta_time
        self.t_last += delta_time
        self.t_accumulator += delta_time

        while self.t_accumulator > UPDATE_TIME:
            self.robot.reactToUserInput(self.keys_pressed)

            if self.robot.shooting:
                bullet = self.robot.createBullet()
                self.scene.addItem(bullet)
                self.bullets.append(bullet)

            self.robot.move()

            for ai_r in self.AI_robots:
                ai_r.move()
                ai_r.followPoints()
                ai_r.inform_brain(self.robot, ai_r)

            hit = False
            for b in self.bullets:
                b.trajectory()
                hit, o = b.isHittingObject()
                if hit:
                    self.bullets.remove(b)
                    # TODO: Impelemt Damage or something
                    self.buildScene()

            self.t_accumulator -= UPDATE_TIME

            self.update()

        # Here all the objetcs in the game are drawn to the canvas ------

        self.painter.begin(self.label.pixmap())
        self.arena.render(self.painter)
        self.robot.render(self.painter)
        self.painter.end()

        for ai_r in self.AI_robots:
            self.painter.begin(self.label.pixmap())
            ai_r.render(self.painter)
            self.painter.end()

        self.painter.begin(self.label.pixmap())
        for b in self.bullets:
            b.render(self.painter)
        self.painter.end()

        # ---------------------------------------------------------------

        if self.clock % 300 == 0:
            print(str(self.getFPS()) + " FPS")

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
