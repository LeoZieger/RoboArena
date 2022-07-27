from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QRectF
from PathUtil import getPath
from BasePowerup import BasePowerup


class RapidfirePowerup(BasePowerup):
    def __init__(self, x, y, fireRate, isCollected):
        BasePowerup.__init__(self, x, y)
        self.fireRate = fireRate
        self.isCollected = isCollected
        self.texture = QImage(getPath("res", "rapidPowerup.png"))

    def increaseFirerate(self):
        if BaseRobot.cooldown == 1:
            BaseRobot.cooldown +=1

    def resetFirerate(self):
        if BaseRobot.cooldown > 1:
            BaseRobot.cooldown = 1
