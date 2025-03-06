from .card_base import ItemCard
from typing import Literal
from PyQt5.QtCore import Qt
from libs.consts import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (PushButton, TogglePushButton, BodyLabel, InfoBar,
                            InfoBarPosition, TransparentToolButton, TransparentToggleToolButton,
                             IndeterminateProgressRing)
from ..pages.dialog.download import DownloadDialog
from ..worker.preferred import GetPreferredInfoWorker
from ..worker.download import download_file
from ..cached import cachePapersInfo

import os


class ResultCard(ItemCard):
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
                full_info: dict,
                config,
                logger,
                parent=None,
                extra:str = "",
                result_type:Literal["paper", "preferred"] = "paper"
                ):
        
        super().__init__(config, logger, parent)

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
        
        self.parent_ = parent

        

        self.addText(title, "title", stylesheet="font-size: 16px;")
        self.addText(f"下载量：{download} 浏览量：{view}", "body")
        self.addText(f"作者：{author} 上传时间：{upload_time}", "body")

        if extra:
            self.addText(extra, "body")

        badges = []

        if is_hot:
            badges.append(("热门", "badge", "#FE143B", ""))
        
        if is_real:
            badges.append(("真实", "badge", "#00BFFF", ""))

        self.addTexts(badges)

        # self.download_pdf_button = self.addButton(PushButton(FIF.DOWNLOAD, "下载PDF文件"), self.downloadPdf)
        # self.download_word_button = self.addButton(PushButton(FIF.DOWNLOAD, "下载Word文件"), self.downloadWord)
        
        # self.view_web_button, self.view_pdf_button = self.addButton([
        #     (PushButton(FIF.CLOUD, "查看网页"), self.viewWeb),
        #     (PushButton(FIF.DOCUMENT, "预览网页"), self.viewPdf)
        # ])


        # self.collect_button = self.addButton(TogglePushButton(FIF.HEART, "收藏"), self.collectButton)

        self.download_button = self.addButton(TransparentToolButton(FIF.DOWNLOAD), self.downloadButton)
        self.collect_button = self.addButton(TransparentToggleToolButton(FIF.HEART), self.collectButton)

        self.clicked.connect(lambda: print("Clicked"))

        self.refreshButton()

        if result_type == "preferred":

            self.loading = IndeterminateProgressRing()
            self.loading.setFixedSize(45, 45)
            self.right_layout.addWidget(self.loading)

            self.error_label = BodyLabel(ERROR_TEXT)
            self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.error_label.setStyleSheet("font-size: 40px;")
            self.error_label.hide()
            self.right_layout.addWidget(self.error_label)

            self.error_info_label = BodyLabel("出错了，请重试")
            self.error_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.error_info_label.setStyleSheet("font-size: 20px;")
            self.error_info_label.hide()
            self.right_layout.addWidget(self.error_info_label)

            self.initWorker()

            self.download_button.hide()
            self.collect_button.hide()

    def workerFinished(self, data):
        self.logger.info(f"Got preferred info(id:{self.id}) success.")

        if data[0]:
            
            if data[1]["storeInfo"]["pdf_paper"] == "":
                if data[1]["storeInfo"]["pdf_answer"] == "":
                    self.pdf_file = None
                else:
                    self.pdf_file = data[1]["storeInfo"]["pdf_answer"]
            else:
                self.pdf_file = data[1]["storeInfo"]["pdf_paper"]


            if data[1]["storeInfo"]["word_paper"] == "":    
                if data[1]["storeInfo"]["word_answer"] == "":
                    self.word_file = None
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

    def showButton(self):
        self.download_button.show()
        self.collect_button.show()
        self.loading.hide()

    def showError(self, info):

        self.download_button.hide()
        self.collect_button.hide()
        self.loading.hide()

        self.error_label.show()
        self.error_info_label.show()

        self.error_info_label.setText(info)

    def downloadButton(self):
        dialog = DownloadDialog(self.title, {
            "word": self.word_file,
            "pdf": self.pdf_file
        },
        self.config,
        self.logger,
        self.parent_)

        dialog.show()




    # def downloadPdf(self):
    #     # print(self._parent)
    #     if self.pdf_file == "":
    #         InfoBar.error(
    #             "无法下载PDF文件",
    #             "该试卷无PDF格式的文件",
    #             orient=Qt.Vertical,
    #             isClosable=True,
    #             position=InfoBarPosition.TOP_RIGHT,
    #             parent=self._parent,
    #             duration=INFO_BAR_DURATION
    #         )
    #     elif os.path.exists(f"{FILE_PATH}{self.title}.pdf"):
    #         os.startfile(f"{FILE_PATH}{self.title}.pdf")
    #     else:
    #         download_file(f"{DOWNLOAD_URL}{self.pdf_file}", f"{FILE_PATH}{self.title}.pdf", f"正在下载{self.title}", parent=self._parent) 
    #         self.download_pdf_button.setText("查看PDF文件")

    # def downloadWord(self):
    #     if self.word_file == "":
    #         InfoBar.error(
    #             "无法下载Word文件",
    #             "该试卷无Word格式的文件",
    #             orient=Qt.Vertical,
    #             isClosable=True,
    #             position=InfoBarPosition.TOP_RIGHT,
    #             parent=self._parent,
    #             duration=INFO_BAR_DURATION
    #         )
    #     elif os.path.exists(f"{FILE_PATH}{self.title}.docx"):
    #         os.startfile(f"{FILE_PATH}{self.title}.docx")
    #     else:
    #         download_file(f"{DOWNLOAD_URL}{self.word_file}", f"{FILE_PATH}{self.title}.docx", f"正在下载{self.title}", parent=self._parent)
    #         self.download_word_button.setText("查看Word文件")

    # def viewWeb(self):
    #     os.system(f"start {WEB_URL}?id={self.id}&title={self.title}")
    
    # def viewPdf(self):
    #     os.system(f"start {DOWNLOAD_URL}{self.pdf_file}")

    def refreshButton(self):
        # if os.path.exists(f"{FILE_PATH}{self.title}.pdf"):
        #     self.download_pdf_button.setText("查看PDF文件")
        # else:
        #     self.download_pdf_button.setText("下载PDF文件")
        
        # if os.path.exists(f"{FILE_PATH}{self.title}.docx"):
        #     self.download_word_button.setText("查看Word文件")
        # else:
        #     self.download_word_button.setText("下载Word文件")

        collects = self.config.get("collects", [])
        item = [self.id, self.title]
        if item in collects:
            self.collect_button.toggle()
            # self.collect_button.setText("取消收藏")
        else:
            pass
            # self.collect_button.setText("收藏")

    def collectButton(self):
        collects = self.config.get(CONFIG_COLLECTS, [])

        item = [self.id, self.title]
        if item in collects:
            collects.remove(item)
            # self.collect_button.setText("收藏")
        else:
            collects.append(item)
            cachePapersInfo([self.full_info])

            # self.collect_button.setText("取消收藏")

        self.config.set(CONFIG_COLLECTS, collects)
