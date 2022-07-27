
from PyQt5.QtGui import QImage
from PathUtil import getPath
from BasePowerup import BasePowerup


class HealthPowerup(BasePowerup):
    def __init__(self, x, y, healthAmount, isCollected):
        BasePowerup.__init__(self, x, y)
        self.healthAmount = healthAmount
        self.isCollected = isCollected
        self.texture = QImage(getPath("res", "healPowerup.png"))
