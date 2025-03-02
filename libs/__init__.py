import os
from datetime import datetime
from .log import create_logger
from .consts import *
from .cached import initCacheFile
from utility.config import JsonConfig
from PyQt5.QtWidgets import QApplication
from .pages.main_window import MainWindow

print("Initiating <Moudle> libs.__init__")
print(f"    -<Class> BeijingTiku")
class BeijingTiku:
    def __init__(self):
        
        self.logger = self.createLogger()
        self.config = self.loadConfig()


    def createLogger(self):
        now = datetime.now() # 获取当前时间
        logger = create_logger(LOGGER_NAME, # 创建日志记录器
                        file_logger_name=f"{now.strftime('%Y-%m-%d')}.log") # 设置日志文件名
        
        return logger
    
    def loadConfig(self):
        config = JsonConfig(CONFIG_PATH)

        return config
    
    def prepare(self):
        for path in DEPEND_PATH:
            if not os.path.exists(path):
                self.logger.warning(f"Dependency path {path} not found, creating...")
                os.mkdir(path)

        initCacheFile()

        

    def run(self):
        self.prepare()

        self.app = QApplication([])


        self.mainWindow = MainWindow(self.config, self.logger)
        self.mainWindow.show()

        self.logger.info("Application running.")

        result = self.app.exec_()
        self.logger.info(f"Application exited with code {result}")
        return result
