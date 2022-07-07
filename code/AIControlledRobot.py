from PyQt5.QtCore import QThreadPool

import numpy as np

from BaseRobot import BaseRobot
import Brain
from PyQt5.QtGui import QImage


class AIControlledRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed, arena, n=0):
        BaseRobot.__init__(self, x, y, r, alpha, speed)
        self.n = n

        self.brain = Brain.BrainLVL1(self.n, arena)

        self.brain.signals.informAboutNextPoint.connect(self.setNewPointToMoveTo)
        self.brain.signals.finished.connect(self.setThreadToFinished)
        self.brain.signals.informToClearQueue.connect(self.clearFollowPointQueue)

        self.pool = QThreadPool()
        self.brain.setAutoDelete(False)
        self.pool.start(self.brain)

        self.texture = QImage("res/red_tank.png")

        self.point_queue = []

    def inform_brain(self, human_player, robo_player):
        self.brain.inform_brain(human_player, robo_player)

    def setNewPointToMoveTo(self, new_point):
        self.point_queue.append(new_point)

    def followPoints(self):
        if len(self.point_queue) > 0:
            if self.hasReachedPoint(self.point_queue[0]):
                self.point_queue.pop(0)
            else:
                self.speed = 1
                new_alpha = self.calculateAlphaToReachPoint(self.point_queue[0])
                self.alpha = new_alpha
        else:
            self.speed = 0

    def hasReachedPoint(self, point):
        offset = 2
        dist = np.sqrt(np.power(point.x() - self.x, 2)
                       + np.power(point.y() - self.y, 2))
        return dist <= offset

    def clearFollowPointQueue(self):
        self.point_queue.clear()

    def calculateAlphaToReachPoint(self, point):
        d_x = (point.x() - self.x)
        d_y = (point.y() - self.y)

        # This switch case is because of the arccos
        if point.y() >= self.y:
            return 360 - self.getAlpha([d_x, d_y])
        else:
            return self.getAlpha([d_x, d_y])

    def setThreadToFinished(self):
        self.restart_brain()

    def restart_brain(self):
        self.pool.tryStart(self.brain)

    def stopAllThreads(self):
        self.brain.stop = True

    # For now, the Robots will drive against walls which isnt that impressive
    def move(self, scene):
        self.x += self.getVector()[0] * self.speed
        self.y += self.getVector()[1] * self.speed
