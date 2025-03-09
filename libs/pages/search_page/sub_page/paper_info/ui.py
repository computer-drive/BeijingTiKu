from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import Qt, QUrl, QObject
from qfluentwidgets import (
    BodyLabel, TitleLabel, LargeTitleLabel, TransparentToolButton
)
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *

class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def interceptRequest(self, info):
        print(f"Intercepting request to {info.requestUrl().toString()}")
        info.setHttpHeader(b"Authorization", self.token)
        info.setHttpHeader(b"Authori-Zation", self.token)


class PaperInfoSubPage(QFrame):
    def __init__(self, config, parent=None):
        super().__init__(parent)

        self.parent_ = parent
        self.config = config

        self.initUi()
        

    def initWebview(self):
        self.webview = QWebEngineView()
        
        # 创建独立的 Profile 和 Page
        self.profile = QWebEngineProfile()
        self.page = QWebEnginePage(self.profile, self.webview)

        # 创建并保留拦截器实例
        token = f"Bearer {self.config.get(CONFIG_ACCOUNT_TOKEN, '')}".encode()
        self.interceptor = RequestInterceptor(token)  # 保存为实例变量
        self.profile.setUrlRequestInterceptor(self.interceptor)

        self.webview.setPage(self.page)

    
    def initUi(self):
        self.initWebview()

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
        
        # WebView 配置
        self.webview.setSizePolicy(
            QSizePolicy.Expanding,  # 水平策略
            QSizePolicy.Expanding   # 垂直策略
        )
        main_layout.addWidget(self.webview, stretch=1)  # 添加拉伸系数
        
        # 右侧信息面板
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)
        
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

        self.webview.setUrl(QUrl(f"{DOWNLOAD_URL}{data["pdf_answer"]}"))

        self.title_label.setText(data["store_name"])
        
        self.info0_label.setText(data["store_name"])
        self.info1_label.setText(f"下载量: {data['upload_num']} 浏览量: {data['browse']}")
        self.info2_label.setText(f"作者：{data['upload_people']} 上传时间：{data['add_time']}")




