from PyQt5.QtGui import QImage, QPen
from PyQt5.QtCore import Qt
import numpy as np
import math


class Bullet():
    def __init__(self, tank, width, velocity):
        self.texture = QImage("res/bullet.png")  # bullet
        self.x = tank.x + tank.r/2               # x-position of the tank
        self.y = tank.y + tank.r/2               # y-position of the tank
        self.width = width                       # width of the bullet
        self.alpha = tank.alpha                  # direction/angle
        self.velocity = velocity                 # speed of the bullet
        rad_alpha = -np.deg2rad(tank.alpha)
        offset = tank.r/2, 0
        offset = self.rotate_x_y(offset, rad_alpha)
        self.x += offset[0]
        self.y += offset[1]
        # Später damage hinzufügen!

    # Rotates x and y
    def rotate_x_y(self, vec, rad_alpha):
        x = vec[0] * math.cos(rad_alpha) - vec[1] * math.sin(rad_alpha)
        y = vec[0] * math.sin(rad_alpha) + vec[1] * math.cos(rad_alpha)

        return x, y

    # Calculates how the bullet has to travel
    def trajectory(self):
        rad_alpha = -np.deg2rad(self.alpha)
        speed = self.velocity, 0
        rotated = self.rotate_x_y(speed, rad_alpha)
        self.x += rotated[0]
        self.y += rotated[1]

    # Renders the bullet on the canvas
    def render(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.DashLine))
        painter.drawEllipse(int(self.x), int(self.y), int(self.width), int(self.width))
