from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout
from qfluentwidgets import BodyLabel, ToolButton, HyperlinkButton
from qfluentwidgets import FluentIcon as FIF
from ..worker.download import Downloader
from .loading_widget import LoadingWidget
from libs.consts import *
import os


class PdfView(QPdfView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pdf_document = QPdfDocument(parent)

        self.setDocument(self.pdf_document)

    def load(self, pdf_path):
        self.pdf_document.load(pdf_path)

    def changePage(self, index):
        """
        index 以 1 开始
        """
        count = self.pdf_document.pageCount()

        if index - 1 > count:
            raise ValueError(f"The largest page is {count}, not {index -1 }")

        self.pageNavigator().jump(index - 1, QPointF(0, 0))


class PdfWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.id = None

        self.name = None
        self.url = None

        self.initUi()

    def setData(self, name, url):
        self.name = name
        self.url = url

        self.show_web_button.setUrl(f"{DOWNLOAD_URL}{self.url}")

    def initUi(self):
        v_layout = QVBoxLayout()

        self.stack_widget = QStackedWidget()
        v_layout.addWidget(self.stack_widget)

        self.pdf_view = PdfView()
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.stack_widget.addWidget(self.pdf_view)

        self.loading_widget = LoadingWidget(
            ERROR_TEXT, "发生错误", SEARCH_NULL_TEXT, "未找到", self
        )
        self.stack_widget.addWidget(self.loading_widget)

        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        v_layout.addLayout(action_layout)

        self.zoom_out_button = ToolButton(FIF.ZOOM_OUT)
        self.zoom_out_button.clicked.connect(self.zoomOut)
        action_layout.addWidget(self.zoom_out_button)

        self.zoom_label = BodyLabel("100%")
        action_layout.addWidget(self.zoom_label)

        self.zoom_in_button = ToolButton(FIF.ZOOM_IN)
        self.zoom_in_button.clicked.connect(self.zoomIn)
        action_layout.addWidget(self.zoom_in_button)

        self.show_web_button = HyperlinkButton("You need set data first", "查看网页")
        action_layout.addWidget(self.show_web_button)

        self.setLayout(v_layout)

    def zoomIn(self):
        current_zoom = self.pdf_view.zoomFactor()
        self.pdf_view.setZoomFactor(current_zoom + 0.1)

        self.zoom_label.setText(f"{int((current_zoom + 0.1) * 100)}%")

    def zoomOut(self):
        current_zoom = self.pdf_view.zoomFactor()
        self.pdf_view.setZoomFactor(current_zoom - 0.1)

        self.zoom_label.setText(f"{int((current_zoom - 0.1) * 100)}%")

    def loadPdf(self):
        self.pdf_view.pdf_document.load(f"{FILE_PATH}{self.name}.pdf")

    def workerFinished(self, data):
        if data[0]:
            self.stack_widget.setCurrentIndex(0)

            self.loadPdf()
        else:
            # TODO：输出日志
            self.loading_widget.showError()

    def showPdf(self):

        if self.name is None or self.url is None:
            raise Exception("You need call self.setData first.")

        if os.path.exists(f"{FILE_PATH}{self.name}.pdf"):
            # self.pdf_view.show()
            # self.loading_widget.hide()
            self.stack_widget.setCurrentIndex(0)

            self.loadPdf()

        else:
            # self.pdf_view.hide()
            # self.loading_widget.show()
            self.loading_widget.showLoading()
            # self.loading_widget.show()
            self.stack_widget.setCurrentIndex(1)

            self.worker = Downloader(
                f"{DOWNLOAD_URL}{self.url}", f"{FILE_PATH}{self.name}.pdf"
            )
            self.worker.finished.connect(self.workerFinished)
            self.worker.start()
