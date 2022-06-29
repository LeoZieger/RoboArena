from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QRectF


class BasePowerup(QGraphicsObject):

    def __init__(self, x, y, duration):
        QGraphicsObject.__init__(self)
        self.x = x
        self.y = y
        self.duration = duration

    def info(self):
        print(self.x)
        print(self.y)
        print(self.duration)

    def render(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(self.x, self.y, 20, 20)

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), 20, 20)
