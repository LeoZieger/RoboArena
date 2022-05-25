# Author: Lasse Niederkrome


# This is important for drawing the robot later
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class BasicRobot:

    # Basic-Robot constructor
    def __init__(self, x, y, r, alpha, speed):
        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # radius
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed

    # Small function that shows all robot-info.
    def info(self):
        print(self.x)
        print(self.y)
        print(self.r)
        print(self.alpha)
        print(self.speed)

    def render(self, painter):
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        painter.drawEllipse(self.x, self.y, self.r*2, self.r*2)

    def move(self, keys_pressed):
        if Qt.Key_W in keys_pressed:
            self.y -= self.speed
        if Qt.Key_S in keys_pressed:
            self.y += self.speed
        if Qt.Key_A in keys_pressed:
            self.x -= self.speed
        if Qt.Key_D in keys_pressed:
            self.x += self.speed
