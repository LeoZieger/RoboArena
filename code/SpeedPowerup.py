
from PyQt5.QtGui import QImage
from PathUtil import getPath
from BasePowerup import BasePowerup


class SpeedPowerup(BasePowerup):

    def __init__(self, x, y, duration, isCollected):
        BasePowerup.__init__(self, x, y)
        self.duration = duration
        self.isCollected = isCollected
        self.texture = QImage(getPath("res", "speedPowerup.png"))
