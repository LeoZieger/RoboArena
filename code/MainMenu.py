from PyQt5.QtWidgets import QPushButton, QApplication, \
                            QMainWindow, QLabel, QDesktopWidget, \
                            QMenu, QAction
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import PyQt5.QtCore

import sys
import RoboArena
import MapCreator


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
BUTTON_HEIGHT = 80


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centerWindowOnScreen()

        # Background
        background_image = QImage("background.jpg")

        # resize Image to widgets size
        sImage = background_image.scaled(QSize(WINDOW_WIDTH, WINDOW_WIDTH))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        # Header
        name_label = QLabel("ROBO ARENA", self)
        name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        name_label.resize(WINDOW_WIDTH, BUTTON_HEIGHT)
        name_label.move(0, 80)
        name_label.setStyleSheet(
            "color: white;"
            "font-size: 100px;"
            "font-style: courier;"
            "font-weight: 1000;"
        )

        # Start Game
        start_btn = QPushButton('Start Game', self)
        start_btn.resize(500, BUTTON_HEIGHT)
        start_btn.move(250, 370)
        start_btn.clicked.connect(self.start_game)

        # Settings
        settings_btn = QPushButton('Settings', self)
        settings_btn.resize(500, BUTTON_HEIGHT)
        settings_btn.move(250, 460)

        # Settings Submenu
        settings_menu = QMenu()
        settings_btn.setMenu(settings_menu)

        # 2 Player Option
        self.multiplayer = self.add_menu(settings_menu, "Multiplayer", True)

        # Difficulty Menu
        difficulty = settings_menu.addMenu("Difficulty")

        # Easy
        self.easy = self.add_menu(difficulty, "Easy", True)

        # Normal
        self.normal = self.add_menu(difficulty, "Normal", True)
        self.normal.toggle()

        # Hard
        self.hard = self.add_menu(difficulty, "Hard", True)

        # Uncheck other difficulties if one is checked
        self.easy.triggered.connect(self.uncheck)
        self.normal.triggered.connect(self.uncheck)
        self.hard.triggered.connect(self.uncheck)

        # Map Editor
        editMap_btn = QPushButton('Map Editor', self)
        editMap_btn.resize(500, BUTTON_HEIGHT)
        editMap_btn.move(250, 550)
        editMap_btn.clicked.connect(self.start_map_creator)

        # Quit
        quit_btn = QPushButton('Quit', self)
        quit_btn.resize(500, BUTTON_HEIGHT)
        quit_btn.move(250, 640)
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

        start_btn.setStyleSheet(buttonstyle)
        settings_btn.setStyleSheet(buttonstyle)
        editMap_btn.setStyleSheet(buttonstyle)
        quit_btn.setStyleSheet(buttonstyle)
        settings_menu.setStyleSheet(buttonstyle)

        self.show()

    def uncheck(self):
        # if no difficulty is checked -> check normal
        if (not self.easy.isChecked()) == \
           (not self.normal.isChecked()) == \
           (not self.hard.isChecked()):
            self.normal.setChecked(True)

        # if easy is selected
        elif self.sender() == self.easy:

            # uncheck other difficulties
            self.normal.setChecked(False)
            self.hard.setChecked(False)

        # if normal is selected
        elif self.sender() == self.normal:

            # uncheck other difficulties
            self.easy.setChecked(False)
            self.hard.setChecked(False)

        # if hard is selected
        elif self.sender() == self.hard:

            # uncheck other difficulties
            self.easy.setChecked(False)
            self.normal.setChecked(False)

    def add_menu(self, menu, name, checkable):
        submenu = QAction(name, self)
        menu.addAction(submenu)
        submenu.setCheckable(checkable)

        return submenu

    def centerWindowOnScreen(self):
        outerRect = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        outerRect.moveCenter(centerOfScreen)
        self.move(outerRect.topLeft())

    def start_game(self):
        self.hide()
        self.game_window = RoboArena.RoboArena()

    def start_map_creator(self):
        self.hide()
        self.map_creator = MapCreator.MapCreator()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()
