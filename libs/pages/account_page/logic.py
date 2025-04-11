from .ui import AccountPage
from libs.consts import *
from PySide6.QtGui import QImage, QPixmap
from qfluentwidgets import MessageBox
from ...worker.login import LoginWorker
from ...config import config


class AccountPage(AccountPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.login_worker = LoginWorker()

        self.login_worker.got_qrcode.connect(self.workerGotQrcode)
        self.login_worker.logined.connect(self.workerLogined)
        self.login_worker.error.connect(self.workerError)
        self.login_worker.got_avator.connect(self.workerGotAvator)

        self.login_window.showEvent = self.workerStart
        self.login_window.closeEvent = self.windowClose

        self.logout_button.clicked.connect(self.logout)

    def windowClose(self, event):
        self.login_worker.__stop__ = True

    def logout(self):
        config.set(CONFIG_ACCOUNT_LOGIN, False)
        config.set(CONFIG_ACCOUNT_NAME, "")
        config.set(CONFIG_ACCOUNT_PHONE, "")
        config.set(CONFIG_ACCOUNT_IS_VIP, False)
        config.set(CONFIG_ACCOUNT_TOKEN, "")

        self.changeButton()
        self.changeText()
        self.changeToken()

    def workerStart(self, event):
        self.login_worker.start()

    def workerGotQrcode(self, data):
        # self.login_window.qrcode_label.setFixedSize(128, 128)
        self.login_window.loading.hide()

        image = QImage().fromData(data)
        image = image.scaled(
            256,
            256,
        )
        self.login_window.qrcode_label.setPixmap(QPixmap.fromImage(image))

    def workerLogined(self, data):
        config.set(CONFIG_ACCOUNT_LOGIN, True)
        config.set(CONFIG_ACCOUNT_TOKEN, data[0])
        config.set(CONFIG_ACCOUNT_NAME, data[1])
        config.set(CONFIG_ACCOUNT_PHONE, data[2])
        config.set(CONFIG_ACCOUNT_IS_VIP, data[3])

    def workerError(self, data):
        match data[0]:
            case "getQrcode":
                window = MessageBox("登录失败", f"获取二维码失败：\n{data[1]}", self)
                window.cancelButton.hide()
                window.exec()
            case "login":
                window = MessageBox("登录失败", f"登录失败：\n{data[1]}", self)
                window.cancelButton.hide()
                window.exec()
            case "avator":
                window = MessageBox("登录失败", f"获取头像失败：\n{data[1]}", self)
                window.cancelButton.hide()
                window.exec()
            case _:
                pass

        self.login_window.close()

    def workerGotAvator(self, data):

        self.login_window.close()

        self.changeButton()
        self.changeText()
        self.changeToken()
