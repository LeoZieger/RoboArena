from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PathUtil import getPath


# Popup where you can insert the name of a map
class NameInput(QtWidgets.QInputDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 600, 200)
        self.setLabelText("Please enter the map-name below!")
        self.setWindowTitle("Save File")
        self.setWindowIcon(QIcon(getPath("res", "blue_tank.png")))
        self.show()
