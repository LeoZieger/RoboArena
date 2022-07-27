from BasePowerup import Basepowerup

class HealthPowerup():
    def __init__(self, x, y, HealthAmount, isCollected):
        BasePowerup.__init__(self, x, y)
        self.HealthAmount = HealthAmount
        self.isCollected = isCollected
