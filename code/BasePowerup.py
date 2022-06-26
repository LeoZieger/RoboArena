from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class BasePowerup():

    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.duration = duration

    def info(self):
        print(self.x)
        print(self.y)
        print(self.duration)


    def render(self, painter):

        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        painter.drawEllipse(self.x, self.y, 50, 50)




