from libs.pages import SearchPage, Preferred, LocalPage, CollectsPage, SettingsPage, LoadingWindow
from libs.widgets import ItemCard
from libs.worker import SearchWorker, GetCategoryWorker
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt
from datetime import datetime



def _layout_clear(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            _layout_clear(item.layout())


class SearchPage(SearchPage):
    def __init__(self, config, logger, parent=None):
        super().__init__(config, parent)

        self.logger = logger
        logger.name = "SearchPage"

        self.stage_input.currentIndexChanged.connect(self.stageChange)

        year = datetime.now().year
        self.time_input.setRange(2000, year) # 设置时间输入框的范围
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
            limit = 20
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

            self.logger.info(
                f"Start searching with args: {keyword=} {subject=} {grade=} {type=} {time=} {place=} {page=} {limit=}",)
            
            def finished(data):
                global search_count

                self.search_button.setEnabled(True)
                self.progress.setVisible(False)
                self.page_back_button.setEnabled(True)
                self.page_forward_button.setEnabled(True)


                if data[0]:
                    if get_total:
                        if data[2] % 20 == 0:
                            self.max_page = data[2] // 20
                        else:
                            self.max_page = data[2] // 20 + 1

                    
                        self.logger.info(f"Search completed with {len(data[1])} results. total: {data[2]}")
                    else:
                        self.logger.info(f"Search completed with {len(data[1])} results. ")
                    
                    self.page_label.setText(f"{self.page}/{self.max_page} 共 {data[2]} 条")

                    self.showContentData(data[1])
                    
                else:
                    self.logger.warning(f"Search failed with error: {data[1]}",)

            self.searchWorker = SearchWorker(keyword, subject, grade, type, time, place, page, limit, get_total)
            self.searchWorker.finished.connect(finished)
            self.searchWorker.start()


class Preferred(Preferred):
    def __init__(self, config, logger, parent=None):
        super().__init__(config, parent)

        self.logger = logger

        self.catetory = None

        now = datetime.now()
        self.time_input.setRange(2000, now.year)
        self.time_input.setValue(now.year)

        self.type_input.currentIndexChanged.connect(self.changeAssembly)
        self.state_input.currentIndexChanged.connect(self.stateChanged)

        self.showEvent = self.getCategory


    def changeAssembly(self):
        if self.type_input.currentText() == "汇编":
            self.assembly_grade_label.show()
            self.assembly_grade_input.show()
            self.assembly_type_input.show()
            self.assembly_type_label.show()
        else:
            self.assembly_grade_label.hide()
            self.assembly_grade_input.hide()
            self.assembly_type_input.hide()
            self.assembly_type_label.hide()

    def stateChanged(self):
        current =self.state_input.currentIndex()
        if current == 0:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"])
        elif current == 1:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(["初一", "初二", "初三"])
        elif current == 2:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(["高一", "高二", "高三"])

    def getCategory(self, event):
        def finished(data):
            self.logger.info("Get category finished.")

            self.category = data[1]["data"]["category"]

            loading.close()

        self.logger.info("Getting category.")
        
        loading = LoadingWindow("正在加载", "正在获取分类", self)

        loading.worker = GetCategoryWorker()
        loading.worker.finished.connect(finished)

        loading.show()
        loading.worker.start()



        

