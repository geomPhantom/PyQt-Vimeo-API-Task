from PyQt5 import QtWidgets
import MoveVideoWindow


class MoveVideoWindow_(QtWidgets.QDialog, MoveVideoWindow.Ui_moveVideoWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
