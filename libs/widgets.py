from typing import Callable
import os
from libs.worker import download_file, GetPreferredInfoWorker
from libs.cached import cachePapersInfo, cachePreferredInfo
from qfluentwidgets import (CardWidget, TitleLabel, BodyLabel, InfoBadge, InfoBar, IconWidget,
                             PushButton, TogglePushButton, InfoBarPosition, CaptionLabel,
                             IndeterminateProgressRing, SubtitleLabel
                            )
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from typing import Literal

from libs.consts import *

class CardBase(CardWidget):
    def __init__(self, left: QWidget, right: QWidget, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.left_widget = left
        self.right_widget = right

        h_layout = QHBoxLayout()

        h_layout.addWidget(left)

        h_layout.addWidget(right)

        self.setLayout(h_layout)

class ItemCard(CardBase):
    def __init__(self, config, logger, parent=None):
        super().__init__(self, QWidget(), QWidget(), config, logger, parent)

        self.config = config
        self.logger = logger

        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.left_widget.setLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.right_widget.setLayout(self.right_layout)


    def addText(self, content:str, style:Literal["title", "subtitle", "body", "badge"], color:str="", style:str=""):
        match style:
            case "title":
                label = TitleLabel(content)
            case "subtitle":
                label = SubtitleLabel(content)
            case "body":
                label = BodyLabel(content)
            case "badge":
                label = InfoBadge.custom(content, color, color)
        
        if style != "":
            label.setStyleSheet(style)

        self.left_layout.addWidget(label)


    def addButton(self, button: PushButton | list[tuple[PushButton, Callable]]):
        if isinstance(button, PushButton):
            self.right_layout.addWidget(button)
        elif isinstance(button, list):
            button_layout = QHBoxLayout()

            for btn, func in button:
                btn.clicked.connect(func)
                button_layout.addWidget(btn)

            self.right_layout.addLayout(button_layout)

        else:
            raise TypeError("button must be a PushButton or a list of (PushButton, Callable)")


class ItemCard(CardWidget):
    def __init__(self,
                id: int,
                title: str,
                view: int,
                download: int,
                author: str, 
                upload_time: str, 
                is_hot: bool, 
                is_real: bool, 
                pdf_file: str,
                word_file: str,
                config,
                full_info: dict,
                parent=None
                ):
        
        

        self.id = id
        self.title = title
        self.view = view
        self.download = download
        self.author = author
        self.upload_time = upload_time
        self.is_hot = is_hot
        self.is_real = is_real
        self.pdf_file = pdf_file
        self.word_file = word_file
        self._parent = parent
        self.config = config
        self.full_info = full_info
        
        super().__init__(parent)
        
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        h_layout.addLayout(left_layout)

        title = TitleLabel(title)
        title.setStyleSheet("font-size: 16px;")
        left_layout.addWidget(title)
        left_layout.addWidget(BodyLabel(f"下载量：{download} 浏览量：{view}"))
        left_layout.addWidget(BodyLabel(f"作者：{author} 上传时间：{upload_time}"))

        hot_label = InfoBadge.custom("热门", "#FE143B", "#FE143B")
        real_label = InfoBadge.custom("真题", "#FF9D37", "#FF9D37")

        info_layout = QHBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if is_hot:
            info_layout.addWidget(hot_label, alignment=Qt.AlignmentFlag.AlignLeft)
        if is_real:
            info_layout.addWidget(real_label, alignment=Qt.AlignmentFlag.AlignLeft)
        left_layout.addLayout(info_layout)


        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        h_layout.addLayout(right_layout)

        
        self.download_pdf_button = PushButton(FIF.DOWNLOAD, "下载PDF文件")
        self.download_pdf_button.clicked.connect(self.downloadPdf)
        if pdf_file == "":
            self.download_pdf_button.setEnabled(False)
        right_layout.addWidget(self.download_pdf_button)

        self.download_word_button = PushButton(FIF.DOWNLOAD, "下载Word文件")
        self.download_word_button.clicked.connect(self.downloadWord)
        if word_file == "":
            self.download_word_button.setEnabled(False)
        right_layout.addWidget(self.download_word_button)

        view_layout = QHBoxLayout()
        right_layout.addLayout(view_layout)

        self.view_web_button = PushButton(FIF.CLOUD, "查看网页")
        self.view_web_button.clicked.connect(self.viewWeb)
        view_layout.addWidget(self.view_web_button)

        self.view_pdf_button = PushButton(FIF.DOCUMENT, "预览网页")
        self.view_pdf_button.clicked.connect(self.viewPdf)
        view_layout.addWidget(self.view_pdf_button)

        self.collect_button = TogglePushButton(FIF.HEART, "收藏")
        self.collect_button.clicked.connect(self.collectButton)
        right_layout.addWidget(self.collect_button)

        self.refreshButton()

    def downloadPdf(self):
        # print(self._parent)
        if self.pdf_file == "":
            InfoBar.error(
                "无法下载PDF文件",
                "该试卷无PDF格式的文件",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self._parent,
                duration=INFO_BAR_DURATION
            )
        elif os.path.exists(f"{FILE_PATH}{self.title}.pdf"):
            os.system(f"start {FILE_PATH}/{self.title}.pdf")
        else:
            download_file(f"{DOWNLOAD_URL}{self.pdf_file}", f"{FILE_PATH}{self.title}.pdf", f"正在下载{self.title}", parent=self._parent) 
            self.download_pdf_button.setText("查看PDF文件")

    def downloadWord(self):
        if self.word_file == "":
            InfoBar.error(
                "无法下载Word文件",
                "该试卷无Word格式的文件",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self._parent,
                duration=INFO_BAR_DURATION
            )
        elif os.path.exists(f"{FILE_PATH}{self.title}.docx"):
            os.system(f"start {FILE_PATH}{self.title}.docx")
        else:
            download_file(f"{DOWNLOAD_URL}{self.word_file}", f"{FILE_PATH}{self.title}.docx", f"正在下载{self.title}", parent=self._parent)
            self.download_word_button.setText("查看Word文件")

    def viewWeb(self):
        os.system(f"start {WEB_URL}?id={self.id}&title={self.title}")
    
    def viewPdf(self):
        os.system(f"start {DOWNLOAD_URL}{self.pdf_file}")

    def refreshButton(self):
        if os.path.exists(f"{FILE_PATH}{self.title}.pdf"):
            self.download_pdf_button.setText("查看PDF文件")
        else:
            self.download_pdf_button.setText("下载PDF文件")
        
        if os.path.exists(f"{FILE_PATH}{self.title}.docx"):
            self.download_word_button.setText("查看Word文件")
        else:
            self.download_word_button.setText("下载Word文件")

        collects = self.config.get("collects", [])
        item = [self.id, self.title]
        if item in collects:
            self.collect_button.toggle()
            self.collect_button.setText("取消收藏")
        else:
            self.collect_button.setText("收藏")

    def collectButton(self):
        collects = self.config.get(CONFIG_COLLECTS, [])

        item = [self.id, self.title]
        if item in collects:
            collects.remove(item)
            self.collect_button.setText("收藏")
        else:
            collects.append(item)
            cachePapersInfo([self.full_info])

            self.collect_button.setText("取消收藏")

        self.config.set(CONFIG_COLLECTS, collects)

class SettingCard(CardWidget):
    def __init__(self, icon, title:str, content:str, actions:list[QWidget], action_layout_type:Literal["h_layout", "v_layout"]="h_layout",parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMidLineWidth(400)

        icon = IconWidget(icon)
        icon.setFixedSize(24, 24)

        title = BodyLabel(title)
        content = CaptionLabel(content)
        content.setTextColor("#606060", "#d2d2d2")

        h_layout = QHBoxLayout()

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        left_layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        content_layout.addWidget(title, 0, Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(content, 0, Qt.AlignmentFlag.AlignLeft)

        left_layout.addLayout(content_layout)

        action_widget = QWidget()
        if action_layout_type == "h_layout":
            action_layout = QHBoxLayout()   
        else:
            action_layout = QVBoxLayout() 


        for action in actions:
            action_layout.addWidget(action)

        action_widget.setLayout(action_layout)

        h_layout.addLayout(left_layout, stretch=1)
        h_layout.addWidget(action_widget, stretch=0)

        

        self.setLayout(h_layout)


class PreferredCard(CardWidget):
    def __init__(self,
                 id: int,
                 title: str,
                 view: int,
                 download: int,
                 upload_time: str,
                 price: float,
                 subject: str,
                 year: int,
                 grade: str,
                 type: str,
                 is_hot: bool,
                 config,
                 logger, 
                 full_info: dict,
                 parent=None
                 ):
        
        super().__init__(parent)
        
        self.id = id
        self.title = title 
        self.view = view 
        self.download = download 
        self.upload_time = upload_time 
        self.price = price 
        self.subject = subject 
        self.year = year 
        self.grade = grade 
        self.type = type 
        self.is_hot = is_hot 
        self.full_info = full_info

        self.pdf_file = ""
        self.word_file = ""

        self.config = config
        self.logger = logger

        self._parent= parent

        self.initUi()
        self.initWorker()
        

    def workerFinished(self, data):
        self.logger.info(f"Got preferred info(id:{self.id}) success.")

        if data[0]:
            
            if data[1]["storeInfo"]["pdf_paper"] == "":
                if data[1]["storeInfo"]["pdf_answer"] == "":
                    self.download_pdf_button.setEnabled(False)
                    self.view_pdf_button.setEnabled(False)
                else:
                    self.pdf_file = data[1]["storeInfo"]["pdf_answer"]
            else:
                self.pdf_file = data[1]["storeInfo"]["pdf_paper"]


            if data[1]["storeInfo"]["word_paper"] == "":    
                if data[1]["storeInfo"]["word_answer"] == "":
                    self.download_word_button.setEnabled(False)
                else:
                    self.word_file = data[1]["storeInfo"]["word_answer"]
            else:
                self.word_file = data[1]["storeInfo"]["word_paper"]

            self.showButton()
            
        else:
            self.showError("出现错误")

    def initWorker(self):
        self.worker = GetPreferredInfoWorker(self.id, self.config, self.logger)

        self.worker.finished.connect(self.workerFinished)

        self.worker.start()

    def initUi(self):
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        h_layout.addLayout(left_layout)

        title = TitleLabel(self.title)
        title.setStyleSheet("font-size: 16px;")
        left_layout.addWidget(title)

        left_layout.addWidget(BodyLabel(f"{self.grade} {self.subject} {self.year} {self.type}"))
        left_layout.addWidget(BodyLabel(f"下载量：{self.download} 浏览量：{self.view}"))
        left_layout.addWidget(BodyLabel(f"上传时间：{self.upload_time}"))

        price_label = BodyLabel(self.updatePrice())
        price_label.setStyleSheet("font-size: 16px; color: #fe690e;")
        
        left_layout.addWidget(price_label)

        hot_label = InfoBadge.custom("热门", "#FE143B", "#FE143B")
        

        info_layout = QHBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if self.is_hot:
            info_layout.addWidget(hot_label, alignment=Qt.AlignmentFlag.AlignLeft)
        left_layout.addLayout(info_layout)


        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        h_layout.addLayout(right_layout)

        
        self.download_pdf_button = PushButton(FIF.DOWNLOAD, "下载PDF文件")
        self.download_pdf_button.clicked.connect(self.downloadPdf)
        self.download_pdf_button.hide()
        right_layout.addWidget(self.download_pdf_button)

        self.download_word_button = PushButton(FIF.DOWNLOAD, "下载Word文件")
        self.download_word_button.clicked.connect(self.downloadWord)
        self.download_word_button.hide()
        right_layout.addWidget(self.download_word_button)

        view_layout = QHBoxLayout()
        right_layout.addLayout(view_layout)

        self.view_web_button = PushButton(FIF.CLOUD, "查看网页")
        self.view_web_button.clicked.connect(self.viewWeb)
        self.view_web_button.hide()
        view_layout.addWidget(self.view_web_button)

        self.view_pdf_button = PushButton(FIF.DOCUMENT, "预览网页")
        self.view_pdf_button.clicked.connect(self.viewPdf)
        self.view_pdf_button.hide()
        view_layout.addWidget(self.view_pdf_button)

        self.collect_button = TogglePushButton(FIF.HEART, "收藏")
        self.collect_button.clicked.connect(self.collectButton)
        self.collect_button.hide()
        right_layout.addWidget(self.collect_button)

        self.loading = IndeterminateProgressRing()
        self.loading.setFixedSize(45, 45)
        right_layout.addWidget(self.loading)

        self.error_label = BodyLabel(ERROR_TEXT)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("font-size: 40px;")
        self.error_label.hide()
        right_layout.addWidget(self.error_label)

        self.error_info_label = BodyLabel("出错了，请重试")
        self.error_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_info_label.setStyleSheet("font-size: 20px;")
        self.error_info_label.hide()
        right_layout.addWidget(self.error_info_label)

        self.refreshButton()
    
    def showButton(self):
        self.download_pdf_button.show()
        self.download_word_button.show()
        self.view_web_button.show()
        self.view_pdf_button.show()
        self.collect_button.show()
        self.loading.hide()

    def showError(self, info):

        self.download_pdf_button.hide()
        self.download_word_button.hide()
        self.view_web_button.hide()
        self.view_pdf_button.hide()
        self.collect_button.hide()
        self.loading.hide()

        self.error_label.show()
        self.error_info_label.show()

        self.error_info_label.setText(info)

    def updatePrice(self):
        if self.price == 0:
            return "免费"
        else:
            return f"￥{self.price}"
        
    def downloadPdf(self):
        # print(self._parent)
        if self.pdf_file == "":
            InfoBar.error(
                "无法下载PDF文件",
                "该试卷无PDF格式的文件",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self._parent,
                duration=INFO_BAR_DURATION
            )
        elif os.path.exists(f"{FILE_PATH}{self.title}.pdf"):
            os.system(f'{FILE_PATH}{self.title}.pdf"')
        else:
            download_file(f"{DOWNLOAD_URL}{self.pdf_file}", f"{FILE_PATH}{self.title}.pdf", f"正在下载{self.title}", parent=self._parent) 
            self.download_pdf_button.setText("查看PDF文件")

    def downloadWord(self):
        if self.word_file == "":
            InfoBar.error(
                "无法下载Word文件",
                "该试卷无Word格式的文件",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self._parent,
                duration=INFO_BAR_DURATION

            )
        elif os.path.exists(f"{FILE_PATH}{self.title}.docx"):
            os.system(f'"{FILE_PATH}{self.title}.docx')
        else:
            download_file(f"{DOWNLOAD_URL}{self.word_file}", f"data/files/{self.title}.docx", f"正在下载{self.title}", parent=self._parent)
            self.download_word_button.setText("查看Word文件")

    def viewWeb(self):
        os.system(f'start {WEB_URL}?id={self.id}&title={self.title}')
    
    def viewPdf(self):
        os.system(f"start {DOWNLOAD_URL}{self.pdf_file}")

    def refreshButton(self):
        if os.path.exists(f"{FILE_PATH}{self.title}.pdf"):
            self.download_pdf_button.setText("查看PDF文件")
        else:
            self.download_pdf_button.setText("下载PDF文件")
        
        if os.path.exists(f"{FILE_PATH}{self.title}.docx"):
            self.download_word_button.setText("查看Word文件")
        else:
            self.download_word_button.setText("下载Word文件")

        collects = self.config.get(CONFIG_COLLECTS, [])
        item = [self.id, self.title]
        if item in collects:
            self.collect_button.toggle()
            self.collect_button.setText("取消收藏")
        else:
            self.collect_button.setText("收藏")

    def collectButton(self):
        collects = self.config.get(CONFIG_COLLECTS, [])

        item = [self.id, self.title]
        if item in collects:
            collects.remove(item)
            self.collect_button.setText("收藏")
        else:
            collects.append(item)
            cachePreferredInfo([self.full_info])

            self.collect_button.setText("取消收藏")

        self.config.set(CONFIG_COLLECTS, collects)

class MaterialIcon(QIcon):
    def __init__(self, name: str, width: int = 32, height: int = 32):
        if os.path.exists(f"{ICON_PATH}{name}.svg"):
            super().__init__(QPixmap(f"{ICON_PATH}{name}.svg").scaled(width, height, Qt.KeepAspectRatio))

        else:
            raise ValueError(f"Icon {name} not found.")

