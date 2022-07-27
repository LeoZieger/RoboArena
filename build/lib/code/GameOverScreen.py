from PyQt5.QtWidgets import QPushButton, QApplication, \
                            QMainWindow, QLabel, QDesktopWidget
from PyQt5.QtGui import QMovie, QPainter, QIcon
from PyQt5.QtCore import QSize
import PyQt5.QtCore
import sys
from SoundFX import SoundFX
from PathUtil import getPath

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
BUTTON_HEIGHT = 80


class GameOverScreen(QMainWindow):
    def __init__(self, result, color):
        super().__init__()
        self.result = result
        self.color = color
        self.initUI()

    def initUI(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centerWindowOnScreen()
        self.setWindowTitle('RoboArena')
        self.setWindowIcon(QIcon(getPath("res", "blue_tank.png")))

        # Background
        self.background_gif = QMovie(getPath("res", "BackgroundGif.gif"))
        self.background_gif.setScaledSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_gif.frameChanged.connect(self.repaint)
        self.background_gif.start()

        SoundFX.initMenuSoundtrack(self, True)

        # Game over text
        name_label = QLabel("GAME OVER", self)
        name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        name_label.resize(WINDOW_WIDTH, BUTTON_HEIGHT)
        name_label.move(0, 200)
        name_label.setStyleSheet(
            "color: white;"
            "font-size: 100px;"
            "font-style: courier;"
            "font-weight: 1000;"
        )

        # Shows who won the game
        name_label = QLabel(self.result, self)
        name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        name_label.resize(WINDOW_WIDTH, BUTTON_HEIGHT)
        name_label.move(0, 300)
        name_label.setStyleSheet(
            "color:" + self.color + ";"
            "font-size: 50px;"
            "font-style: courier;"
            "font-weight: 1000;"
        )

        # Quit
        quit_btn = QPushButton('Quit', self)
        quit_btn.resize(500, BUTTON_HEIGHT)
        quit_btn.move(250, 500)
        quit_btn.clicked.connect(QApplication.instance().quit)

        # Stylesheet for Buttons
        buttonstyle = """
                    QWidget{
                        border: 3px solid #0a0a0a;
                        background-color: #c7bfbf;
                        font:20px;
                    }
                    QPushButton:hover{
                        border: 3px solid #0a0a0a;
                        background-color: #f2eded;
                    }
                    QPushButton:pressed{
                        background-color: #c7bfbf;
                    }
                        """

        # Apply stylesheet to the buttons
        quit_btn.setStyleSheet(buttonstyle)

        self.show()

    def paintEvent(self, event):
        currentFrame = self.background_gif.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def centerWindowOnScreen(self):
        outerRect = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        outerRect.moveCenter(centerOfScreen)
        self.move(outerRect.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameOverScreen()
    app.exec_()
