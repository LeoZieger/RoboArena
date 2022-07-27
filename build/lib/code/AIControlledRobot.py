import numpy as np
from BaseRobot import BaseRobot
import Brain
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsRectItem
from Bullet import Bullet
from SpeedPowerup import SpeedPowerup
import time
from Tile import Tile
from Arena import ARENA_WIDTH, ARENA_HEIGHT


class AIControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed, texture,
                 arena, pool, n=0, difficulty="Normal"):
        BaseRobot.__init__(self, x, y, r, alpha, speed, texture)
        self.n = n

        self.brain = Brain.Brain(self.n, arena, difficulty=difficulty)

        self.connectBainToSlots()

        self.threadpool = pool

        self.brain.setAutoDelete(False)
        self.threadpool.start(self.brain)  # Brain gets added to gloabl Threadpool

        self.texture = texture

        self.diff_speed = 1  # Difficult specific speed of robots

        self.handleDifficulty(difficulty)

        self.point_queue = []
        self.shoot_queue = []

    def handleDifficulty(self, difficulty):
        if difficulty == "Hard":
            self.cooldown = 3
            self.diff_speed = 3
        elif difficulty == "Normal":
            self.cooldown = 3
            self.diff_speed = 2.5
        elif difficulty == "Easy":
            self.cooldown = 4
            self.diff_speed = 2

    def connectBainToSlots(self):
        self.brain.signals.finished.connect(self.setThreadToFinished)

        self.brain.signals.informAboutNextPointToMove.connect(
                                                        self.setNewPointToMoveTo)
        self.brain.signals.informToClearQueueMovement.connect(
                                                        self.clearFollowPointQueue)

        self.brain.signals.informAboutNextPointToShoot.connect(
                                                        self.setNewPointToShootAt)
        self.brain.signals.informToClearQueueShooting.connect(
                                                        self.clearShootingQueue)

    def inform_brain(self, human_player, robo_player):
        self.brain.inform_brain(human_player, robo_player)

    def setNewPointToMoveTo(self, new_point):
        self.point_queue.append(new_point)

    def setNewPointToShootAt(self, new_point):
        self.shoot_queue.append(new_point)

    def followPoints(self):
        if len(self.point_queue) > 0:
            self.speed = self.diff_speed

            if self.hasReachedPoint(self.point_queue[0]):
                self.point_queue.pop(0)
            else:
                new_alpha = self.calculateAlphaToReachPoint(self.point_queue[0])
                self.alpha = new_alpha
        else:
            self.speed = 0

    def shootAtPoints(self):
        if len(self.shoot_queue) > 0:
            if time.time() - self.canShootAgainAt > 0:
                self.shooting = True
                self.canShootAgainAt = time.time() + self.cooldown
            else:
                self.shooting = False
        else:
            self.shooting = False

    def createBullet(self):
        x_pos, y_pos = self.calculateBulletStartPos()

        # Turning around to point where to shoot at
        if len(self.shoot_queue) > 0:
            point = self.shoot_queue[0]
            new_alpha = self.calculateAlphaToReachPoint(point)
            self.alpha = new_alpha
            self.shoot_queue.pop(0)

            # Ai only shoots if there is no obstacle in the way
            if self.hasClearShot(point):
                return Bullet(x_pos,
                              y_pos,
                              self.getVector(),
                              14,
                              10)

    def hasClearShot(self, point):
        # Simulating 'around and shooting a dummy bullet'
        old_apha = self.alpha
        new_alpha = self.calculateAlphaToReachPoint(point)
        self.alpha = new_alpha
        v = self.getVector()
        self.alpha = old_apha

        step_size = 1
        offset = 40

        x, y = self.calculateBulletStartPos()

        dummy_obj = QGraphicsRectItem(x, y, 1, 1)
        dummy_obj.setRect(x, y, 1, 1)

        self.scene().addItem(dummy_obj)

        d_x = point.x() - x
        d_y = point.y() - y

        dist = np.sqrt(np.power(d_x, 2) + np.power(d_y, 2))

        while(dist > offset and
              0 <= x <= ARENA_WIDTH and 0 <= y <= ARENA_HEIGHT):
            x += v[0] * step_size
            y += v[1] * step_size

            dummy_obj.setRect(x, y, 1, 1)

            d_x = point.x() - x
            d_y = point.y() - y

            dist = np.sqrt(np.power(d_x, 2) + np.power(d_y, 2))

            # Checking if there is something in the way
            for o in self.scene().collidingItems(dummy_obj):
                if o == dummy_obj:
                    continue
                if isinstance(o, Tile) and not o.flyThrough:
                    return False
                elif isinstance(o, SpeedPowerup):
                    continue
                elif isinstance(o, Bullet):
                    continue
                elif isinstance(o, QGraphicsRectItem) and not isinstance(o, Tile):
                    return False
        return True

    def hasReachedPoint(self, point):
        # This defines when the robot has reached the given point by an offset
        offset = 2
        dist = np.sqrt(np.power(point.x() - (self.x + 0.5 * self.r), 2)
                       + np.power(point.y() - (self.y + 0.5 * self.r), 2))

        return dist <= offset

    def clearFollowPointQueue(self):
        self.point_queue.clear()

    def clearShootingQueue(self):
        self.shoot_queue.clear()

    def calculateAlphaToReachPoint(self, point):
        centered_x = (self.x + (0.5 * self.r))
        centered_y = (self.y + (0.5 * self.r))

        d_x = (point.x() - centered_x)
        d_y = (point.y() - centered_y)

        new_alpha = self.getAlpha([d_x, d_y])

        # This switch case is because of the arccos
        if point.y() >= centered_y:
            return 360 - new_alpha
        else:
            return new_alpha

    def setThreadToFinished(self):
        self.restart_brain()

    def restart_brain(self):
        self.threadpool.tryStart(self.brain)

    def stopAllThreads(self):
        self.brain.stop = True

    def move(self):
        if self.speed != 0:
            v_unit = self.getUnitVector(self.x,
                                        self.y,
                                        self.x + (self.getVector()[0] * self.speed),
                                        self.y + (self.getVector()[1] * self.speed))

            for i in range(int((self.getVector()[0] * self.speed) / v_unit[0])):
                collision = False

                self.x += v_unit[0]
                self.y += v_unit[1]

                self.setRect(self.boundingRect())

                # If collision takes place we step back

                while self.isCollidingWithTile():
                    self.x -= v_unit[0]
                    self.y -= v_unit[1]

                    self.setRect(self.boundingRect())

                    collision = True

                if collision:
                    break

    def render(self, painter):
        offset = self.r / 2

        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        painter.translate(self.x + offset, self.y + offset)
        painter.rotate(-self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawImage(self.boundingRect(), self.texture)

        painter.resetTransform()

        self.renderHealthBar(painter)

        if self.debug:
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))

            painter.drawEllipse(self.boundingRect())

            painter.drawLine(QPoint(int(self.x), int(self.y)),
                             QPoint(int(self.x + (self.getVector()[0] * 40)),
                                    int(self.y + (self.getVector()[1] * 40))))

            # Rendering the trace of the path
            for p in self.point_queue:
                painter.drawPoint(p)
