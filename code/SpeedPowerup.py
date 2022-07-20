from BasePowerup import BasePowerup


class SpeedPowerup(BasePowerup):

    def __init__(self, x, y, duration, isCollected):
        BasePowerup.__init__(self, x, y, duration, isCollected)
