from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QRectF
from PathUtil import getPath


class BasePowerup(QGraphicsObject):
    def __init__(self, x, y):
        QGraphicsObject.__init__(self)
        self.x = x
        self.y = y
        self.texture = QImage(getPath("res", "notexturePowerup.png"))

    def info(self):
        print(self.x)
        print(self.y)
        print(self.duration)
        print(self.isCollected)

    def render(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawImage(self.boundingRect(), self.texture)

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), 40, 40)
