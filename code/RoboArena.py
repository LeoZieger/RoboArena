from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QThreadPool, QPoint
from PyQt5.QtGui import QPen, QFont, QFontDatabase, QIcon, QImage
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QDesktopWidget, \
                            QApplication
import time
import copy
import Arena
from HumanControlledRobot import HumanControlledRobot
from AIControlledRobot import AIControlledRobot
from BaseRobot import BaseRobot
import SpeedPowerup
import RapidfirePowerup
import HealthPowerup
import random
from Tile import TILE_WIDTH, Tile
from SoundFX import SoundFX
from PathUtil import getPath
import GameOverScreen

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
UPDATE_TIME = 16
# This is the number of Powerups getting spwnd
POWERUP_COUNT = 3
SPEED_RAPID_DURATION = 5


class RoboArena(QtWidgets.QMainWindow):
    def __init__(self, multiplayer, map_name, difficulty="Normal"):
        super().__init__()
        # Load font
        id = QFontDatabase.addApplicationFont(getPath("res", "PixeloidMono.ttf"))
        families = QFontDatabase.applicationFontFamilies(id)
        self.font = families[0]

        # Apply font
        QApplication.setFont(QFont(self.font))

        self.multiplayer = multiplayer

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        self.wasCollisionWithPowerup = False
        self.collectedPowerup = False

        self.arena.loadMap(map_name)

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

        # Robot of Player 1
        self.robot = HumanControlledRobot(75, 75,
                                          50, 0, 3,
                                          QImage(getPath("res", "blue_tank.png")),
                                          False)

        self.hum_robots = []
        self.AI_robots = []

        self.hum_robots.append(self.robot)

        if not self.multiplayer:
            texture = QImage()
            if difficulty == "Easy":
                texture = QImage(getPath("res", "green_tank.png"))
            elif difficulty == "Normal":
                texture = QImage(getPath("res", "yellow_tank.png"))
            elif difficulty == "Hard":
                texture = QImage(getPath("res", "red_tank.png"))

            self.robotAI1 = AIControlledRobot(875, 75, 50,
                                              0, 2,
                                              texture,
                                              copy.copy(self.arena),
                                              self.threadpool,
                                              n=1,
                                              difficulty=difficulty,)
            self.robotAI2 = AIControlledRobot(75, 875, 50,
                                              0, 2,
                                              texture,
                                              copy.copy(self.arena),
                                              self.threadpool,
                                              n=2,
                                              difficulty=difficulty)
            self.robotAI3 = AIControlledRobot(875, 875, 50,
                                              0, 2,
                                              texture,
                                              copy.copy(self.arena),
                                              self.threadpool,
                                              n=3,
                                              difficulty=difficulty)

            self.AI_robots.append(self.robotAI1)
            self.AI_robots.append(self.robotAI2)
            self.AI_robots.append(self.robotAI3)
        else:
            # Robot of Player 2
            self.robot2 = HumanControlledRobot(875, 875, 50, 180, 3,
                                               QImage(
                                                getPath("res", "red_tank.png")),
                                               False)
            self.hum_robots.append(self.robot2)

        BORDER_WIDTH = 10
        self.mapborder_top = QGraphicsRectItem(0, -BORDER_WIDTH,
                                               Arena.ARENA_WIDTH, BORDER_WIDTH)
        self.mapborder_left = QGraphicsRectItem(-BORDER_WIDTH, 0,
                                                BORDER_WIDTH, Arena.ARENA_HEIGHT)
        self.mapborder_bottom = QGraphicsRectItem(0, Arena.ARENA_HEIGHT,
                                                  Arena.ARENA_WIDTH, BORDER_WIDTH)
        self.mapborder_right = QGraphicsRectItem(Arena.ARENA_WIDTH, 0,
                                                 BORDER_WIDTH, Arena.ARENA_HEIGHT)

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
        SoundFX.initSoundrack(self, True)

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

        # rebuilding scene by scrap
        self.arena.add_tiles_to_scene(self.scene)

        for ai_r in self.AI_robots:
            self.scene.addItem(ai_r)
        for hum_r in self.hum_robots:
            self.scene.addItem(hum_r)

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
        self.setWindowTitle('RoboArena')
        self.setWindowIcon(QIcon(getPath("res", "blue_tank.png")))

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

    # Creates 1 of:
    # - speedpowerup/health/rapidfire
    # returns the powauP
    def generateRandomPowerup(self):
        self.randomTile = self.listOfNotCollidableTiles[
            random.randint(0, len(self.listOfNotCollidableTiles))
            ]

        n = random.randint(0, 2)
        if n == 0:
            self.newPowerup = SpeedPowerup.SpeedPowerup(
                                                    self.randomTile.x * TILE_WIDTH,
                                                    self.randomTile.y * TILE_WIDTH,
                                                    5,
                                                    False)
            return self.newPowerup

        if n == 1:
            self.newPowerup = HealthPowerup.HealthPowerup(
                                                    self.randomTile.x * TILE_WIDTH,
                                                    self.randomTile.y * TILE_WIDTH,
                                                    1,
                                                    False)
            return self.newPowerup

        if n == 2:
            self.newPowerup = RapidfirePowerup.RapidfirePowerup(
                                                    self.randomTile.x * TILE_WIDTH,
                                                    self.randomTile.y * TILE_WIDTH,
                                                    0.5,
                                                    False)
            return self.newPowerup

    # Appends a rnmd powerup into a list and adds a hitbox
    def spawnNewPowerup(self):
        temp = self.generateRandomPowerup()
        self.powerupList.append(temp)
        self.scene.addItem(temp)

    # Spawns the powerups and despawns them if collected
    def renderRandomTimePowerup(self):
        for powerUpIndex in self.powerupList:
            powerUpIndex.render(self.painter)
            if powerUpIndex.isCollected:
                self.powerupList.remove(powerUpIndex)
                self.spawnNewPowerup()
                SoundFX.initPwrUpSound(self)
                self.buildScene()

    # render the frames each tick
    def tick(self):
        delta_time = (time.time_ns() // 1_000_000) - self.t_last

        self.clock += 1
        self.clock_time += delta_time
        self.t_last += delta_time
        self.t_accumulator += delta_time

        # Update the positions of the entities only if a certain time has passed
        while self.t_accumulator > UPDATE_TIME:
            self.robot.reactToUserInput(self.keys_pressed)
            if self.multiplayer:
                self.robot2.reactToUserInput2(self.keys_pressed)

            # Moving and shooting for the AI and human players
            for hum_r in self.hum_robots:
                hum_r.move()

                if hum_r.shooting:
                    SoundFX.shootingSound(self)
                    bullet = hum_r.createBullet()
                    self.scene.addItem(bullet)
                    self.bullets.append(bullet)

            for ai_r in self.AI_robots:
                ai_r.move()
                ai_r.followPoints()
                ai_r.shootAtPoints()
                ai_r.inform_brain(self.robot, ai_r)

                if ai_r.shooting:
                    bullet = ai_r.createBullet()
                    if bullet is not None:
                        SoundFX.shootingEnemySound(self)
                        self.scene.addItem(bullet)
                        self.bullets.append(bullet)
                    self.buildScene()

            if not self.multiplayer:
                # Saves the time when a powerups is collected for duration
                # purpose
                if self.robot.collisionWithPowerup(self.scene):
                    self.timeWhenPowerupIsCollected = self.getTimeInSec()
                    self.collectedPowerup = True
                # if collected, resets effect after duration
                if self.collectedPowerup:
                    if self.timeWhenPowerupIsCollected + \
                            SPEED_RAPID_DURATION < self.getTimeInSec():
                        self.robot.resetSpeed()
                        self.robot.resetCooldown()
                        self.collectedPowerup = False

            else:
                # this is the same for 2 players
                for robos in self.hum_robots:
                    if robos.collisionWithPowerup(self.scene):
                        self.timeWhenPowerupIsCollected = self.getTimeInSec()
                        robos.collectedSpeedPowerup = True

                    if robos.collectedSpeedPowerup:
                        if self.timeWhenPowerupIsCollected + 5 < self.getTimeInSec():
                            robos.resetSpeed()
                            robos.resetCooldown()
                            robos.collectedSpeedPowerup = False

            self.checkForBullets()

            self.checkForDestroyedRobots()

            self.checkForWinCondition()

            self.t_accumulator -= UPDATE_TIME

            self.update()

        # Here all the objetcs in the game are drawn on the canvas
        self.painter.begin(self.label.pixmap())
        self.arena.render(self.painter)
        self.painter.end()

        self.painter.begin(self.label.pixmap())
        self.renderRandomTimePowerup()
        self.painter.end()

        for hum_r in self.hum_robots:
            self.painter.begin(self.label.pixmap())
            hum_r.render(self.painter)
            self.painter.end()

        for ai_r in self.AI_robots:
            self.painter.begin(self.label.pixmap())
            ai_r.render(self.painter)
            self.painter.end()

        self.painter.begin(self.label.pixmap())
        for b in self.bullets:
            b.render(self.painter)
        self.painter.end()

        # Update the fps approximately every second
        if self.clock_time > 1000:
            self.fps = int(self.clock / (self.clock_time / 1000))
            self.clock_time = 0
            self.clock = 0

        # Draw the fps counter
        self.painter.begin(self.label.pixmap())
        self.painter.setPen(QPen(Qt.white, 20, Qt.SolidLine))
        self.painter.setFont(QFont(self.font))
        self.painter.drawText(QPoint(10, 22), str(self.fps) + " FPS")
        self.painter.end()

    def checkForBullets(self):
        # checks for collision with bullets
        hit = False
        for b in self.bullets:
            b.trajectory()
            hit, o = b.isHittingObject()
            if hit:
                if isinstance(o, BaseRobot):  # Collision with Robots
                    o.takeDamage()
                    self.bullets.remove(b)

                    # Rebuild Scene after Bullet is deleted
                    self.buildScene()
                elif isinstance(o, Tile) or isinstance(o, QGraphicsRectItem):
                    if isinstance(o, Tile) and o.flyThrough:
                        continue

                    if not b.reflectedOnce:
                        b.reflect(o)
                    else:
                        self.bullets.remove(b)

                        # Rebuild Scene after Bullet is deleted
                        self.buildScene()

        self.removeBulletsOutOfBorder()

    def checkForDestroyedRobots(self):
        # removes already destroyed robots
        for hum_r in self.hum_robots:
            if hum_r.isDestroyed():
                self.hum_robots.remove(hum_r)
                self.buildScene()
                SoundFX.explosionSFX(self)

        for ai_r in self.AI_robots:
            if ai_r.isDestroyed():
                self.AI_robots.remove(ai_r)
                self.buildScene()
                ai_r.stopAllThreads()
                SoundFX.explosionSFX(self)

    def checkForWinCondition(self):
        # Checks if someone has already won aka. all robots are destroyed
        if self.multiplayer:
            if self.robot.isDestroyed():
                SoundFX.transitionSound(self)
                self.timer.stop()
                self.game_over = GameOverScreen.GameOverScreen("PLAYER 2 WINS!",
                                                               "yellow")
                self.close()
                SoundFX.initSoundrack(self, False)

            elif self.robot2.isDestroyed():
                SoundFX.transitionSound(self)
                self.timer.stop()
                self.game_over = GameOverScreen.GameOverScreen("PLAYER 1 WINS!",
                                                               "yellow")
                self.close()
                SoundFX.initSoundrack(self, False)

        else:
            if len(self.AI_robots) == 0:
                SoundFX.transitionSound(self)
                self.timer.stop()
                self.game_over = GameOverScreen.GameOverScreen("YOU WIN!",
                                                               "lime")
                self.close()
                SoundFX.initSoundrack(self, False)

            elif self.robot.isDestroyed():
                SoundFX.transitionSound(self)
                self.timer.stop()
                self.game_over = GameOverScreen.GameOverScreen("YOU LOSE!",
                                                               "orangered")
                self.close()
                SoundFX.initSoundrack(self, False)

    def removeBulletsOutOfBorder(self):
        # Removing Bullets that are out of bounds
        offset = 100  # Error how much it is allowed to be out of border
        for b in self.bullets:
            if (not (0 - offset <= b.x <= self.arena.arena_width + offset) or
               not (0 - offset <= b.y <= self.arena.arena_height + offset)):
                self.bullets.remove(b)

    def loadMap(self, name):
        self.arena.loadMap(name)

    def closeEvent(self, event):
        if not self.multiplayer:
            for ai_r in self.AI_robots:
                ai_r.stopAllThreads()
