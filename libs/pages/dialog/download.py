from qfluentwidgets import (BodyLabel)
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from ...widgets.download_button import DownloadButton
from . import Dialog
from typing import Literal
import os
from libs.consts import *

class DownloadDialog(Dialog):
    def __init__(self, name:str, types_url:dict[Literal["word", "pptx", "pdf"], str], config, logger, parent=None):
        super().__init__(f"查看和下载", f"{name}", config, logger, parent)

        self.name = name
        self.types_url = types_url

        self.config = config
        self.logger = logger

        self.initUi()

    def initUi(self):
        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        for key, value in self.types_url.items():
            downloaded = False
            if key == "word":
                if os.path.exists(f"{FILE_PATH}{self.name}.docx"):
                    downloaded = True
            else:
                # print(f"{FILE_PATH}{self.name}{key}")
                if os.path.exists(f"{FILE_PATH}{self.name}.{key}"):
                    downloaded = True

            h_layout.addWidget(DownloadButton(self.name, key, value, downloaded))

        self.content_layout.addLayout(h_layout)

                    
        