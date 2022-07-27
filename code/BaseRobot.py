from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsEllipseItem, QGraphicsRectItem
import numpy as np
from Bullet import Bullet
from Tile import Tile

MAX_SPEED = 5
MIN_SPEED = 3
STANDARD_COOLDOWN = 4


class BaseRobot(QGraphicsEllipseItem):
    debug = False

    # Basic-Robot constructor
    def __init__(self, x, y, r, alpha, speed, texture):
        QGraphicsEllipseItem.__init__(self)

        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # width
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed

        self.canShootAgainAt = 0
        self.cooldown = STANDARD_COOLDOWN

        self.max_HP = 3
        self.current_HP = 3

        self.shooting = False

        # Initialising the bounding box for the circular hitbox (EllipseItem)
        self.setRect(self.boundingRect())

    # Get the current direction vector of a robot
    def getVector(self):
        return [np.cos(np.deg2rad(self.alpha)), -1 * np.sin(np.deg2rad(self.alpha))]

    # Get the current direction of a robot in degrees
    def getAlpha(self, v2):
        v1 = [1, 0]
        l1 = np.sqrt(np.power(v1[0], 2) + np.power(v1[1], 2))
        l2 = np.sqrt(np.power(v2[0], 2) + np.power(v2[1], 2))
        if l1 != 0 and l2 != 0:
            return np.rad2deg(np.arccos(
                                        ((v1[0] * v2[0]) + (v1[1] * v2[1])) /
                                        (l1 * l2)))
        return 0

    # Get the normalised vector from one point to another
    def getUnitVector(self, old_x, old_y, new_x, new_y):
        dist = np.sqrt(np.power(new_x - old_x, 2) + np.power(new_y - old_y, 2))
        if dist != 0:
            v_unit = [(self.getVector()[0] * self.speed) / dist,
                      (self.getVector()[1] * self.speed) / dist]
            return v_unit
        else:
            return [0, 0]

    # render the robot using QPainter
    def render(self, painter):
        offset = self.r / 2

        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        painter.translate(self.x + offset, self.y + offset)
        painter.rotate(-self.alpha)
        painter.translate(-(self.x + offset), -(self.y + offset))

        painter.drawImage(self.boundingRect(), self.texture)

        painter.resetTransform()

        self.renderHealthBar(painter)

        # Optional debug-mode to show the direction and hitbox of a robot
        if self.debug:
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))

            painter.drawEllipse(self.boundingRect())

            painter.drawLine(QPoint(int(self.x), int(self.y)),
                             QPoint(int(self.x + (self.getVector()[0] * 40)),
                                    int(self.y + (self.getVector()[1] * 40))))

    # Create the health-bar of the robot with QPainter
    def renderHealthBar(self, painter):
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        # outer rect
        painter.drawRect(
            int(self.x),
            int(self.y - 20),
            int(self.r),
            2
        )

        # inner red 'filling'
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawRect(
            int(self.x),
            int(self.y - 20),
            int((self.current_HP / self.max_HP) * self.r),
            2)

    def takeDamage(self):
        if self.current_HP != 0:
            self.current_HP -= 1

    def isDestroyed(self):
        return self.current_HP == 0

    # Bounding rectangle of the circular hitbox
    def boundingRect(self):
        return QRectF(int(self.x), int(self.y), self.r, self.r)

    def createBullet(self):
        x_pos, y_pos = self.calculateBulletStartPos()

        return Bullet(x_pos,
                      y_pos,
                      self.getVector(),
                      14,
                      10)

    def calculateBulletStartPos(self):
        radius_around_rect = np.sqrt(
                                np.power(self.r, 2) + np.power(self.r, 2))
        x_pos = ((self.x + 0.5 * self.r)
                 + self.getVector()[0] * radius_around_rect)
        y_pos = ((self.y + 0.5 * self.r)
                 + self.getVector()[1] * radius_around_rect)

        return x_pos, y_pos

    def isCollidingWithTile(self):
        for o in self.scene().collidingItems(self):
            if (issubclass(type(o), Tile) or
               type(o) == QGraphicsRectItem):
                return True
        return False
