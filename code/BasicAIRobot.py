# Author: Lukas Reutemann

from BasicRobot import BasicRobot

from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class BasicAIRobot(BasicRobot):

    def __init__(self, x, y, r, alpha, speed):
        super().__init__(x, y, r, alpha, speed)

    def render(self, painter):
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        painter.drawEllipse(self.x, self.y, self.r*2, self.r*2)

    def move(self, keys_pressed):
        self.y += self.speed
        self.x -= self.speed
