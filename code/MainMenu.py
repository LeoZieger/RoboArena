from PyQt5.QtWidgets import QPushButton, QApplication, \
                            QMainWindow, QLabel, QDesktopWidget, \
<<<<<<< HEAD
                            QMenu, QAction
=======
                            QMenu
>>>>>>> 0df1a3655c2ecddfbb8c2ee9f01b6567776be710
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

        #SubWindow Settings
<<<<<<< HEAD
        def add_menu(self, menu, sub, name):
            submenu = sub
            submenu = QAction(name, self)
            menu.addAction(submenu)

        settings_menu = QMenu()
        settings_btn.setMenu(settings_menu)
        difficulty = settings_menu.addMenu("Difficulty")
        #easy = QAction("Easy", self)
        #difficulty.addAction(easy)
        add_menu(self, difficulty, "easy", "Easy")
        #easy.trigger.connect(QApplication.instance().quit)
        normal = QAction("Normal", self)
        difficulty.addAction(normal)
=======
        settings = [
            {'Difficulty': ["Easy", "Normal", "Hard"]},
            {'Keybindings': ['Movement', 'Shoot']}
        ]
        settings_menu = QMenu()
        settings_btn.setMenu(settings_menu)
        self.add_menu(settings, settings_menu)
>>>>>>> 0df1a3655c2ecddfbb8c2ee9f01b6567776be710

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

<<<<<<< HEAD
=======
    # Adds a menu
    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)


>>>>>>> 0df1a3655c2ecddfbb8c2ee9f01b6567776be710
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()