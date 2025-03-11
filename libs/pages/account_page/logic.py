from .ui import AccountPage
from libs.consts import *
from PySide6.QtGui import QImage, QPixmap
from qfluentwidgets import MessageBox
from ...worker.login import LoginWorker

class AccountPage(AccountPage):
    def __init__(self, config, logger, parent=None):
        super().__init__(config, logger, parent)


        self.login_worker = LoginWorker(logger)

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
        self.config.set(CONFIG_ACCOUNT_LOGIN, False)
        self.config.set(CONFIG_ACCOUNT_NAME, "")
        self.config.set(CONFIG_ACCOUNT_PHONE, "")
        self.config.set(CONFIG_ACCOUNT_IS_VIP, False)
        self.config.set(CONFIG_ACCOUNT_TOKEN, "")

        self.changeButton()
        self.changeText()
        self.changeToken()

    def workerStart(self, event):
        self.login_worker.start()

    def workerGotQrcode(self, data):
        # self.login_window.qrcode_label.setFixedSize(128, 128)
        self.login_window.loading.hide()

        image = QImage().fromData(data)
        image = image.scaled(256, 256,)
        self.login_window.qrcode_label.setPixmap(QPixmap.fromImage(image))

    def workerLogined(self, data):
        self.config.set(CONFIG_ACCOUNT_LOGIN, True)
        self.config.set(CONFIG_ACCOUNT_TOKEN, data[0])
        self.config.set(CONFIG_ACCOUNT_NAME, data[1])
        self.config.set(CONFIG_ACCOUNT_PHONE, data[2])
        self.config.set(CONFIG_ACCOUNT_IS_VIP, data[3])
    
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
