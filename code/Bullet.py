from PyQt5.QtGui import QImage, QPen
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsRectItem


class Bullet(QGraphicsRectItem):
    def __init__(self, x, y, direction, width, velocity):
        QGraphicsRectItem.__init__(self)

        self.texture = QImage("res/bullet.png")
        self.x = x
        self.y = y
        self.direction = direction  # direction of bullet as vector
        self.width = width
        self.velocity = velocity  # speed of the bullet

        self.setRect(self.boundingRect())

    # Calculates how the bullet has to travel
    def trajectory(self):
        self.x = self.x + self.direction[0] * self.velocity
        self.y = self.y + self.direction[1] * self.velocity

        self.setRect(self.boundingRect())

    # Renders the bullet on the canvas
    def render(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.DashLine))
        painter.drawEllipse(int(self.x), int(self.y),
                            int(self.width), int(self.width))
        painter.setPen(QPen(Qt.red, 5, Qt.DashLine))
        painter.drawRect(self.boundingRect())

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.width, self.width)

    def isHittingObject(self, scene):
        if len(scene.collidingItems(self)) > 0:
            return True, scene.collidingItems(self)[0]
        return False, None
