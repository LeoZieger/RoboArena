#!/usr/bin/python

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
import Arena


class TestArena(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.arena = Arena.Arena()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(self.arena.arena_width, self.arena.arena_height)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.drawArena()

    def drawArena(self):
        painter = QtGui.QPainter(self.label.pixmap())
        for x in range(self.arena.tile_count_x):
            for y in range(self.arena.tile_count_y):
                # painter.fillRect(self.arena.matrix[x][y].rect,
                #                 self.arena.matrix[x][y].color)
                painter.drawImage(self.arena.matrix[x][y].rect,
                                  self.arena.matrix[x][y].texture)
        painter.end()


app = QtWidgets.QApplication(sys.argv)
window = TestArena()
window.show()
app.exec_()
