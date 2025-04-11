from PySide6.QtGui import QIcon
from qfluentwidgets import NavigationItemPosition, FluentWindow
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *
from ..config import config
from ..log import logger


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        from .search_page.logic import SearchPage
        from .preferred_page.logic import Preferred
        from .local_page.logic import LocalPage
        from .settings_page.logic import SettingsPage
        from .account_page.logic import AccountPage

        self.setWindowTitle(WINDOW_TITLE)  # 设置窗口标题

        self.searchInterface = SearchPage(self)
        self.searchInterface.setObjectName("searchInterface")

        self.preferredInterface = Preferred(self)
        self.preferredInterface.setObjectName("preferredInterface")

        self.localInterface = LocalPage(self)
        self.localInterface.setObjectName("localInterface")

        self.settingInterface = SettingsPage(self)
        self.settingInterface.setObjectName("settingInterface")

        self.avatorInterface = AccountPage(self)
        self.avatorInterface.setObjectName("avatorInterface")

        self.initNavigation()

        self.setStyleSheet(
            """
                LargeTitleLabel {
                    font-weight: normal;
                }
        """
        )

    def initNavigation(self):

        self.addSubInterface(self.searchInterface, FIF.DOCUMENT, "试卷")
        self.addSubInterface(self.preferredInterface, FIF.FLAG, "优选")

        self.addSubInterface(self.localInterface, FIF.FOLDER, "本地")

        self.initAvator()

        self.addSubInterface(
            self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )

    def initAvator(self):

        logined = config.get(CONFIG_ACCOUNT_LOGIN, False)
        name = config.get(CONFIG_ACCOUNT_NAME, "未登录")

        if logined:
            avator = QIcon(AVATOR_PATH)
        else:
            avator = FIF.PEOPLE

        self.addSubInterface(
            self.avatorInterface, avator, name, NavigationItemPosition.BOTTOM
        )
