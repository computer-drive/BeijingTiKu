from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import (
    MessageBoxBase,
    TitleLabel,
    BodyLabel,
    ToolButton,
    IndeterminateProgressRing,
)
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF
from . import Dialog
from libs.consts import *


class LoginDialog(Dialog):
    def __init__(self, parent=None):
        super().__init__("登录", "请使用微信扫码登录", parent)

        self.loading = IndeterminateProgressRing()
        self.loading.setFixedSize(*PROGRESS_RING_SIZE)
        self.content_layout.addWidget(
            self.loading, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.qrcode_label = QLabel()
        self.content_layout.addWidget(
            self.qrcode_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.content_layout.addStretch()

        self.yesButton.hide()
        self.cancelButton.hide()

        self.widget.setMinimumSize(400, 400)

        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()

        self.showEvent = self.whenShow

    def whenShow(self, event):

        self.loading.show()

        self.qrcode_label.clear()
