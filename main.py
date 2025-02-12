import sys
from datetime import datetime
from libs.pages_logical import SearchPage, LocalPage, CollectsPage, SettingsPage, Preferred
from libs.log import create_logger
from libs.worker import SearchWorker

from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from utility.config import JsonConfig


search_count = 0

now = datetime.now() # 获取当前时间
logger = create_logger(__name__, # 创建日志记录器
                       file_logger_name=f"{now.strftime('%Y-%m-%d')}.log") # 设置日志文件名

config = JsonConfig("config.json")

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BeijingTiKu") # 设置窗口标题

        self.searchInterface = SearchPage(config, self)
        self.searchInterface.setObjectName("searchInterface")
        self.searchInterface.search_button.clicked.connect(lambda: self.search(True)) # 连接搜索按钮的点击事件到search函数
        
        year = datetime.now().year
        self.searchInterface.time_input.setRange(2000, year) # 设置时间输入框的范围
        self.searchInterface.time_input.setValue(year) 
        
        self.preferredInterface = Preferred(config, self)
        self.preferredInterface.setObjectName("preferredInterface")

        self.searchInterface.page_back_button.clicked.connect(lambda: self.searchInterface.backPage(self.search)) # 连接后退按钮的点击事件到backPage函数
        self.searchInterface.page_forward_button.clicked.connect(lambda: self.searchInterface.nextPage(self.search)) # 连接前进按钮的点击事件到nextPage函数

        self.localInterface = LocalPage(self)
        self.localInterface.setObjectName("localInterface")

        self.collectsInterface = CollectsPage(self)
        self.collectsInterface.setObjectName("collectsInterface")

        self.settingInterface = SettingsPage(self)
        self.settingInterface.setObjectName("settingInterface")

        self.initNavigation()
         
    def initNavigation(self):

        self.addSubInterface(self.searchInterface, FIF.DOCUMENT, "试卷")
        self.addSubInterface(self.preferredInterface, FIF.FLAG, "优选")

        self.addSubInterface(self.localInterface, FIF.FOLDER, "本地")
        self.addSubInterface(self.collectsInterface, FIF.HEART, "收藏")


        self.addSubInterface(self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)

    def search(self, get_total=True):
        global search_count

        if get_total:
            self.searchInterface.page = 1

        self.searchInterface.search_button.setEnabled(False)
        self.searchInterface.page_back_button.setEnabled(False)
        self.searchInterface.page_forward_button.setEnabled(False)
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
            self.searchInterface.page_back_button.setEnabled(True)
            self.searchInterface.page_forward_button.setEnabled(True)


            if data[0]:
                if get_total:
                    if data[2] % 20 == 0:
                        self.searchInterface.max_page = data[2] // 20
                    else:
                        self.searchInterface.max_page = data[2] // 20 + 1

                
                    logger.info(f"Search completed with {len(data[1])} results. total: {data[2]}", extra={"type_name":f"searchWorker-{search_count}"})
                else:
                    logger.info(f"Search completed with {len(data[1])} results. ", extra={"type_name":f"searchWorker-{search_count}"})
                
                self.searchInterface.page_label.setText(f"{self.searchInterface.page}/{self.searchInterface.max_page} 共 {data[2]} 条")

                self.searchInterface.showContentData(data[1])
                
            else:
                logger.warning(f"Search failed with error: {data[1]}", extra={"type_name":f"searchWorker-{search_count}"})

            search_count += 1

            
        self.searchWorker = SearchWorker(keyword, subject, grade, type, time, place, page, limit, get_total)
        self.searchWorker.finished.connect(finished)
        self.searchWorker.start()


        
if __name__ == "__main__":
    logger.info("App Started.")
    try:
        app = QApplication(sys.argv)

        w = MainWindow()
        
        w.show()

        profiler.disable() 
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats(20)   # 显示耗时前20的函数

        result = app.exec_()

        if result == 0:
            logger.info(f"App Closed with code {result}.")
        else:
            logger.error(f"App Closed with code {result}")
        
        sys.exit(result)
    except Exception as e:
        logger.error(f"An error occured while running: {e.__class__.__name__}.")
        logger.exception(e)
 