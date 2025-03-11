from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel

class LocalCollectSubPage(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)

        self.config = config

        v_layout  = QVBoxLayout()

        v_layout.addWidget(SubtitleLabel("收藏"))

        self.setLayout(v_layout)

    def onShow(self):
        pass