# Author: Lukas Reutemann

from BasicRobot import BasicRobot

from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class BasicAIRobot(BasicRobot):

    def __init__(self, x, y, r, alpha, speed):
        super().__init__(x, y, r, alpha, speed)
        self.n = 0

    def render(self, painter):
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        painter.drawEllipse(self.x, self.y, self.r, self.r)

    def moveAI1(self, keys_pressed):
        if self.x < 650:
            self.alpha[0] *= -1
            self.x = 650
        if self.x > 850:
            self.alpha[0] *= -1
            self.x = 850

        self.x += self.alpha[0] * self.speed

    def moveAI2(self, keys_pressed):
        if self.x < 750 or self.y < 800:
            self.alpha = [1, 1]
            self.x = 750
            self.y = 800
        if self.x > 850 or self.y > 900:
            self.alpha = [-1, -1]
            self.x = 850
            self.y = 900

        self.x += self.alpha[0] * self.speed
        self.y += self.alpha[1] * self.speed

    def moveAI3(self, keys_pressed):
        if self.n <= 6:
            self.x += self.alpha[0] * self.speed
            self.y += self.alpha[1] * self.speed
            self.n += 1
        else:
            if self.alpha == [0, -1]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [-1, -1]

            elif self.alpha == [-1, -1]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [-1, 0]

            elif self.alpha == [-1, 0]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [-1, 1]

            elif self.alpha == [-1, 1]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [0, 1]

            elif self.alpha == [0, 1]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [1, 1]

            elif self.alpha == [1, 1]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [1, 0]

            elif self.alpha == [1, 0]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [1, -1]

            elif self.alpha == [1, -1]:
                self.x += self.alpha[0] * self.speed
                self.y += self.alpha[1] * self.speed
                self.alpha = [0, -1]

            self.n = 0
