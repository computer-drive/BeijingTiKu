from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from qfluentwidgets import TitleLabel, BodyLabel, LargeTitleLabel, CardWidget, PrimaryPushButton
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *
from ..login_window import LoginWindow

class AccountPage(QFrame):
    def __init__(self, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.initUI()

        self.login_window = LoginWindow(config, logger, self)
        self.login_window.hide()


    def initUI(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        layout.addWidget(LargeTitleLabel("账户"))

        layout.addWidget(self.initCard())

        self.token_label = BodyLabel("Token:未登录")
        self.changeToken()
        self.token_label.setMaximumWidth(400)
        layout.addWidget(self.token_label)

        layout.addWidget(TitleLabel("为什么需要登录？"))
        layout.addWidget(BodyLabel("北京题库中的一个api，需要获取登录后的token，否则无法使用."))
        layout.addWidget(BodyLabel("api为北京题库获取优选信息的接口，登录后才可获取下载地址(若不使用优选功能或可以自行下载，则可不进行登录)."))
        layout.addWidget(BodyLabel("登录后token保存在本地，注意不要泄露你的token"))

        
        

    def login(self):
        self.login_window.show()


    def changeToken(self):
        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)
        token = self.config.get(CONFIG_ACCOUNT_TOKEN, "")

        # print(logined)
        if logined:
            self.token_label.setText(f"Token:{token}")
        else:
            self.token_label.setText("Token:未登录")
    
    def initCard(self):
        card = CardWidget()

        layout = QHBoxLayout()
        card.setLayout(layout)

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(left_layout)

        self.icon = QLabel()
        left_layout.addWidget(self.icon)

        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.addLayout(info_layout)

        self.name_label = TitleLabel()
        info_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.phone_label = BodyLabel()
        info_layout.addWidget(self.phone_label, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(right_layout)

        self.logout_button = PrimaryPushButton("退出登录")
        self.logout_button.setVisible(False)
        right_layout.addWidget(self.logout_button)

        self.login_button = PrimaryPushButton("登录")
        self.login_button.clicked.connect(self.login)
        self.login_button.setVisible(False)
        right_layout.addWidget(self.login_button)

        self.changeButton()

        self.changeText()

        return card

    def changeButton(self):
        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)

        if logined:
            self.login_button.hide()
            self.logout_button.show()
        else:
            self.login_button.show()
            self.logout_button.hide()

    def changeText(self):
        name = self.config.get(CONFIG_ACCOUNT_NAME, "未登录")
        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)
        is_vip = self.config.get(CONFIG_ACCOUNT_IS_VIP, False)
        phone = self.config.get(CONFIG_ACCOUNT_PHONE, "")

        if logined:
            avator = QIcon(AVATOR_PATH)

            if is_vip:
                vip_str = "会员"
            else:
                vip_str = "非会员"

        else:
            avator = FIF.PEOPLE.icon()
            vip_str = ""

        if phone is None:
            phone_str = "未绑定"
        else:
            phone_str = phone

        self.icon.setPixmap(avator.pixmap(32, 32))

        self.name_label.setText(name)
        self.phone_label.setText(f"{phone_str} {vip_str}")

