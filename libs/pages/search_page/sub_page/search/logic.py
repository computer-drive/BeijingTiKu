from datetime import datetime
from .... import _layout_clear
from .ui import SearchSubPage
from libs.consts import *
from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar
from .....worker.search import SearchWorker
from .....widgets.result_card import ResultCard
from .....log import logger
from .....config import config


class SearchSubPage(SearchSubPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_ = parent

        self.stage_input.currentIndexChanged.connect(self.stageChange)

        year = datetime.now().year
        self.time_input.setRange(2000, year)  # 设置时间输入框的范围
        self.time_input.setValue(year)

        self.search_button.clicked.connect(lambda: self.search(True))
        self.page_back_button.clicked.connect(lambda: self.backPage())
        self.page_forward_button.clicked.connect(lambda: self.nextPage())

    def showContentData(self, data):

        _layout_clear(self.content_data.content_layout)
        for item in data:
            if len(item) == 2:
                InfoBar.warning(
                    "无结果",
                    "没有找到相关内容，以下是可能的原因：\n 1.试卷未上传，一般在考试3-4天后上传 \n2.时间错误 \n3.关键词错误，可尝试删除关键词搜索\n",
                    parent=self,
                    orient=Qt.Vertical,
                    duration=INFO_BAR_DURATION,
                )
                continue

            if item["is_hot"] == 1:
                is_hot = True
            else:
                is_hot = False

            if item["is_quality"] == 1:
                is_real = True
            else:
                is_real = False

            if item["pdf_answer"] == "":
                pdf_file = item["pdf_paper"]
            else:
                pdf_file = item["pdf_answer"]

            if item["word_answer"] == "":
                word_file = item["word_paper"]
            else:
                word_file = item["word_answer"]

            self.content_data.content_layout.addWidget(
                ResultCard(
                    item["id"],
                    item["store_name"],
                    item["browse"],
                    item["upload_num"],
                    item["upload_people"],
                    item["add_time"],
                    is_hot,
                    is_real,
                    pdf_file,
                    word_file,
                    item,
                    self,
                )
            )

    def stageChange(self):
        current = self.stage_input.currentIndex()
        match current:
            case 0:
                grade = PRIMARY_GRADE
            case 1:
                grade = MIDDLE_GRADE
            case 2:
                grade = HIGH_GRADE

        self.grade_input.clear()
        self.grade_input.addItems(grade)

    def nextPage(self):
        if self.page < self.max_page:
            self.page += 1
            self.page_back_button.setEnabled(True)
            self.page_forward_button.setEnabled(True)
        else:
            self.page_back_button.setEnabled(False)
            self.page_forward_button.setEnabled(True)

        self.search(False)

    def backPage(self):
        if self.page > 1:
            self.page -= 1
            self.page_back_button.setEnabled(True)
            self.page_forward_button.setEnabled(True)
        else:
            self.page_back_button.setEnabled(False)
            self.page_forward_button.setEnabled(True)

        self.search(False)

    def search(self, get_total=True):
        if get_total:
            self.page = 1

        self.search_button.setEnabled(False)
        self.page_back_button.setEnabled(False)
        self.page_forward_button.setEnabled(False)
        self.progress.setVisible(True)

        keyword = self.search_input.text()
        limit = PAPERS_DEFAULT_LIMIT
        page = self.page
        subject = self.subject_input.currentText()
        grade = self.grade_input.currentText()
        type = self.type_input.currentText()
        time = self.time_input.value()
        place = self.region_input.currentText()

        if type == "全部":
            type = ""

        if place == "北京":
            place = ""

        logger.info(
            f"Start searching with args: {keyword=} {subject=} {grade=} {type=} {time=} {place=} {page=} {limit=}",
        )

        def finished(data):
            global search_count

            self.search_button.setEnabled(True)
            self.progress.setVisible(False)
            self.page_back_button.setEnabled(True)
            self.page_forward_button.setEnabled(True)

            if data[0]:
                if get_total:
                    if data[2] % PAPERS_DEFAULT_LIMIT == 0:
                        self.max_page = data[2] // PAPERS_DEFAULT_LIMIT
                    else:
                        self.max_page = data[2] // PAPERS_DEFAULT_LIMIT + 1

                    logger.info(
                        f"Search completed with {len(data[1])} results. total: {data[2]}"
                    )
                else:
                    logger.info(f"Search completed with {len(data[1])} results. ")

                self.page_label.setText(f"{self.page}/{self.max_page} 共 {data[2]} 条")

                self.showContentData(data[1])

            else:
                logger.warning(
                    f"Search failed with error: {data[1]}",
                )

        self.searchWorker = SearchWorker(
            keyword, subject, grade, type, time, place, page, limit, get_total
        )
        self.searchWorker.finished.connect(finished)
        self.searchWorker.start()
