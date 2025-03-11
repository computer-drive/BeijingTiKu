from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget
from .sub_page import SearchSubPage, PaperInfoSubPage
from libs.consts import *



class SearchPage(QFrame):
    def __init__(self, config, logger, parent=None): 

        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.parent_ = parent

        self.page = 1
        self.max_page = 0

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        v_layout.addWidget(self.stacked_widget)

        self.stacked_widget.addWidget(SearchSubPage(self.config, self.logger, self))
        self.stacked_widget.addWidget(PaperInfoSubPage(self.config, self))
    
    def changePage(self, page):
        self.stacked_widget.setCurrentIndex(page)

    def showPaperInfo(self, data):
        self.stacked_widget.widget(1).setData(data)
        self.changePage(1)