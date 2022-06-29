# Author: Lasse Niederkrome

from PyQt5.QtCore import Qt
from BaseRobot import BaseRobot
from Tile import *


class HumanControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed):
        BaseRobot.__init__(self, x, y, r, alpha, speed)

        self.moveForward = False
        self.moveBackward = False


    def reactToUserInput(self, keys_pressed):
        if Qt.Key_W in keys_pressed:
            self.moveForward = True
        else:
            self.moveForward = False

        if Qt.Key_S in keys_pressed:
            self.moveBackward = True
        else:
            self.moveBackward = False

        if Qt.Key_Shift in keys_pressed:
            if self.speed < self.MAX_SPEED:
                self.speed += 2
        else:
            self.speed = self.MIN_SPEED

        if Qt.Key_A in keys_pressed:
            self.alpha += 2
        if Qt.Key_D in keys_pressed:
            self.alpha -= 2

    def move(self, scene):
        if self.moveForward:
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
                while self.collisonWithTile(scene):
                    if BaseRobot.debug:
                        print("collision with wall!")
                    self.x -= v_unit[0]
                    self.y -= v_unit[1]
                    collision = True

                if collision:
                    break

        if self.moveBackward:
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
                while self.collisonWithTile(scene):
                    print(self.collisonWithTile(scene))
                    self.x += v_unit[0]
                    self.y += v_unit[1]
                    collision = True

                if collision:
                    break

    def collisonWithTile(self, scene):
        if len(scene.collidingItems(self)) > 0:
            for o in scene.collidingItems(self):
                if issubclass(type(o), Tile) or isinstance(o, QGraphicsRectItem):
                    return True
        return False

    def collisionWithPowerup(self, scene):
        if (len(scene.collidingItems(self))) > 0:
            if BaseRobot.debug:
                print("collision with powerup!")
            self.MIN_SPEED += 2
            self.speed = self.MIN_SPEED
