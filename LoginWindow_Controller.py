from PyQt5 import QtWidgets
import LoginWindow
import os
import requests
from requests.auth import HTTPBasicAuth
from cryptography.fernet import Fernet
from TheMainWindow_Controller import TheMainWindow_
from credentials import client_id, client_secret, key


def check_if_allowed_access(authorize_link, user_code, device_code):
    post_req = requests.post(authorize_link,
                             auth=HTTPBasicAuth(client_id, client_secret),
                             data={'user_code': user_code, 'device_code': device_code})
    if post_req.status_code == requests.codes.ok:
        data_from_req = post_req.json()
        token = data_from_req['access_token']

        f = open(os.environ['HOME'] + '/Documents/vimeo_token', 'wb')
        f.write(Fernet(key).encrypt(token.encode()))
        f.close()
        return True
    else:
        print(str(post_req.status_code) + " " + post_req.reason)
        return False


def token_already_saved():
    return os.path.isfile(os.environ['HOME'] + '/Documents/vimeo_token')


def auth():
    if token_already_saved():
        return True
    else:
        post_req1 = requests.post('https://api.vimeo.com/oauth/device',
                                  auth=HTTPBasicAuth(client_id, client_secret),
                                  data={'grant_type': 'device_grant', 'scope': 'private create edit delete interact public'})
        if post_req1.status_code == requests.codes.ok:
            data_from_req1 = post_req1.json()
            print(data_from_req1)
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Auth")
            msg.setText("Visit " + data_from_req1['activate_link'] + " and enter the code " + data_from_req1['user_code'] +
                        '. After that click OK here. The code expires in ' + str(data_from_req1['expires_in']) + ' seconds.')
            # msg.buttonClicked.connect(check_if_authorized)
            x = msg.exec_()
            return check_if_allowed_access(data_from_req1['authorize_link'], data_from_req1['user_code'], data_from_req1['device_code'])
        else:
            print(str(post_req1.status_code) + " " + post_req1.reason)
            return False


class LoginWindow_(QtWidgets.QMainWindow, LoginWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.theMainWindow = None
        self.pushButton.clicked.connect(self.login_button_clicked)

    def login_button_clicked(self):
        if auth():
            print("Auth success!")
            self.theMainWindow = TheMainWindow_()
            self.theMainWindow.show()
            # create vimeo.VimeoClient instance
            # open main window
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Auth failed')
            error_dialog.exec_()
