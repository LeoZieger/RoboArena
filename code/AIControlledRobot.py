import numpy as np
from PathUtil import getPath
from Tile import Tile
from BaseRobot import BaseRobot
import Brain
from PyQt5.QtGui import QImage, QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsRectItem


class AIControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed, arena, pool, n=0):
        BaseRobot.__init__(self, x, y, r, alpha, speed)
        self.n = n

        self.brain = Brain.BrainLVL1(self.n, arena)

        self.threadpool = pool

        self.brain.signals.informAboutNextPoint.connect(self.setNewPointToMoveTo)
        self.brain.signals.finished.connect(self.setThreadToFinished)
        self.brain.signals.informToClearQueue.connect(self.clearFollowPointQueue)

        self.brain.setAutoDelete(False)
        self.threadpool.start(self.brain)

        self.texture = QImage(getPath("res", "red_tank.png"))

        self.point_queue = []

        self.setRect(self.boundingRect())

    def inform_brain(self, human_player, robo_player):
        self.brain.inform_brain(human_player, robo_player)

    def setNewPointToMoveTo(self, new_point):
        self.point_queue.append(new_point)

    def followPoints(self):
        if len(self.point_queue) > 0:
            self.speed = self.MIN_SPEED

            if self.hasReachedPoint(self.point_queue[0]):
                self.point_queue.pop(0)
            else:
                new_alpha = self.calculateAlphaToReachPoint(self.point_queue[0])
                self.alpha = new_alpha
        else:
            self.speed = 0

    def hasReachedPoint(self, point):
        offset = 2
        dist = np.sqrt(np.power(point.x() - (self.x + 0.5 * self.r), 2)
                       + np.power(point.y() - (self.y + 0.5 * self.r), 2))

        return dist <= offset

    def clearFollowPointQueue(self):
        self.point_queue.clear()

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

            painter.drawRect(self.boundingRect())

            painter.drawLine(QPoint(int(self.x), int(self.y)),
                             QPoint(int(self.x + (self.getVector()[0] * 40)),
                                    int(self.y + (self.getVector()[1] * 40))))

            for p in self.point_queue:
                painter.drawPoint(p)

    # Allows AI-Robos to go through PowerUps without collision
    def aiCollisionWithTile(self, scene):
        if len(scene.collidingItems(self)) > 0:
            for o in scene.collidingItems(self):
                if issubclass(type(o), Tile) or isinstance(o, QGraphicsRectItem):
                    return True
        return False
