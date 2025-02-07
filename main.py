from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
import sys
from libs.pages import SearchPage, LocalPage, CollectsPage, SettingsPage
from libs.log import create_logger
from libs.worker import SearchWorker
import datetime
import json


search_count = 0
now = datetime.datetime.now() # 获取当前时间
logger = create_logger(__name__, # 创建日志记录器
                       file_logger_name=f"{now.strftime('%Y-%m-%d')}.log") # 设置日志文件名

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BeijingTiKu") # 设置窗口标题

        self.searchInterface = SearchPage(self)
        self.searchInterface.setObjectName("searchInterface")
        self.searchInterface.search_button.clicked.connect(self.search) # 连接搜索按钮的点击事件到search函数


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

    def search(self):
        global search_count

        self.searchInterface.search_button.setEnabled(False)
        self.searchInterface.progress.setVisible(True)

        keyword = self.searchInterface.search_input.text()
        limit = 20
        page = self.searchInterface.page
        subject = self.searchInterface.subject_input.currentText()
        grade = self.searchInterface.grade_input.currentText()
        type = self.searchInterface.type_input.currentText()
        time = self.searchInterface.time_input.value()
        place = self.searchInterface.region_input.currentText()

        if type == "全部":
            type = ""
        
        if place == "北京":
            place = ""

        logger.info(
            f"Start searching with args: {keyword=} {subject=} {grade=} {type=} {time=} {place=} {page=} {limit=}",
            extra={"type_name":f"searchWorker-{search_count}"})
        
        def finished(data):
            global search_count

            self.searchInterface.search_button.setEnabled(True)
            self.searchInterface.progress.setVisible(False)


            if data[0]:
                # print(json.dumps(data[1][0], indent=4, ensure_ascii=False))
                logger.info(f"Search completed with {len(data[1])} results.", extra={"type_name":f"searchWorker-{search_count}"})
                self.searchInterface.showContentData(data[1])
            else:
                logger.warning(f"Search failed with error: {data[1]}", extra={"type_name":f"searchWorker-{search_count}"})

            search_count += 1

            
        self.searchWorker = SearchWorker(keyword, subject, grade, type, time, place, page, limit)
        self.searchWorker.finished.connect(finished)
        self.searchWorker.start()

        



        
if __name__ == "__main__":
    logger.info("App Started.")
    try:
        app = QApplication(sys.argv)

        w = MainWindow()
        # print(w)
        w.show()

        result = app.exec_()

        if result == 0:
            logger.info(f"App Closed with code {result}.")
        else:
            logger.error(f"App Closed with code {result}")
        
        sys.exit(result)
    except Exception as e:
        logger.error(f"An error occured while running: {e.__class__.__name__}.")
        logger.exception(e)
 