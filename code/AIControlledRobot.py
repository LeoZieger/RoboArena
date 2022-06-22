from PyQt5.QtCore import QThreadPool

import numpy as np

from BaseRobot import BaseRobot
import Brain


class BasicAIRobot(BaseRobot):

    def __init__(self, x, y, r, alpha, speed, n=0):
        BaseRobot.__init__(self, x, y, r, alpha, speed)
        self.n = n

        self.thread_is_finished = False

        self.brain = Brain.BrainLVL1(self.n)

        self.brain.signals.informAboutNextPoint.connect(self.setNewPointToMoveTo)
        self.brain.signals.finished.connect(self.setThreadToFinished)

        self.pool = QThreadPool()
        self.pool.start(self.brain)
        self.brain.setAutoDelete(False)

        self.point_queue = []

    def inform_brain(self, arena, human_player):
        self.brain.inform_brain(arena, human_player)

        if self.thread_is_finished:
            self.thread_is_finished = False
            self.pool.tryStart(self.brain)

    def setNewPointToMoveTo(self, n, new_point):
        if n == self.n:
            if len(self.point_queue) > 0:
                if self.point_queue[0] != new_point:
                    self.point_queue.append(new_point)
            else:
                self.point_queue.append(new_point)

    def followPoints(self):
        if len(self.point_queue) > 0:
            if self.hasReachedPoint(self.point_queue[0]):
                self.point_queue.pop()
            else:
                new_alpha = self.calculateAlphaToReachPoint(self.point_queue[0])
                self.alpha = new_alpha

    def hasReachedPoint(self, point):
        offset = 2  # precission of radius when robot reached Point
        dist = np.sqrt(np.power(point.x() - self.x, 2)
                       + np.power(point.y() - self.y, 2))
        return dist <= offset

    def calculateAlphaToReachPoint(self, point):
        d_x = (point.x() - self.x)
        d_y = (point.y() - self.y)

        # This switch case is because of the arccos
        if point.y() >= self.y:
            return 360 - self.getAlpha([d_x, d_y])
        else:
            return self.getAlpha([d_x, d_y])

    def setThreadToFinished(self, n):
        if n == self.n:
            self.thread_is_finished = True

    def stopAllThreads(self):
        self.brain.stop = True

    # For now, the Robots will drive against walls which isnt that impressive
    def move(self, scene):
        self.x += self.getVector()[0] * self.speed
        self.y += self.getVector()[1] * self.speed
