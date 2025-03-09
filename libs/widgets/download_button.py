import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from qfluentwidgets import BodyLabel, ProgressRing
from typing import  Literal
from libs.consts import *
from ..worker.download import Downloader


class DownloadButton(QWidget):
    def __init__(self, file_name:str, file_type:Literal["word", "pdf", "pptx"], file_url:str, downloaded:bool=False, parent=None):
        super().__init__(parent)

        self.file_type = file_type
        self.file_url = file_url
        self.file_name = file_name
        self.downloaded = downloaded

        self.mousePressEvent = self.onClick
     
        self.initUi()

    def initUi(self):
        self.v_layout = QVBoxLayout()

        self.image = BodyLabel()
        self.v_layout.addWidget(self.image, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress = ProgressRing(useAni=False)
        self.progress.setFixedSize(96, 96)
        self.progress.hide()
        self.v_layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_label = BodyLabel()
        self.info_label.setStyleSheet("font-size: 16px;")
        self.v_layout.addWidget(self.info_label, alignment=Qt.AlignmentFlag.AlignCenter)

        if self.downloaded:
            text = "查看"
        else:
            text = "下载"

        if self.file_type == "word":
            icon = QPixmap(ICON_PATHS["word"])

        elif self.file_type == "pdf":
            icon = QPixmap(ICON_PATHS["pdf"])
            
        elif self.file_type == "pptx":
            # TODO: 添加pptx图标
            pass
        else:
            raise ValueError(f"File type must be word, pdf or pptx, not {self.file_type}")
        
        icon = icon.scaled(96, 96)
        self.image.setPixmap(icon)

        self.info_label.setText(f"{text}")

        self.setLayout(self.v_layout)
    
    def onClick(self, event):
        self.progress.setValue(0)
        if self.downloaded:
            if self.file_type == "word":
                os.startfile(f"{FILE_PATH}{self.file_name}.docx")
            else:
                os.startfile(f"{FILE_PATH}{self.file_name}.{self.file_type}")
        else:
            if self.file_type == "word":
                self.worker = Downloader(f"{DOWNLOAD_URL}{self.file_url}", f"{FILE_PATH}{self.file_name}.docx")
            else:
                self.worker = Downloader(f"{DOWNLOAD_URL}{self.file_url}", f"{FILE_PATH}{self.file_name}.{self.file_type}")
            
            self.worker.finished.connect(self.onFinished)
            self.worker.update.connect(self.onUpdate)

            self.worker.start()
            self.progress.show()
            self.image.hide()

    def onFinished(self, result):
        if result[0]:
            self.info_label.setText("下载完成")
        else:
            self.info_label.setText("下载失败")

        self.progress.hide()
        self.image.show()

        self.downloaded = True

    def onUpdate(self, data):
        count, total, speed, eta, progress = data

        
        self.info_label.setText(f"{progress}%")

        self.progress.setValue(progress)
        











