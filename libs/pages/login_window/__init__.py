from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import (MessageBoxBase, TitleLabel, BodyLabel, ToolButton,
                             IndeterminateProgressRing,
                               )
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *

class LoginWindow(MessageBoxBase):
    def __init__(self, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout = QHBoxLayout()
        self.viewLayout.addLayout(top_layout)

        top_left_layout = QVBoxLayout()
        top_layout.addLayout(top_left_layout)

        top_left_layout.addWidget(TitleLabel("登录"))

        info_label = BodyLabel("请使用微信扫码登录")
        info_label.setStyleSheet("font-size: 20px;")
        top_left_layout.addWidget(info_label)

        close_button = ToolButton(FIF.CLOSE)
        close_button.clicked.connect(self.close)
        top_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)


        content_layout = QVBoxLayout()
        self.viewLayout.addLayout(content_layout)

        content_layout.addStretch()

        self.loading = IndeterminateProgressRing()
        self.loading.setFixedSize(*PROGRESS_RING_SIZE)
        content_layout.addWidget(self.loading, alignment=Qt.AlignmentFlag.AlignCenter)

        self.qrcode_label = QLabel()
        content_layout.addWidget(self.qrcode_label, alignment=Qt.AlignmentFlag.AlignCenter)

        content_layout.addStretch()

        self.yesButton.hide()
        self.cancelButton.hide()


        self.widget.setMinimumSize(400, 400)

        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()

        self.showEvent = self.whenShow

    def whenShow(self, event):

        self.loading.show()

        self.qrcode_label.clear()