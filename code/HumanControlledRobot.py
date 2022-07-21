# Author: Lasse Niederkrome, Leonard Zieger, Lukas Reutemann

from PyQt5.QtWidgets import QGraphicsRectItem
from BaseRobot import BaseRobot

import time

from PyQt5.QtCore import Qt
from Tile import Tile
from BasePowerup import BasePowerup

MAX_SPEED = 5
MIN_SPEED = 3


class HumanControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed):
        BaseRobot.__init__(self, x, y, r, alpha, speed)

        self.moveForward = False
        self.moveBackward = False
        self.shooting = False

    def reactToUserInput(self, keys_pressed):
        if Qt.Key_W in keys_pressed:
            self.moveForward = True
        else:
            self.moveForward = False

        if Qt.Key_S in keys_pressed:
            self.moveBackward = True
        else:
            self.moveBackward = False

        if Qt.Key_A in keys_pressed:
            self.alpha += 2
        if Qt.Key_D in keys_pressed:
            self.alpha -= 2

        # Bullet
        if Qt.Key_Space in keys_pressed:
            if time.time() - self.canShootAgainAt > 0:
                self.shooting = True
                self.canShootAgainAt = time.time() + self.cooldown
            else:
                self.shooting = False
        else:
            self.shooting = False

    def reactToUserInput2(self, keys_pressed):
        if Qt.Key_Up in keys_pressed:
            self.moveForward = True
        else:
            self.moveForward = False

        if Qt.Key_Down in keys_pressed:
            self.moveBackward = True
        else:
            self.moveBackward = False

        if Qt.Key_Left in keys_pressed:
            self.alpha += 2
        if Qt.Key_Right in keys_pressed:
            self.alpha -= 2

        # Bullet
        if Qt.Key_Enter in keys_pressed:
            if time.time() - self.canShootAgainAt > 0:
                self.shooting = True
                self.canShootAgainAt = time.time() + self.cooldown
            else:
                self.shooting = False
        else:
            self.shooting = False

    def isCollisionWithRobot(self):
        for o in self.scene().collidingItems(self):
            if issubclass(type(o), BaseRobot):
                return True
        return False

    def collisionWithTile(self, scene):
        if len(scene.collidingItems(self)) > 0:
            for o in scene.collidingItems(self):
                if issubclass(type(o), Tile) or isinstance(o, QGraphicsRectItem):
                    return True
        return False

    def move(self):
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

                self.setRect(self.boundingRect())

                # If collision takes place we step back
                while self.isCollidingWithTile():
                    self.x -= v_unit[0]
                    self.y -= v_unit[1]

                    self.setRect(self.boundingRect())

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

                self.setRect(self.boundingRect())

                # If collision takes place we step back
                while self.isCollidingWithTile():
                    self.x += v_unit[0]
                    self.y += v_unit[1]

                    self.setRect(self.boundingRect())

                    collision = True

                if collision:
                    break

    # Checks, if there is a collision with a Tile or an QGraphicsRectItem.
    # A Tile is a one of:
    # -WaterTile
    # -LavaTile
    #
    # a QGraphicsRectItem is one of:
    # -Wall around the map
    #
    # Returns Boolean

    # Checks, if there is a collision with a powerup. Increasing speed
    # to MAX_SPEED@BsaseRobot.py if True
    def collisionWithPowerup(self, scene):
        if (len(scene.collidingItems(self))) > 0:

            for o in scene.collidingItems(self):
                if issubclass(type(o), BasePowerup):
                    o.isCollected = True
            if BaseRobot.debug:
                print("collision with powerup!")

            if self.speed < self.MAX_SPEED:
                self.speed += 2
            return True

    # Void: This function resets the speed of a HumanControlledRobot
    def resetSpeed(self):
        self.speed -= 2
