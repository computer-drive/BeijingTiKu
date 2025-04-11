from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SubtitleLabel


class LocalHistorySubPage(QWidget):
    # TODO: 获取所有历史记录，并显示
    def __init__(self, parent=None):
        super().__init__(parent)

        v_layout = QVBoxLayout()

        v_layout.addWidget(SubtitleLabel("历史"))

        self.setLayout(v_layout)
