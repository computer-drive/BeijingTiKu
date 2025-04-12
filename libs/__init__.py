import os
from .log import logger
from .consts import *
from .cached import initCacheFile
from PySide6.QtWidgets import QApplication
from .pages.main_window import MainWindow
from PySide6.QtCore import Qt

QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)


class BeijingTiku:

    def prepare(self):
        # 检查依赖路径是否存在，不存在则创建
        for path in DEPEND_PATH:
            if not os.path.exists(path):
                logger.warning(f"Dependency path {path} not found, creating...")
                os.mkdir(path)

        initCacheFile()

    def run(self):
        self.prepare()

        self.app = QApplication([]) # 创建应用程序实例

        self.mainWindow = MainWindow() # 创建主窗口实例

        self.mainWindow.show() # 显示主窗口

        logger.info("Application running.")

        result = self.app.exec()
        logger.info(f"Application exited with code {result}")
        return result
