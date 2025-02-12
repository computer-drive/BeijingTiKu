from libs.pages import SearchPage, Preferred, LocalPage, CollectsPage, SettingsPage
from libs.widgets import ItemCard
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt


def _layout_clear(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            _layout_clear(item.layout())


class SearchPage(SearchPage):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

        self.stage_input.currentIndexChanged.connect(self.stageChange)

    def showContentData(self, data):

        _layout_clear(self.content_data.content_layout)
        for item in data:
            if len(item) == 2:
                InfoBar.warning(
                    "无结果",
                    "没有找到相关内容，以下是可能的原因：\n 1.试卷未上传，一般在考试3-4天后上传 \n2.时间错误 \n3.关键词错误，可尝试删除关键词搜索\n",
                    parent=self,
                    orient=Qt.Vertical,
                    duration=5000
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

            # print(self)
            self.content_data.content_layout.addWidget(ItemCard(
            item["id"], item["store_name"],
            item["browse"], item["upload_num"],
            item["upload_people"], item["add_time"],
            is_hot, is_real,
            pdf_file, word_file,
            self.config,
            self 
            ))
    
    def stageChange(self):
        current = self.stage_input.currentIndex()
        match current:
            case 0:
                grade = ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"]
            case 1:
                grade = ["初一", "初二", "初三"]
            case 2:
                grade = ["高一", "高二", "高三"]

        self.grade_input.clear()
        self.grade_input.addItems(grade)

    def nextPage(self, search):
        if self.page < self.max_page:
            self.page += 1
            self.page_back_button.setEnabled(True)
            self.page_forward_button.setEnabled(True)
        else:
            self.page_back_button.setEnabled(False)
            self.page_forward_button.setEnabled(True)

        search(False)

    def backPage(self, search):
        if self.page > 1:
            self.page -= 1
            self.page_back_button.setEnabled(True)
            self.page_forward_button.setEnabled(True)
        else:
            self.page_back_button.setEnabled(False)
            self.page_forward_button.setEnabled(True)

        search(False)
