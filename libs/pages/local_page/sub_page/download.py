from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel

class LocalDownloadSubPage(QWidget):

    # TODO: 获取所有下载内容，并显示
    def __init__(self, parent=None):
        super().__init__(parent)

        v_layout  = QVBoxLayout()

        v_layout.addWidget(SubtitleLabel("下载"))

        self.setLayout(v_layout)