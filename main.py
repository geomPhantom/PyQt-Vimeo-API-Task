import sys    
from PyQt5 import QtWidgets
import ssl
from LoginWindow_Controller import LoginWindow_

ssl._create_default_https_context = ssl._create_unverified_context


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    login_window = LoginWindow_()  # Создаём объект класса ExampleApp
    login_window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
