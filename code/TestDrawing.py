# This is just a test for drawing a circle with PyQt5

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        self.top= 150
        self.left= 150
        self.width = 1000
        self.height = 1000
        self.InitWindow()

    def InitWindow(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 8, Qt.DashLine))
        painter.drawEllipse(500, 500, 10, 10)             # X, Y, WIDTH, HEIGHT



def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())







