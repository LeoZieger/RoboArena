# Author: Lasse Niederkrome


# This is important for drawing the robot later
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint, QRunnable, QRectF
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsObject, QGraphicsItem
import numpy as np

MAX_SPEED = 5
MIN_SPEED = 3


class BaseRobot(QGraphicsItem):

    debug = True

    # Basic-Robot constructor

    def __init__(self, x, y, r, alpha, speed):
        super().__init__()

        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # width
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed

    def getVector(self):
        return [np.cos(np.deg2rad(self.alpha)), np.sin(np.deg2rad(self.alpha))]

    def getUnitVector(self, old_x, old_y, new_x, new_y):
        l = np.sqrt(np.power(new_x - old_x, 2) + np.power(new_y - old_y, 2))
        v_unit = [(self.getVector()[0] * self.speed) / l,
                (self.getVector()[1] * self.speed) / l]
        return v_unit

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
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))

        painter.translate(self.x + offset, self.y + offset)
        painter.rotate(self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawRect(self.boundingRect())

        painter.resetTransform()

        if self.debug:
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))

            painter.drawRect(self.boundingRect())

            painter.drawLine(QPoint(int(self.x), int(self.y)),
                            QPoint(int(self.x + (self.getVector()[0] * 40)),
                                    int(self.y + (self.getVector()[1] * 40))))
        
    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.r, self.r)
