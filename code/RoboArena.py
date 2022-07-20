from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QThreadPool, QPoint
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QDesktopWidget

import time
from os.path import exists
import copy

import Arena
from HumanControlledRobot import HumanControlledRobot
from AIControlledRobot import AIControlledRobot
import NameInput
import SpeedPowerup
import random
from Tile import TILE_WIDTH
from SoundFX import SoundFX

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
UPDATE_TIME = 16
# This is the number of Powerups getting spwnd
POWERUP_COUNT = 3


class RoboArena(QtWidgets.QMainWindow):
    def __init__(self, multiplayer):
        super().__init__()
        self.multiplayer = multiplayer

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        self.wasCollisionWithPowerup = False
        self.collectedPowerup = False

        self.arena.loadMap("Example_2Player")

        # This is where the Powerups are initialised
        self.listOfNotCollidableTiles = self.arena.listOfNotCollidableTiles()
        self.powerupList = []
        for p in range(POWERUP_COUNT):
            self.randomTile = self.listOfNotCollidableTiles[
                random.randint(0, len(self.listOfNotCollidableTiles))
                ]
            self.powerup = SpeedPowerup.SpeedPowerup(self.randomTile.x*TILE_WIDTH,
                                                     self.randomTile.y*TILE_WIDTH,
                                                     5,
                                                     False)
            self.powerupList.append(self.powerup)

        # ThreadPool where each AI starts their Threads in
        self.threadpool = QThreadPool.globalInstance()

        self.robot = HumanControlledRobot(100, 50, 50, 0, 3)

        if not self.multiplayer:

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

        else:

            self.robot2 = HumanControlledRobot(800, 850, 50, 0, 3)

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

        # Variables for renderRandomPowerUp
        self.leftIntBorder = 5
        self.rightIntBorder = 15

        self.initUI()
        SoundFX.initSoundrack(self)

        # Timer for ticks

        self.clock = 0
        self.clock_time = 0
        self.t_accumulator = 0
        self.fps = 0

        self.timer = QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.tick)
        self.t_last = time.time_ns() // 1_000_000
        self.t_start = time.time_ns() // 1_000_000
        self.timer.start(1)

    def buildScene(self):
        # removing all 'old' items in the scene (with wrong idx)
        for it in self.scene.items():
            self.scene.removeItem(it)

        self.scene.setBspTreeDepth(0)

        self.arena.add_tiles_to_scene(self.scene)

        self.scene.addItem(self.robot)

        if not self.multiplayer:
            for ai_r in self.AI_robots:
                self.scene.addItem(ai_r)
        else:
            self.scene.addItem(self.robot2)

        for b in self.bullets:
            self.scene.addItem(b)

        for i in self.powerupList:
            self.scene.addItem(i)

        self.scene.addItem(self.mapborder_top)
        self.scene.addItem(self.mapborder_left)
        self.scene.addItem(self.mapborder_bottom)
        self.scene.addItem(self.mapborder_right)

    def getTimeInSec(self):

        return int(((time.time_ns() // 1_000_000) - self.t_start) / 1000)

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

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def spawnNewPowerup(self):
        self.randomTile = self.listOfNotCollidableTiles[
            random.randint(0, len(self.listOfNotCollidableTiles))
            ]
        self.newPowerup = SpeedPowerup.SpeedPowerup(self.randomTile.x * TILE_WIDTH,
                                                    self.randomTile.y * TILE_WIDTH,
                                                    5,
                                                    False)
        self.powerupList.append(self.newPowerup)
        self.scene.addItem(self.newPowerup)

        # Takes 2 numbers, spawns all powerups after a
        # random time between these 2 numbers
    def renderRandomTimePowerup(self, leftIntBorder, rightIntBorder):
        if self.getTimeInSec() > random.randint(leftIntBorder, rightIntBorder):
            # this prevents the powerup from respawning over and over again
            self.leftIntBorder = 0
            self.rightIntBorder = 0
            for powerUpIndex in self.powerupList:
                powerUpIndex.render(self.painter)
                if powerUpIndex.isCollected:
                    self.powerupList.remove(powerUpIndex)
                    self.spawnNewPowerup()
                    SoundFX.initPwrUpSound(self)
                    QGraphicsScene.removeItem(self.scene, powerUpIndex)

    def tick(self):
        delta_time = (time.time_ns() // 1_000_000) - self.t_last

        self.clock += 1
        self.clock_time += delta_time
        self.t_last += delta_time
        self.t_accumulator += delta_time

        while self.t_accumulator > UPDATE_TIME:
            self.robot.reactToUserInput(self.keys_pressed)
            self.robot.move()

            if self.robot.shooting:
                bullet = self.robot.createBullet()
                self.scene.addItem(bullet)
                self.bullets.append(bullet)

            if self.multiplayer and self.robot2.shooting:
                bullet = self.robot.createBullet()
                self.scene.addItem(bullet)
                self.bullets.append(bullet)

            if not self.multiplayer:
                for ai_r in self.AI_robots:
                    ai_r.move()
                    ai_r.followPoints()
                    ai_r.inform_brain(self.robot, ai_r)
            else:
                self.robot2.move()
                self.robot2.reactToUserInput2(self.keys_pressed)

            if self.robot.collisionWithPowerup(self.scene):
                self.timeWhenPowerupIsCollected = self.getTimeInSec()
                self.collectedPowerup = True

            if self.collectedPowerup:
                if self.timeWhenPowerupIsCollected + 5 < self.getTimeInSec():
                    self.robot.resetSpeed()
                    self.collectedPowerup = False

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
        self.renderRandomTimePowerup(self.leftIntBorder, self.rightIntBorder)

        self.painter.end()

        if not self.multiplayer:
            for ai_r in self.AI_robots:
                self.painter.begin(self.label.pixmap())
                ai_r.render(self.painter)
                self.painter.end()

        else:
            self.painter.begin(self.label.pixmap())
            self.robot2.render(self.painter)
            self.painter.end()

        self.painter.begin(self.label.pixmap())
        for b in self.bullets:
            b.render(self.painter)
        self.painter.end()

        # ---------------------------------------------------------------

        if self.clock_time > 1000:
            self.fps = int(self.clock / (self.clock_time / 1000))
            self.clock_time = 0
            self.clock = 0

        self.painter.begin(self.label.pixmap())
        self.painter.setPen(QPen(Qt.white, 10, Qt.SolidLine))
        self.painter.setFont(QFont("Verdana", 12))
        self.painter.drawText(QPoint(10, 22), str(self.fps) + " FPS")
        self.painter.end()

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
        if not self.multiplayer:
            for ai_r in self.AI_robots:
                ai_r.stopAllThreads()
