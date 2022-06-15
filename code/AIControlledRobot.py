# Author: Lukas Reutemann

from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QRunnable
import numpy as np
import time

from BaseRobot import BaseRobot

class BasicAIRobot(BaseRobot, QRunnable):

    def __init__(self, x, y, r, alpha, speed):
        BaseRobot.__init__(self, x, y, r, alpha, speed)
        QRunnable.__init__(self)
        self.n = 0

    def run(self):
        print("Sleeping now")
        time.sleep(5)
        print("Waking up")

    def render(self, painter):
        offset = self.r / 2

        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))

        painter.translate(self.x + offset, self.y + offset)
        painter.rotate(-self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawRect(QRect(int(self.x), int(self.y), self.r, self.r))
