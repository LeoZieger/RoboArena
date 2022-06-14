# Author: Lukas Reutemann

from BasicRobot import BasicRobot

from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QRect
import numpy as np


class BasicAIRobot(BasicRobot):

    def __init__(self, x, y, r, alpha, speed):
        super().__init__(x, y, r, alpha, speed)
        self.n = 0

    def getVector(self):

        return [np.cos(np.deg2rad(self.alpha)), np.sin(np.deg2rad(self.alpha))]

    def render(self, painter):
        offset = self.r / 2

        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))

        painter.translate(self.x + offset, self.y + offset)
        painter.rotate(-self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawRect(QRect(self.x, self.y, self.r, self.r))

    def moveAI1(self, keys_pressed):
        if self.x > 850:
            self.alpha = 180
        if self.x < 650:
            self.alpha = 0
        self.x += self.getVector()[0] * self.speed / 2
        self.y -= self.getVector()[1] * self.speed / 2

    def moveAI2(self, keys_pressed):
        self.alpha += 1
        self.x += self.getVector()[0] * self.speed / 2
        self.y -= self.getVector()[1] * self.speed / 2

    def moveAI3(self, keys_pressed):
        if self.alpha > 180:
            self.alpha = 0

        if self.y > 200:
            self.alpha += 1
            self.x += self.getVector()[0] * self.speed / 2
            self.y -= self.getVector()[1] * self.speed / 2
        else:
            self.x = 100
            self.y = 850
