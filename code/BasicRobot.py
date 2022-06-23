# Author: Lasse Niederkrome


# This is important for drawing the robot later
from PyQt5.QtGui import QPen, QImage
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsRectItem
import numpy as np

MAX_SPEED = 5
MIN_SPEED = 3


class BasicRobot(QGraphicsRectItem):

    # Basic-Robot constructor
    debug = False

    def __init__(self, x, y, r, alpha, speed):
        super().__init__()

        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # width
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed
        self.texture = QImage("res/blue_tank.png")              # texture

        self.setRect(int(self.x), int(self.y), self.r, self.r)

    def getVector(self):
        return [np.cos(np.deg2rad(self.alpha)), np.sin(np.deg2rad(self.alpha))]

    def getUnitVector(self, old_x, old_y, new_x, new_y):
        length = np.sqrt(np.power(new_x - old_x, 2) + np.power(new_y - old_y, 2))
        v_unit = [(self.getVector()[0] * self.speed) / length,
                  (self.getVector()[1] * self.speed) / length]
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

        painter.translate(self.x + offset, self.y + offset)
        painter.rotate(self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawImage(self.rect(), self.texture)

        painter.resetTransform()

        if self.debug:
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))

            painter.drawRect(self.rect())

            painter.drawLine(QPoint(int(self.x), int(self.y)),
                             QPoint(int(self.x + (self.getVector()[0] * 40)),
                                    int(self.y + (self.getVector()[1] * 40))))

    def move(self, keys_pressed, scene):
        if Qt.Key_W in keys_pressed:
            v_unit = self.getUnitVector(self.x,
                                        self.y,
                                        self.x + (self.getVector()[0] * self.speed),
                                        self.y + (self.getVector()[1] * self.speed))

            # Checking UV for UV, if collision takes place
            for i in range(int((self.getVector()[0] * self.speed) / v_unit[0])):
                collision = False

                self.x += v_unit[0]
                self.y += v_unit[1]

                self.setRect(int(self.x), int(self.y), self.r, self.r)

                # If collision takes place we step back
                while len(scene.collidingItems(self)) > 0:
                    self.x -= v_unit[0]
                    self.y -= v_unit[1]
                    self.setRect(int(self.x), int(self.y), self.r, self.r)
                    collision = True

                if collision:
                    break

        if Qt.Key_S in keys_pressed:
            v_unit = self.getUnitVector(self.x,
                                        self.y,
                                        self.x - (self.getVector()[0] * self.speed),
                                        self.y - (self.getVector()[1] * self.speed))

            # Checking UV for UV, if collision takes place
            for i in range(int((self.getVector()[0] * self.speed) / v_unit[0])):
                collision = False

                self.x -= v_unit[0]
                self.y -= v_unit[1]

                self.setRect(int(self.x), int(self.y), self.r, self.r)

                # If collision takes place we step back
                while len(scene.collidingItems(self)) > 0:
                    self.x += v_unit[0]
                    self.y += v_unit[1]
                    self.setRect(int(self.x), int(self.y), self.r, self.r)
                    collision = True

                if collision:
                    break

        if Qt.Key_A in keys_pressed:
            self.alpha -= 2

        if Qt.Key_D in keys_pressed:
            self.alpha += 2

        if Qt.Key_Shift in keys_pressed:
            if self.speed < MAX_SPEED:
                self.speed += 2
        else:
            self.speed = MIN_SPEED

        self.setRect(int(self.x), int(self.y), self.r, self.r)
