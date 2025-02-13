import sys
from datetime import datetime
from libs.pages import MainWindow
from libs.log import create_logger
from PyQt5.QtWidgets import QApplication
from utility.config import JsonConfig


search_count = 0

now = datetime.now() # 获取当前时间
logger = create_logger("Main", # 创建日志记录器
                       file_logger_name=f"{now.strftime('%Y-%m-%d')}.log") # 设置日志文件名

config = JsonConfig("config.json")

if __name__ == "__main__":
    logger.info("App Started.")
    try:
        app = QApplication(sys.argv)

        w = MainWindow(config, logger)
        
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
 