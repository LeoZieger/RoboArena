# Author: Lukas Reutemann

from BasicRobot import BasicRobot

import numpy as np


class BasicAIRobot(BasicRobot):

    def __init__(self, x, y, r, alpha, speed):
        super().__init__(x, y, r, alpha, speed)
        self.n = 0

    def getVector(self):

        return [np.cos(np.deg2rad(self.alpha)), np.sin(np.deg2rad(self.alpha))]

    def moveAI1(self, keys_pressed):
        if self.x > 850:
            self.alpha = 180
        if self.x < 650:
            self.alpha = 0
        self.x += self.getVector()[0] * self.speed / 2
        self.y += self.getVector()[1] * self.speed / 2

        self.setRect(int(self.x), int(self.y), self.r, self.r)

    def moveAI2(self, keys_pressed):
        self.alpha += 1
        self.x += self.getVector()[0] * self.speed / 2
        self.y += self.getVector()[1] * self.speed / 2

        self.setRect(int(self.x), int(self.y), self.r, self.r)

    def moveAI3(self, keys_pressed):
        if self.x <= 100:
            self.alpha = 315
        if self.x >= 200:
            self.alpha = 135

        self.x += self.getVector()[0] * self.speed / 2
        self.y += self.getVector()[1] * self.speed / 2

        self.setRect(int(self.x), int(self.y), self.r, self.r)
