import os
from libs.worker import download_file
from qfluentwidgets import (CardWidget, TitleLabel, BodyLabel, InfoBadge, InfoBar, IconWidget,
                             PushButton, TogglePushButton, InfoBarPosition, CaptionLabel
                            )
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from typing import Literal

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
                duration=5000
            )
        elif os.path.exists(f"data/files/{self.title}.pdf"):
            os.system(f"start data/files/{self.title}.pdf")
        else:
            download_file(f"https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com{self.pdf_file}", f"data/files/{self.title}.pdf", f"正在下载{self.title}", parent=self._parent) 
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
                duration=5000
            )
        elif os.path.exists(f"data/files/{self.title}.docx"):
            os.system(f"start data/files/{self.title}.docx")
        else:
            download_file(f"https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com{self.word_file}", f"data/files/{self.title}.docx", f"正在下载{self.title}", parent=self._parent)
            self.download_word_button.setText("查看Word文件")

    def viewWeb(self):
        os.system(f"start https://www.jingshibang.com/home/detailPaper/?id={self.id}&title={self.title}")
    
    def viewPdf(self):
        os.system(f"start https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com{self.pdf_file}")

    def refreshButton(self):
        if os.path.exists(f"data/files/{self.title}.pdf"):
            self.download_pdf_button.setText("查看PDF文件")
        else:
            self.download_pdf_button.setText("下载PDF文件")
        
        if os.path.exists(f"data/files/{self.title}.docx"):
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
        collects = self.config.get("collects", [])

        item = [self.id, self.title]
        if item in collects:
            collects.remove(item)
            self.collect_button.setText("收藏")
        else:
            collects.append(item)
            self.collect_button.setText("取消收藏")

        self.config.set("collects", collects)

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
                 is_hot: bool
                 ):
        
        self.config = {
            "id": id,
            "title": title,
            "view": view,
            "download": download,
            "upload_time": upload_time,
            "price": price,
            "subject": subject,
            "year": year,
            "grade": grade,
            "type": type,
            "is_hot": is_hot
        }

        

