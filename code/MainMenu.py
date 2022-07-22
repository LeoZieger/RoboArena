from PyQt5.QtWidgets import QPushButton, QApplication, \
                            QMainWindow, QLabel, QDesktopWidget, \
                            QMenu, QAction, QActionGroup
from PyQt5.QtGui import QMovie, QPainter
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
        self.background_gif = QMovie("res/BackgroundGif.gif")
        self.background_gif.setScaledSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_gif.frameChanged.connect(self.repaint)
        self.background_gif.start()

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
        self.selectedMap = self.all_maps[0]
        map_menu = settings_menu.addMenu("Maps")
        map_group = QActionGroup(self)

        # Create button for all maps
        for x in self.all_maps:
            self.x = self.add_group(map_menu, map_group, x, True)
            self.map_objects.append(self.x)

        map_menu.triggered.connect(self.mapClicked)
        self.map_objects[0].toggle()

        # Difficulty Menu
        difficulty = settings_menu.addMenu("Difficulty")
        difficulty_group = QActionGroup(self)
        self.selectedDifficulty = "normal"
        difficulty.triggered.connect(self.difficultyClicked)

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

    def paintEvent(self, event):
        currentFrame = self.background_gif.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def mapClicked(self, action):
        self.selectedMap = action.text()

    def difficultyClicked(self, action):
        self.selectedDifficulty = action.text()

    def get_maps(self):
        self.all_maps = next(walk('maps'), (None, None, []))[2]
        for x in range(len(self.all_maps)):
            self.all_maps[x] = self.all_maps[x][:-5]

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
        self.game_window = RoboArena.RoboArena(self.multiplayer.isChecked(),
                                               map_name=self.selectedMap)
        # diff=self.selectedDifficulty)
        SoundFX.initMenuSoundtrack(self, False)

    def start_map_creator(self):
        self.hide()
        self.map_creator = MapCreator.MapCreator()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()
