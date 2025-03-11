from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import (MessageBoxBase, TitleLabel, BodyLabel, ToolButton,
                             IndeterminateProgressRing,
                               )
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *

class Dialog(MessageBoxBase):
    def __init__(self, title, tips, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout = QHBoxLayout()
        self.viewLayout.addLayout(top_layout)

        top_left_layout = QVBoxLayout()
        top_layout.addLayout(top_left_layout)

        top_left_layout.addWidget(TitleLabel(title))

        info_label = BodyLabel(tips)
        info_label.setStyleSheet("font-size: 20px;")
        top_left_layout.addWidget(info_label)

        close_button = ToolButton(FIF.CLOSE)
        close_button.clicked.connect(self.close)
        top_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)


        self.content_layout = QVBoxLayout()
        self.viewLayout.addLayout(self.content_layout)
        self.content_layout.addStretch()

        self.yesButton.hide()
        self.cancelButton.hide()

        # self.widget.setMinimumSize(400, 400)

        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()


