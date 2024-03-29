from BaseRobot import BaseRobot, MIN_SPEED, STANDARD_COOLDOWN, MAX_SPEED
import time
from PyQt5.QtCore import Qt
from SpeedPowerup import SpeedPowerup
from RapidfirePowerup import RapidfirePowerup
from HealthPowerup import HealthPowerup

ROTATION_SPEED = 3


class HumanControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed, texture, collectedSpeedPowerup):
        BaseRobot.__init__(self, x, y, r, alpha, speed, texture)

        self.moveForward = False
        self.moveBackward = False

        self.collectedSpeedPowerup = collectedSpeedPowerup

        self.texture = texture

    # User input of Player 1
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
            self.alpha += ROTATION_SPEED
        if Qt.Key_D in keys_pressed:
            self.alpha -= ROTATION_SPEED

        # Bullet
        if Qt.Key_Space in keys_pressed:
            if time.time() - self.canShootAgainAt > 0:
                self.shooting = True
                self.canShootAgainAt = time.time() + self.cooldown
            else:
                self.shooting = False
        else:
            self.shooting = False

    # User input of Player 2
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
            self.alpha += ROTATION_SPEED
        if Qt.Key_Right in keys_pressed:
            self.alpha -= ROTATION_SPEED

        # Bullet
        if Qt.Key_Return in keys_pressed:
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

    # Checks, if there is a collision with a Tile or an QGraphicsRectItem
    def collisionWithPowerup(self, scene):
        if (len(scene.collidingItems(self))) > 0 and not self.isCollisionWithRobot():
            for o in scene.collidingItems(self):
                if BaseRobot.debug:
                    print("collision with powerup!")
                # What kind of powerup was detected
                if issubclass(type(o), SpeedPowerup):
                    o.isCollected = True
                    if self.speed < MAX_SPEED:
                        self.speed += 2

                if issubclass(type(o), RapidfirePowerup):
                    o.isCollected = True
                    self.cooldown = 0.2

                if issubclass(type(o), HealthPowerup):
                    o.isCollected = True
                    self.healPlayer()

            return True

    # Void: This function resets the speed of a HumanControlledRobot
    def resetSpeed(self):
        self.speed = MIN_SPEED

    # Resets the cooldown of the shooting speed
    def resetCooldown(self):
        self.cooldown = STANDARD_COOLDOWN

    def healPlayer(self):
        if self.current_HP < self.max_HP:
            self.current_HP += 1
