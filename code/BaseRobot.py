# Author: Lasse Niederkrome

from PyQt5.QtGui import QPen, QImage
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtWidgets import QGraphicsObject
import numpy as np


class BaseRobot(QGraphicsObject):
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
        self.texture = QImage("res/blue_tank.png")              # texture

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

        if self.debug:
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))

            painter.drawRect(self.boundingRect())

            painter.drawLine(QPoint(int(self.x), int(self.y)),
                             QPoint(int(self.x + (self.getVector()[0] * 40)),
                                    int(self.y + (self.getVector()[1] * 40))))

    def move(self, scene):
        if self.speed != 0:
            v_unit = self.getUnitVector(self.x,
                                        self.y,
                                        self.x + (self.getVector()[0] * self.speed),
                                        self.y + (self.getVector()[1] * self.speed))

            # Checking UV for UV, if collision takes place
            for i in range(int((self.getVector()[0] * self.speed) / v_unit[0])):
                collision = False

                self.x += v_unit[0]
                self.y += v_unit[1]

                # If collision takes place we step back
                while len(scene.collidingItems(self)) > 0:
                    self.x -= v_unit[0]
                    self.y -= v_unit[1]
                    collision = True

                if collision:
                    break

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.r, self.r)
