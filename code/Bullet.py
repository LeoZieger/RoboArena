from PyQt5.QtGui import QImage, QBrush
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsRectItem
from PathUtil import getPath
from SpeedPowerup import SpeedPowerup
from Tile import Tile
import numpy as np


class Bullet(QGraphicsRectItem):
    def __init__(self, x, y, direction, width, velocity):
        QGraphicsRectItem.__init__(self)

        self.texture = QImage(getPath("res", "bullet.png"))
        self.x = x
        self.y = y
        self.direction = direction  # direction of bullet as vector
        self.width = width
        self.velocity = velocity  # speed of the bullet

        self.reflectedOnce = False

        self.setRect(self.boundingRect())

    # Calculates how the bullet has to travel
    def trajectory(self):
        v_unit = self.getUnitVector(self.x,
                                    self.y,
                                    self.x + (self.direction[0] * self.velocity),
                                    self.y + (self.direction[1] * self.velocity))

        # Checking UV for UV, if collision takes place
        for i in range(int((self.direction[0] * self.velocity) / v_unit[0])):
            self.x += v_unit[0]
            self.y += v_unit[1]

            self.setRect(self.boundingRect())

            if self.shouldStopMove():
                return

    def shouldStopMove(self):
        for o in self.scene().collidingItems(self):
            if not isinstance(o, SpeedPowerup):
                if isinstance(o, Tile) and o.flyThrough:
                    continue
                else:
                    return True
        return False

    def getUnitVector(self, old_x, old_y, new_x, new_y):
        dist = np.sqrt(np.power(new_x - old_x, 2) + np.power(new_y - old_y, 2))
        if dist != 0:
            v_unit = [(self.direction[0] * self.velocity) / dist,
                      (self.direction[1] * self.velocity) / dist]
            return v_unit
        else:
            return [0, 0]

    def getDegree(self, v2):
        v1 = [1, 0]
        l1 = np.sqrt(np.power(v1[0], 2) + np.power(v1[1], 2))
        l2 = np.sqrt(np.power(v2[0], 2) + np.power(v2[1], 2))
        if l1 != 0 and l2 != 0:
            return np.rad2deg(np.arccos(
                                        ((v1[0] * v2[0]) + (v1[1] * v2[1])) /
                                        (l1 * l2)))
        return 0

    # Renders the bullet on the canvas
    def render(self, painter):
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawEllipse(int(self.x), int(self.y),
                            int(self.width), int(self.width))

    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.width, self.width)

    def isHittingObject(self):
        if len(self.scene().collidingItems(self)) > 0:
            return True, self.scene().collidingItems(self)[0]
        return False, None

    def isHittingSpecObject(self, obj):
        return obj in self.scene().collidingItems(self)

    def reflect(self, o):
        # backing off to make sure there is a clea collision side
        while self.isHittingSpecObject(o):
            self.velocity = -self.velocity
            self.trajectory()
            self.velocity = -self.velocity

        original_rect = o.rect()

        while not self.isInSideArea(o):
            # If collision in Side area is not detectable,
            # we just make the side area bigger. The Side
            # we collide stays still the same
            self.scaleUpRectAroundCenter(o, 1.2)

        o.setRect(original_rect)
        self.reflectedOnce = True

    def isInSideArea(self, o):
        if o.rect().x() < self.x + self.width <= o.rect().x() + o.rect().width():
            self.direction[1] = -1 * self.direction[1]  # Collision Top/Bottom
            return True
        elif o.rect().y() < self.y + self.width <= o.rect().y() + o.rect().height():
            self.direction[0] = -1 * self.direction[0]  # Collision Left/Right
            return True
        return False

    def scaleUpRectAroundCenter(self, o, scale):
        new_width = o.rect().width() * scale
        new_height = o.rect().height() * scale
        new_x = o.rect().x() - 0.5 * (new_width - o.rect().width())
        new_y = o.rect().y() - 0.5 * (new_height - o.rect().height())

        o.setRect(new_x, new_y, new_width, new_height)
