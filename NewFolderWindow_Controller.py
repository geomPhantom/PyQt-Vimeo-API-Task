from PyQt5 import QtWidgets
import NewFolderWindow


class NewFolderWindow_(QtWidgets.QDialog, NewFolderWindow.Ui_newFolderWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
