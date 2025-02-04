from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
import sys
from libs.pages import SearchPage, LocalPage, CollectsPage, SettingsPage
from libs.log import create_logger
import datetime

now = datetime.datetime.now()
logger = create_logger(__name__,
                       file_logger_name=f"{now.strftime('%Y-%m-%d')}.log")

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BeijingTiKu")

        self.searchInterface = SearchPage(self)
        self.searchInterface.setObjectName("searchInterface")

        self.localInterface = LocalPage(self)
        self.localInterface.setObjectName("localInterface")

        self.collectsInterface = CollectsPage(self)
        self.collectsInterface.setObjectName("collectsInterface")

        self.settingInterface = SettingsPage(self)
        self.settingInterface.setObjectName("settingInterface")

        self.initNavigation()
        
    def initNavigation(self):
        self.addSubInterface(self.searchInterface, FIF.SEARCH, "搜索")
        self.addSubInterface(self.localInterface, FIF.FOLDER, "本地")
        self.addSubInterface(self.collectsInterface, FIF.HEART, "收藏")

        self.addSubInterface(self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)

if __name__ == "__main__":
    logger.info("App Started.")
    try:
        app = QApplication(sys.argv)

        w = MainWindow()
        w.show()

        result = app.exec_()

        if result == 0:
            logger.info(f"App Closed with code {result}.")
        else:
            logger.error(f"App Closed with code {result}")
        
        sys.exit(result)
    except Exception as e:
        logger.error(f"An error occured while runningapp: {e.__class__.__name__}.")
        logger.exception(e)
 