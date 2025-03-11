from qfluentwidgets import (MessageBoxBase, IndeterminateProgressRing,
                             TitleLabel, BodyLabel)
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt
from libs.consts import *


class LoadingWindow(MessageBoxBase):
    def __init__(self, title:str, content:str, parent=None):
        super().__init__(parent)

        self.setMinimumSize(500,300)

        progress = IndeterminateProgressRing()
        progress.setFixedSize(*PROGRESS_RING_SIZE)
        self.viewLayout.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)

        content_layout = QVBoxLayout()

        content_layout.addWidget(TitleLabel(title), alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_label = BodyLabel(content)
        content_layout.addWidget(self.content_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.viewLayout.addLayout(content_layout)


        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()