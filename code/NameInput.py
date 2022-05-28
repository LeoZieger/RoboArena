from PyQt5 import QtWidgets


class NameInput(QtWidgets.QInputDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 600, 200)
        self.show()
