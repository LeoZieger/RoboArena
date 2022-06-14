# Author: Lasse Niederkrome


# This is important for drawing the robot later
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QRect
import numpy as np

MAX_SPEED = 5
MIN_SPEED = 3


class BasicRobot:

    # Basic-Robot constructor

    def __init__(self, x, y, r, alpha, speed):

        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # width
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed

    def getVector(self):

        return [np.cos(np.deg2rad(self.alpha)), np.sin(np.deg2rad(self.alpha))]

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
        painter.rotate(-self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawRect(QRect(int(self.x), int(self.y), self.r, self.r))

    def move(self, keys_pressed):
        if Qt.Key_W in keys_pressed:
            self.x += self.getVector()[0] * self.speed / 2
            self.y -= self.getVector()[1] * self.speed / 2

        if Qt.Key_S in keys_pressed:
            self.x -= self.getVector()[0] * self.speed / 2
            self.y += self.getVector()[1] * self.speed / 2

        if Qt.Key_A in keys_pressed:
            self.alpha += 1

        if Qt.Key_D in keys_pressed:
            self.alpha -= 1

        if Qt.Key_Shift in keys_pressed:
            if self.speed < MAX_SPEED:
                self.speed += 2
        else:
            self.speed = MIN_SPEED
