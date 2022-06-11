from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMainWindow, QApplication, QLabel
import PyQt5.QtCore

import sys
import RoboArena
import MapCreator


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 250
BUTTON_HEIGHT = 50

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        name_label = QLabel("ROBO ARENA", self)
        name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        name_label.resize(WINDOW_WIDTH, BUTTON_HEIGHT)
        name_label.move(0, 0)

        start_btn = QPushButton('Start Game', self)
        start_btn.resize(WINDOW_WIDTH, BUTTON_HEIGHT)
        start_btn.move(0, 50)
        start_btn.clicked.connect(self.start_game)

        settings_btn = QPushButton('Settings', self)
        settings_btn.resize(int(WINDOW_WIDTH / 2), 50)
        settings_btn.move(0, 100)

        difficulty_btn = QPushButton('Difficulty', self)
        difficulty_btn.resize(int(WINDOW_WIDTH / 2), 50)
        difficulty_btn.move(int(WINDOW_WIDTH / 2), 100)

        editRob_btn = QPushButton('Edit Robot', self)
        editRob_btn.resize(int(WINDOW_WIDTH / 2), 50)
        editRob_btn.move(0, 150)

        editMap_btn = QPushButton('Map Editor', self)
        editMap_btn.resize(int(WINDOW_WIDTH / 2), 50)
        editMap_btn.move(int(WINDOW_WIDTH / 2), 150)
        editMap_btn.clicked.connect(self.start_map_creator)

        quit_btn = QPushButton('Quit', self)
        quit_btn.resize(WINDOW_WIDTH, 50)
        quit_btn.move(0, 200)
        quit_btn.clicked.connect(QApplication.instance().quit)
        
        self.show()
    
    def start_game(self):
        self.hide()
        self.game_window = RoboArena.RoboArena()
        self.game_window.show()

    def start_map_creator(self):
        self.hide()
        self.map_creator = MapCreator.MapCreator()
        self.map_creator.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    app.exec_()
