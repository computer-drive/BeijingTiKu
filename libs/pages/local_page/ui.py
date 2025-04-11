from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout
from qfluentwidgets import LargeTitleLabel, Pivot
from PySide6.QtCore import Qt
from .sub_page.collects import LocalCollectSubPage
from .sub_page.download import LocalDownloadSubPage
from .sub_page.history import LocalHistorySubPage


class LocalPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pages: dict[str, QWidget] = {
            "Collects": LocalCollectSubPage(self),
            "Downloads": LocalDownloadSubPage(self),
            "History": LocalHistorySubPage(self),
        }

        v_layout = QVBoxLayout()
        self.v_layout = v_layout
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(v_layout)

        v_layout.addWidget(LargeTitleLabel("本地"))

        self.pivot = Pivot()
        self.pivot.addItem("CollectsPage", "收藏", lambda: self.changePage("Collects"))
        self.pivot.addItem(
            "DownloadsPage", "下载", lambda: self.changePage("Downloads")
        )
        self.pivot.addItem("HistoryPage", "历史", lambda: self.changePage("History"))
        v_layout.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignCenter)

        self.initPage("Collects")

    def initPage(self, default: str):
        # print(self.pages)
        for page, widget in self.pages.items():
            self.v_layout.addWidget(widget)
            if page == default:
                widget.show()
            else:
                widget.hide()

    def changePage(self, name):

        if name not in self.pages:
            raise ValueError("Page not found")
        else:
            for page, widget in self.pages.items():
                if widget is not None:
                    if page == name:
                        widget.show()
                    else:
                        widget.hide()
