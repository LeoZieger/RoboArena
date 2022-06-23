# Author: Lasse Niederkrome

from PyQt5.QtCore import Qt, QRectF

from BaseRobot import BaseRobot

MAX_SPEED = 5
MIN_SPEED = 3


class HumanControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed):
        BaseRobot.__init__(self, x, y, r, alpha, speed)

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

                # If collision takes place we step back
                while len(scene.collidingItems(self)) > 0:
                    self.x -= v_unit[0]
                    self.y -= v_unit[1]
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

                # If collision takes place we step back
                while len(scene.collidingItems(self)) > 0:
                    self.x += v_unit[0]
                    self.y += v_unit[1]
                    collision = True

                if collision:
                    break

        if Qt.Key_A in keys_pressed:
            self.alpha += 1

        if Qt.Key_D in keys_pressed:
            self.alpha -= 1

        if Qt.Key_Shift in keys_pressed:
            if self.speed < MAX_SPEED:
                self.speed += 2
        else:
            self.speed = MIN_SPEED

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.r, self.r)
