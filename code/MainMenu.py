from PyQt5.QtWidgets import QPushButton, QApplication, \
                            QMainWindow, QLabel, QDesktopWidget, \
                            QMenu, QAction, QActionGroup
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import PyQt5.QtCore

import sys
import RoboArena
import MapCreator
from SoundFX import SoundFX
from os import walk

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
        SoundFX.initMenuSoundtrack(self, True)

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

        # Mode Option
        mode = settings_menu.addMenu("Mode")
        mode_group = QActionGroup(self)
        self.singleplayer = self.add_group(mode, mode_group, "Singleplayer", True)
        self.singleplayer.toggle()
        self.multiplayer = self.add_group(mode, mode_group, "Multiplayer", True)

        # Change map
        self.get_maps()
        self.map_objects = []
        self.map_list = None
        map_menu = settings_menu.addMenu("Maps")
        map_group = QActionGroup(self)

        # Create button for all maps
        for x in self.all_maps:
            self.x = self.add_group(map_menu, map_group, x, True)
            self.x.triggered.connect(self.actionClicked)
            self.map_objects.append(self.x)
            print(self.map_objects)

        self.map_objects[0].toggle()

        # Difficulty Menu
        difficulty = settings_menu.addMenu("Difficulty")
        difficulty_group = QActionGroup(self)

        # Easy
        self.easy = self.add_group(difficulty, difficulty_group, "Easy", True)

        # Normal
        self.normal = self.add_group(difficulty, difficulty_group, "Normal", True)
        self.normal.toggle()

        # Hard
        self.hard = self.add_group(difficulty, difficulty_group, "Hard", True)

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

        # Apply stylesheet to the buttons
        start_btn.setStyleSheet(buttonstyle)
        settings_btn.setStyleSheet(buttonstyle)
        editMap_btn.setStyleSheet(buttonstyle)
        quit_btn.setStyleSheet(buttonstyle)
        settings_menu.setStyleSheet(buttonstyle)

        self.show()

    def actionClicked(self, action):
        print(action.text())

    def choose_map(self):
        for x in range(len(self.map_list)):
            if self.map_list[x].isChecked():
                return self.map_list[x].sende

    def get_maps(self):
        self.all_maps = next(walk('maps'), (None, None, []))[2]
        for x in range(len(self.all_maps)):
            self.all_maps[x] = self.all_maps[x][:-5]

    def change_map(self, map):
        self.map = map

    def add_group(self, menu, group, name, checkable):
        submenu = QAction(name, self)
        menu.addAction(submenu)
        submenu.setCheckable(checkable)
        group.addAction(submenu)

        return submenu

    def centerWindowOnScreen(self):
        outerRect = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        outerRect.moveCenter(centerOfScreen)
        self.move(outerRect.topLeft())

    def start_game(self):
        SoundFX.transitionSound(self)
        self.hide()
        self.game_window = RoboArena.RoboArena(self.multiplayer.isChecked())
        SoundFX.initMenuSoundtrack(self, False)

    def start_map_creator(self):
        self.hide()
        self.map_creator = MapCreator.MapCreator()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()
