from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from .....widgets.pdf_view import PdfWidget
from PySide6.QtCore import Qt, QUrl
from qfluentwidgets import BodyLabel, TitleLabel, LargeTitleLabel, TransparentToolButton
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *


class PaperInfoSubPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name = None
        self.url = None

        self.parent_ = parent

        self.initUi()

    def initPdfView(self):

        self.pdf_widget = PdfWidget()

        return self.pdf_widget

    def initUi(self):

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)  # 移除布局边距

        # 顶部布局
        top_layout = QHBoxLayout()
        self.back_button = TransparentToolButton(FIF.LEFT_ARROW)
        self.back_button.clicked.connect(lambda: self.parent_.changePage(0))
        top_layout.addWidget(self.back_button)
        self.title_label = LargeTitleLabel("No Data")
        top_layout.addWidget(self.title_label)
        v_layout.addLayout(top_layout)

        # 主内容区域
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        main_layout.addWidget(self.initPdfView(), stretch=1)  # 添加拉伸系数

        # 右侧信息面板
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.info0_label = TitleLabel("No Data")
        self.info0_label.setStyleSheet("font-size: 20px;")
        info_layout.addWidget(self.info0_label)

        self.info1_label = BodyLabel("下载量: No Data 浏览量: No Data")
        info_layout.addWidget(self.info1_label)

        self.info2_label = BodyLabel("作者：No Data 上传时间：No Data")
        info_layout.addWidget(self.info2_label)

        main_layout.addLayout(info_layout)

        v_layout.addLayout(main_layout, stretch=1)  # 添加垂直拉伸系数
        self.setLayout(v_layout)

    def setData(self, data):

        # self.webview.setUrl(QUrl(f"{DOWNLOAD_URL}{data["pdf_answer"]}"))

        self.title_label.setText(data["store_name"])

        self.info0_label.setText(data["store_name"])
        self.info1_label.setText(
            f"下载量: {data['upload_num']} 浏览量: {data['browse']}"
        )
        self.info2_label.setText(
            f"作者：{data['upload_people']} 上传时间：{data['add_time']}"
        )

        self.name = data["store_name"]

        # TODO: 有答案从pdf_paper中取值

        self.url = data["pdf_answer"]

        self.pdf_widget.setData(self.name, self.url)
        self.pdf_widget.id = data["id"]

        self.pdf_widget.showPdf()
