from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QPoint
import time

import Arena
import BaseRobot


class Signals(QObject):
    finished = pyqtSignal(int)
    informAboutNextPoint = pyqtSignal(int, QPoint)


class BrainLVL1(QRunnable):
    signals = Signals()

    def __init__(self, n):
        QRunnable.__init__(self)
        self.n = n

        self.arena = Arena.Arena()
        self.human_player = BaseRobot.BaseRobot(0, 0, 0, 0, 0)

        self.stop = False

    def inform_brain(self, arena, human_player):
        self.arena = arena
        self.human_player = human_player

    def run(self):
        time.sleep(1)
        if self.stop:
            return

        # TODO PATHFINDING To Point
        self.signals.informAboutNextPoint.emit(self.n,
                                               QPoint(int(self.human_player.x),
                                                      int(self.human_player.y)))
        self.signals.finished.emit(self.n)
