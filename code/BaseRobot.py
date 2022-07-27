# Author: Lasse Niederkrome

from PyQt5.QtGui import QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsRectItem
import numpy as np
from Bullet import Bullet
from Tile import Tile
from PathUtil import getPath


class BaseRobot(QGraphicsRectItem):
    MAX_SPEED = 5
    MIN_SPEED = 3

    debug = False

    # Basic-Robot constructor

    def __init__(self, x, y, r, alpha, speed):
        QGraphicsObject.__init__(self)

        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # width
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed
        self.texture = QImage(getPath("res", "blue_tank.png"))        # texture

        self.canShootAgainAt = 0
        self.cooldown = 1

        self.max_HP = 3
        self.current_HP = 3

        self.shooting = False

        self.setRect(self.boundingRect())

    def getVector(self):
        return [np.cos(np.deg2rad(self.alpha)), -1 * np.sin(np.deg2rad(self.alpha))]

    def getAlpha(self, v2):
        v1 = [1, 0]
        l1 = np.sqrt(np.power(v1[0], 2) + np.power(v1[1], 2))
        l2 = np.sqrt(np.power(v2[0], 2) + np.power(v2[1], 2))
        if l1 != 0 and l2 != 0:
            return np.rad2deg(np.arccos(
                                        ((v1[0] * v2[0]) + (v1[1] * v2[1])) /
                                        (l1 * l2)))
        return 0

    def getUnitVector(self, old_x, old_y, new_x, new_y):
        dist = np.sqrt(np.power(new_x - old_x, 2) + np.power(new_y - old_y, 2))
        if dist != 0:
            v_unit = [(self.getVector()[0] * self.speed) / dist,
                      (self.getVector()[1] * self.speed) / dist]
            return v_unit
        else:
            return [0, 0]

    # Small function that shows all robot-info.
    def info(self):
        print(self.x)
        print(self.y)
        print(self.r)
        print(self.alpha)
        print(self.speed)

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

    def renderHealthBar(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        # outer rect
        painter.drawRect(
            int(self.x),
            int(self.y - 20),
            int(self.r),
            2
        )

        # inner red 'filling'
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawRect(
            int(self.x),
            int(self.y - 20),
            int((self.current_HP / self.max_HP) * self.r),
            2)

    def takeDamage(self):
        if self.current_HP != 0:
            self.current_HP -= 1

    def isDestroyed(self):
        return self.current_HP == 0

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.r, self.r)

    def createBullet(self):
        x_pos, y_pos = self.calculateBulletStartPos()

        return Bullet(x_pos,
                      y_pos,
                      self.getVector(),
                      10,
                      15)

    def calculateBulletStartPos(self):
        radius_around_rect = np.sqrt(
                                np.power(self.r, 2) + np.power(self.r, 2))
        x_pos = ((self.x + 0.5 * self.r)
                 + self.getVector()[0] * radius_around_rect)
        y_pos = ((self.y + 0.5 * self.r)
                 + self.getVector()[1] * radius_around_rect)

        return x_pos, y_pos

    def isCollidingWithTile(self):
        for o in self.scene().collidingItems(self):
            if (issubclass(type(o), Tile) or
               type(o) == QGraphicsRectItem):
                return True
        return False
