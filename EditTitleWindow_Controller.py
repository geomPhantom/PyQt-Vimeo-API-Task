from PyQt5 import QtWidgets
import EditTitleWindow


class EditTitleWindow_(QtWidgets.QDialog, EditTitleWindow.Ui_editTitleWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
