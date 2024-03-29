from PyQt5.QtWidgets import QPushButton, QApplication, \
                            QMainWindow, QLabel, QDesktopWidget, \
                            QMenu, QAction, QActionGroup
from PyQt5.QtGui import QMovie, QPainter, QFontDatabase, QFont, QIcon
from PyQt5.QtCore import QSize
import PyQt5.QtCore
import sys
import RoboArena
import MapCreator
from SoundFX import SoundFX
from os import walk
from PathUtil import getDir, getPath

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

        # Windowtitle + Icon
        self.setWindowTitle('RoboArena')
        self.setWindowIcon(QIcon(getPath("res", "blue_tank.png")))

        # Background
        self.background_gif = QMovie(getPath("res", "BackgroundGif.gif"))
        self.background_gif.setScaledSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_gif.frameChanged.connect(self.repaint)
        self.background_gif.start()

        # Soundtrack
        SoundFX.initMenuSoundtrack(self, True)

        # Load font
        id = QFontDatabase.addApplicationFont(getPath("res", "PixeloidMono.ttf"))
        families = QFontDatabase.applicationFontFamilies(id)
        self.font = families[0]

        # Apply font
        QApplication.setFont(QFont(self.font))

        # Headline
        name_label = QLabel("ROBO ARENA", self)
        name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        name_label.resize(WINDOW_WIDTH, BUTTON_HEIGHT)
        name_label.move(0, 150)
        name_label.setStyleSheet(
            "color: white;"
            "font-size: 100px;"
        )

        # Start Game Button
        start_btn = QPushButton('Start Game', self)
        start_btn.resize(500, BUTTON_HEIGHT)
        start_btn.move(250, 370)
        start_btn.clicked.connect(self.start_game)

        # Settings Button
        settings_btn = QPushButton('Settings', self)
        settings_btn.resize(500, BUTTON_HEIGHT)
        settings_btn.move(250, 460)

        # Settings Submenu Button
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
        self.selectedDifficulty = "Normal"
        difficulty.triggered.connect(self.difficultyClicked)

        # Easy
        self.easy = self.add_group(difficulty, difficulty_group, "Easy", True)

        # Normal
        self.normal = self.add_group(difficulty, difficulty_group, "Normal", True)
        self.normal.toggle()

        # Hard
        self.hard = self.add_group(difficulty, difficulty_group, "Hard", True)

        # Map Editor
        editor_btn = QPushButton('Map Editor', self)
        editor_btn.resize(500, BUTTON_HEIGHT)
        editor_btn.move(250, 550)

        self.get_maps()
        self.map_editor_objects = []
        self.selectedEditorMap = "New Map"
        edit_menu = QMenu()
        editor_btn.setMenu(edit_menu)
        map_editor_group = QActionGroup(self)

        # Create menu to edit maps
        self.map_editor_objects.append(self.add_group(edit_menu,
                                                      map_editor_group,
                                                      "New Map",
                                                      True))
        # Button for each map
        for x in self.all_maps:
            self.x = self.add_group(edit_menu, map_editor_group, x, True)
            self.map_editor_objects.append(self.x)

        edit_menu.triggered.connect(self.mapClickedEditor)
        self.map_editor_objects[0].toggle()

        # Quit Button
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
        editor_btn.setStyleSheet(buttonstyle)
        quit_btn.setStyleSheet(buttonstyle)
        settings_menu.setStyleSheet(buttonstyle)
        edit_menu.setStyleSheet(buttonstyle)

        self.show()

    # paintEvent for animated background
    def paintEvent(self, event):
        currentFrame = self.background_gif.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    # Set the variable to the button you clicked
    def mapClicked(self, action):
        self.selectedMap = action.text()

    def mapClickedEditor(self, action):
        self.selectedEditorMap = action.text()
        self.start_map_creator()

    def difficultyClicked(self, action):
        self.selectedDifficulty = action.text()

    # Reads all map files from maps folder
    def get_maps(self):
        self.all_maps = next(walk(getDir("maps")), (None, None, []))[2]
        for x in range(len(self.all_maps)):
            self.all_maps[x] = self.all_maps[x][:-5]

    # Add certain menu to button + Checkbox
    def add_group(self, menu, group, name, checkable):
        submenu = QAction(name, self)
        menu.addAction(submenu)
        submenu.setCheckable(checkable)
        group.addAction(submenu)
        return submenu

    # Centers Window
    def centerWindowOnScreen(self):
        outerRect = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        outerRect.moveCenter(centerOfScreen)
        self.move(outerRect.topLeft())

    # Starts RoboArena
    def start_game(self):
        SoundFX.transitionSound(self)
        self.hide()
        self.game_window = RoboArena.RoboArena(self.multiplayer.isChecked(),
                                               map_name=self.selectedMap,
                                               difficulty=self.selectedDifficulty)
        SoundFX.initMenuSoundtrack(self, False)

    # Starts Map Editor
    def start_map_creator(self):
        self.hide()
        self.map_creator = MapCreator.MapCreator(self.selectedEditorMap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()
