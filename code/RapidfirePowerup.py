from PyQt5.QtGui import QImage
from PathUtil import getPath
from BasePowerup import BasePowerup


# Increases Firerate when collected
class RapidfirePowerup(BasePowerup):
    def __init__(self, x, y, fireRate, isCollected):
        BasePowerup.__init__(self, x, y)
        self.fireRate = fireRate
        self.isCollected = isCollected
        self.texture = QImage(getPath("res", "rapidPowerup.png"))
