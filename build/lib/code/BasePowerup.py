from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QRectF
from PathUtil import getPath


# This is the basepowerup, each powerup will inherit from this class
class BasePowerup(QGraphicsObject):
    def __init__(self, x, y):
        QGraphicsObject.__init__(self)
        self.x = x
        self.y = y
        self.texture = QImage(getPath("res", "notexturePowerup.png"))

    # Render-function for the powerups
    def render(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawImage(self.boundingRect(), self.texture)

    # This defines the collider
    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), 40, 40)
