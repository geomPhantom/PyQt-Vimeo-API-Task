from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
import os
import requests
from cryptography.fernet import Fernet
import vimeo
import urllib.request
import TheMainWindow
from NewFolderWindow_Controller import NewFolderWindow_
from MoveVideoWindow_Controller import MoveVideoWindow_
from EditTitleWindow_Controller import EditTitleWindow_
from credentials import client_id, client_secret, key


def get_image_from_response(link):
    pixmap = QPixmap()
    url_data = None
    with urllib.request.urlopen(link) as url:
        url_data = url.read()
    pixmap.loadFromData(url_data)
    image = QtGui.QImage(pixmap)
    return image


class TheMainWindow_(QtWidgets.QMainWindow, TheMainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.newFolderButton.clicked.connect(self.new_folder_button_clicked)
        self.moveVideoButton.clicked.connect(self.move_video_button_clicked)
        self.editTitleButton.clicked.connect(self.edit_title_button_clicked)
        self.deleteButton.clicked.connect(self.delete_button_clicked)
        self.updateButton.clicked.connect(self.update_button_clicked)
        self.logOutButton.clicked.connect(self.logout_button_clicked)
        self.moveVideoButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.editTitleButton.setEnabled(False)

        self.client = vimeo.VimeoClient(
            token=(Fernet(key).decrypt(open(os.environ['HOME'] + '/Documents/vimeo_token', 'rb').read())).decode(),
            key=client_id,
            secret=client_secret
        )
        self.folders = []
        self.nonfolder_videos = []
        self.model = None

        self.update_treeview()

    def selection_changed(self, selected, deselected):
        if len(self.treeView.selectedIndexes()) > 0:
            self.deleteButton.setEnabled(True)
            self.editTitleButton.setEnabled(True)
            if (self.model.itemFromIndex(selected.indexes()[3])).text() == 'Video':
                self.moveVideoButton.setEnabled(True)
            else:
                self.moveVideoButton.setEnabled(False)
        else:
            self.moveVideoButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.editTitleButton.setEnabled(False)

    def update_treeview(self):
        print("Updating tree")
        self.folders = self.get_folders()
        print(self.folders)
        self.nonfolder_videos = self.get_nonfolder_videos()

        self.model = QtGui.QStandardItemModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.selection_changed)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        for folder in self.folders:
            folder_icon = QtGui.QStandardItem("")
            folder_icon.setData(folder['Thumbnail'].scaled(40, 40, QtCore.Qt.KeepAspectRatio), QtCore.Qt.DecorationRole)
            id_item = QtGui.QStandardItem(folder['ID'])
            self.model.appendRow([folder_icon, QtGui.QStandardItem(folder['Title']), id_item, QtGui.QStandardItem('Folder')])
            for video in folder['Videos']:
                thumbn = QtGui.QStandardItem("")
                thumbn.setData(video['Thumbnail'].scaled(150, 150, QtCore.Qt.KeepAspectRatio), QtCore.Qt.DecorationRole)
                folder_icon.appendRow([thumbn, QtGui.QStandardItem(video['Title']), QtGui.QStandardItem(video['ID']),
                                       QtGui.QStandardItem('Video')])

        for video in self.nonfolder_videos:
            thumbn = QtGui.QStandardItem("")
            thumbn.setData(video['Thumbnail'].scaled(150, 150, QtCore.Qt.KeepAspectRatio), QtCore.Qt.DecorationRole)
            self.model.appendRow([thumbn, QtGui.QStandardItem(video['Title']), QtGui.QStandardItem(video['ID']),
                                  QtGui.QStandardItem('Video')])

        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Thumbnail")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Title")
        self.treeView.resizeColumnToContents(0)

    def get_folders(self):
        print("Getting folders")
        projects = self.client.get('https://api.vimeo.com/me/projects').json()
        print(projects)
        folders = []
        for folder in projects['data']:
            folders.append({'ID': (folder['uri'].split("/"))[-1],
                           'Thumbnail': QtGui.QImage('folder_icon.png'),
                            'Title': folder['name'],
                            'Videos': self.get_videos_in_folder(folder['uri'])})
        return folders

    def get_videos_in_folder(self, project_path):
        print("Getting folder videos")
        # print(self.client.patch('https://api.vimeo.com' + project_path,
        #                         data={'name': project_path}))

        videos_in_folder = self.client.get('https://api.vimeo.com' + project_path + '/videos').json()
        print(videos_in_folder)
        videos = []
        for video in videos_in_folder['data']:
            videos.append({'ID': (video['uri'].split("/"))[-1],
                          'Thumbnail': get_image_from_response(video['pictures']['sizes'][1]['link']),
                           'Title': video['name']})
        return videos

    def get_nonfolder_videos(self):
        print("Getting videos")
        about_me = self.client.get('https://api.vimeo.com/me/videos').json()
        print(about_me)
        videos = []
        for video in about_me['data']:
            if video['parent_folder'] is None:
                videos.append({'ID': (video['uri'].split("/"))[-1],
                               'Thumbnail': get_image_from_response(video['pictures']['sizes'][1]['link']),
                               'Title': video['name']})
        return videos

    def add_folder(self):
        new_folder_req = self.client.post('/me/projects',
                                          data={'name': self.new_folder_window.newFolderInputField.text()})
        print("New folder req")
        new_folder_req_json = new_folder_req.json()
        if new_folder_req.status_code == requests.codes.created:
            print("New folder created successfully")
            #self.update_treeview() # too slow
            folder_icon = QtGui.QStandardItem("")
            folder_id = (new_folder_req_json['uri'].split("/"))[-1]
            folder_icon.setData(QtGui.QImage('folder_icon.png').scaled(40, 40, QtCore.Qt.KeepAspectRatio), QtCore.Qt.DecorationRole)
            self.model.appendRow([folder_icon, QtGui.QStandardItem(self.new_folder_window.newFolderInputField.text()),
                                  QtGui.QStandardItem(folder_id), QtGui.QStandardItem('Folder')])
            self.folders.append({'ID': folder_id,
                                 'Thumbnail': QtGui.QImage('folder_icon.png'),
                                 'Title': self.new_folder_window.newFolderInputField.text(),
                                 'Videos': []})
        else:
            print("Error while creating folder: " + str(new_folder_req.status_code) + " " + new_folder_req.reason)

    def new_folder_button_clicked(self):
        print("New folder button clicked")

        self.new_folder_window = NewFolderWindow_()  # Создаём объект класса ExampleApp
        self.new_folder_window.buttonBox.accepted.connect(self.add_folder)
        self.new_folder_window.show()  # Показываем окно

    def move_video(self):
        move_video_req = self.client.put('https://api.vimeo.com/me/projects/' +
                                         self.folders[self.move_video_window.foldersComboBox.currentIndex()]["ID"] +
                                         '/videos/' +
                                         self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(self.treeView.selectedIndexes()[0].row(), 2)).text()
                                         )
        #print("New folder req")
        #print(new_folder_req)
        if move_video_req.status_code == requests.codes.no_content:
            print("Video moved successfully")
            self.update_treeview()
        else:
            print("Error while moving folder: " + str(move_video_req.status_code) + " " + move_video_req.reason)

    def move_video_button_clicked(self):
        print("Move video button clicked")

        self.move_video_window = MoveVideoWindow_()
        for folder in self.folders:
            self.move_video_window.foldersComboBox.addItem(folder["Title"])
        self.move_video_window.buttonBox.accepted.connect(self.move_video)
        self.move_video_window.show()

    def edit_title(self):
        edit_title_req = None
        is_video = None
        # print(self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(self.treeView.selectedIndexes()[0].row(),3)).text())
        if (self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                self.treeView.selectedIndexes()[0].row(), 3))).text() == 'Video':
            is_video = True
            edit_title_req = self.client.patch('https://api.vimeo.com/videos/' +
                                               self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                                                   self.treeView.selectedIndexes()[0].row(), 2)).text(),
                                               data={'name': self.edit_title_window.editTitleInputField.text()})
        else:
            edit_title_req = self.client.patch('https://api.vimeo.com/me/projects/' +
                                            self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                                                self.treeView.selectedIndexes()[0].row(), 2)).text(),
                                               data={'name': self.edit_title_window.editTitleInputField.text()})
            is_video = False

        if edit_title_req.status_code == requests.codes.ok:
            print("Edit title successfully")
            #self.update_treeview()
            if is_video:
                self.model.setData(self.treeView.selectedIndexes()[1], self.edit_title_window.editTitleInputField.text())
                found = False
                for idx, video in enumerate(self.nonfolder_videos):
                    if video['ID'] == self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                                                   self.treeView.selectedIndexes()[0].row(), 2)).text():
                        self.nonfolder_videos[idx]['Title'] = self.edit_title_window.editTitleInputField.text()
                        found = True
                        break
                if not found:
                    for idx, folder in enumerate(self.folders):
                        temp_found = False
                        for jdx, video in enumerate(self.folders[idx]['Videos']):
                            if video['ID'] == self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                                                   self.treeView.selectedIndexes()[0].row(), 2)).text():
                                self.folders[idx]['Videos'][jdx]['Title'] = self.edit_title_window.editTitleInputField.text()
                                temp_found = True
                                break
                        if temp_found:
                            break
            else:
                self.model.setData(self.treeView.selectedIndexes()[1], self.edit_title_window.editTitleInputField.text())
                for idx, folder in enumerate(self.folders):
                    if folder['ID'] == self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                                                self.treeView.selectedIndexes()[0].row(), 2)).text():
                        self.folders[idx]['Title'] = self.edit_title_window.editTitleInputField.text()
                        break
        else:
            print("Error while editing title: " + str(edit_title_req.status_code) + " " + edit_title_req.reason)
        # print(len(self.treeView.selectedIndexes()))

    def edit_title_button_clicked(self):
        print("Edit title button clicked")
        self.edit_title_window = EditTitleWindow_()
        self.edit_title_window.buttonBox.accepted.connect(self.edit_title)
        self.edit_title_window.show()

    def delete_button_clicked(self):
        print("Delete button clicked")
        delete_req = None

        #print(self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(self.treeView.selectedIndexes()[0].row(),3)).text())
        if (self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                self.treeView.selectedIndexes()[0].row(), 3))).text() == 'Video':
            delete_req = self.client.delete('https://api.vimeo.com/videos/' +
                                            self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                self.treeView.selectedIndexes()[0].row(), 2)).text())
        else:
            delete_req = self.client.delete('https://api.vimeo.com/me/projects/' +
                                            self.model.itemFromIndex(self.treeView.selectedIndexes()[0].sibling(
                self.treeView.selectedIndexes()[0].row(), 2)).text())

        if delete_req.status_code == requests.codes.no_content:
            print("Delete successful")
            self.update_treeview()
        else:
            print("Error while deleting: " + str(delete_req.status_code) + " " + delete_req.reason)
        #print(len(self.treeView.selectedIndexes()))

    def update_button_clicked(self):
        print("Update button clicked")
        self.update_treeview()

    def logout_button_clicked(self):
        print("Logout button clicked")
        os.remove(os.environ['HOME'] + '/Documents/vimeo_token')
        self.close()