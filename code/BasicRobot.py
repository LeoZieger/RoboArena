# Author: Lasse Niederkrome


# This is important for drawing the robot later
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QRect

MAX_SPEED = 5
MIN_SPEED = 3


class BasicRobot:

    # Basic-Robot constructor

    def __init__(self, x, y, r, alpha, speed):

        self.x = x                          # x-position
        self.y = y                          # y-position
        self.r = r                          # radius
        self.alpha = alpha                  # direction
        self.speed = speed                  # speed

    # Small function that shows all robot-info.
    def info(self):
        print(self.x)
        print(self.y)
        print(self.r)
        print(self.alpha)
        print(self.speed)

    def render(self, painter):
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        painter.drawEllipse(self.x, self.y, self.r, self.r)

    def try_move(self, keys_pressed, other_objects):
        COLLISION_OFFSET = 7

        if Qt.Key_W in keys_pressed:
            intersect, possible = self.move_is_possible(self.x, self.y - self.speed, other_objects)
            if possible:
                self.y -= self.speed
            else:
                self.y = self.y + intersect.height() + COLLISION_OFFSET

        if Qt.Key_S in keys_pressed:
            intersect, possible = self.move_is_possible(self.x, self.y + self.speed, other_objects)
            if possible:
                self.y += self.speed
            else:
                self.y = self.y - intersect.height() - COLLISION_OFFSET

        if Qt.Key_A in keys_pressed:
            intersect, possible = self.move_is_possible(self.x - self.speed, self.y, other_objects)
            if possible:
                self.x -= self.speed
            else:
                self.x = self.x + intersect.width() + COLLISION_OFFSET

        if Qt.Key_D in keys_pressed:
            intersect, possible = self.move_is_possible(self.x + self.speed, self.y, other_objects)
            if possible:
                self.x += self.speed
            else:
                self.x = self.x - intersect.width() - COLLISION_OFFSET

        if Qt.Key_Shift in keys_pressed:
            if self.speed < MAX_SPEED:
                self.speed += 2
        elif self.speed == MAX_SPEED:
            self.speed = MIN_SPEED

    def move_is_possible(self, fut_x, fut_y, other_objects):
        for o in other_objects:
            if self.get_bounding_box().intersects(o):
                return self.get_bounding_box().intersected(o), False
        return None, True

    def get_bounding_box(self):
        return QRect(self.x,
                     self.y,
                     self.r,
                     self.r)
