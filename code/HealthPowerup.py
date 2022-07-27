from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QRectF
from PathUtil import getPath
from BasePowerup import BasePowerup


class HealthPowerup(BasePowerup):
    def __init__(self, x, y, HealthAmount, isCollected):
        BasePowerup.__init__(self, x, y)
        self.HealthAmount = HealthAmount
        self.isCollected = isCollected
        self.texture = QImage(getPath("res", "healPowerup.png"))


