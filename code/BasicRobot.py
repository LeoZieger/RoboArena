# Author: Lasse Niederkrome


# This is important for drawing the robot later
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt


class BasicRobot:

    # Basic-Robot constructor
    def __init__(self, x, y, r, alpha):
        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # radius
        self.alpha = alpha                  # direction

    # Small function that shows all robot-info.
    def info(self):
        print(self.x)
        print(self.y)
        print(self.r)
        print(self.alpha)

    def render(self, painter):
        painter.setPen(QPen(Qt.green, 8, Qt.DashLine))
        painter.drawEllipse(self.x, self.y, self.r*2, self.r*2)

    def move(self):
        self.x += 1
        self.y += 1
