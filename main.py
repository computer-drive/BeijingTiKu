import sys
import os
from datetime import datetime
from libs.pages import MainWindow
from libs.log import create_logger
from PyQt5.QtWidgets import QApplication
from utility.config import JsonConfig
from libs.except_hook import except_hook
from libs.consts import *
    

sys.excepthook = except_hook

search_count = 0

now = datetime.now() # 获取当前时间
logger = create_logger(LOGGER_NAME, # 创建日志记录器
                       file_logger_name=f"{now.strftime('%Y-%m-%d')}.log") # 设置日志文件名

config = JsonConfig(CONFIG_PATH)

for path in DEPEND_PATH:
    if not os.path.exists(path):
        logger.warning(f"Dependency path {path} not found, creating...")
        os.mkdir(path)

if __name__ == "__main__":
    logger.info("App Started.")

    app = QApplication(sys.argv)

    w = MainWindow(config, logger)
        
    w.show()

    result = app.exec_()

    logger.info(f"App Closed with code {result}")
        
    sys.exit(result)

