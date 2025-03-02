from datetime import datetime
from libs.consts import *
from .ui import Preferred
from .. import _layout_clear
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from qfluentwidgets import InfoBar
from ..loading_window import LoadingWindow
from ...worker.preferred import GetCategoryWorker, GetPointsWorker, GetPapersListWorker
from ...widgets.result_card import ResultCard


class Preferred(Preferred):

    def __init__(self, config, logger, parent=None):
        super().__init__(config, parent)

        self.logger = logger

        self.catetory = None
        self.currentMoudle = (None, "")
        self.currentChapter = (None, "")
        self.currentPoint = (None, "")
        self.workers = {}
        self.page = 1
        self.max_page = 1
        self.__started_search__ = False
        self.got_category = False

        now = datetime.now()
        self.time_input.setRange(0, now.year)
        self.time_input.setValue(now.year)

        self.type_input.currentIndexChanged.connect(self.changeAssembly)
        self.state_input.currentIndexChanged.connect(self.stateChanged)

        self.state_input.currentIndexChanged.connect(self.showCateGory)
        self.subject_input.currentIndexChanged.connect(self.showCateGory)

        self.all_time_button.clicked.connect(lambda: self.time_input.setValue(0))

        self.page_back_button.clicked.connect(self.pageBack)
        self.page_forward_button.clicked.connect(self.pageNext)

        self.showEvent = self.getCategory

        self.loading = LoadingWindow("正在加载", "[DefaultText]", self)

        
    def pageBack(self):
        if self.__started_search__:
            return 
        
        if self.page > 1:
            self.page -= 1

        self.pageChange()

        self.search()
        
    def pageNext(self):
        if self.__started_search__:
            return 
         
        if self.page < self.max_page:
            self.page += 1

        self.pageChange()

        self.search()
    
    def pageChange(self):
        self.page_back_button.setEnabled(self.page > 1)
        self.page_forward_button.setEnabled(self.page < self.max_page)

        self.page_label.setText(f"{self.page}/{self.max_page} 共{self.max_page * 10}条")

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
        current = self.state_input.currentIndex()
        if current == 0:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(PRIMARY_GRADE)
        elif current == 1:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(MIDDLE_GRADE)
        elif current == 2:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(HIGH_GRADE)

    def getCategory(self, event):
        if self.got_category:
            return
        
        def finished(data):
            self.logger.info("Got category.")

            self.category = data[1]["data"]["category"]
        

            self.showCateGory()

            self.got_category = True


        self.logger.info("Getting category.")
        
    
        self.loading.worker = GetCategoryWorker()
        self.loading.worker.finished.connect(finished)

        self.loading.content_label.setText("正在获取分类")
        self.loading.show()
        self.loading.worker.start()

    def changeItem(self, item, column):

        if item.typ == "moudle":
            self.currentMoudle = (item.id, item.name)
            self.currentChapter = (None, '')
            self.currentPoint = (None, '')

        elif item.typ == "chapter":
            self.currentChapter = (item.id, item.name)
            self.currentPoint = (None, '')

        elif item.typ == "point":
            self.currentPoint = (item.id, item.name)

        items = [
            self.currentMoudle[1],
            self.currentChapter[1],
            self.currentPoint[1]
        ]
        text = ""
        for item in items:

            if item != "":
                text += item + " > "
        text = text[:-3]
        self.path_label.setText(text)

        self.page = 1
        self.max_page = 1
        
        
        if not self.__started_search__:
            self.search()

    def showCateGory(self):
        # print(self.loading.isVisible())
        if not self.loading.isVisible():
            self.loading.show()


        currentSubject = self.subject_input.currentText()
        currentState = self.state_input.currentText()
        
        subject_cate = None
        state_cate = None

        self.catetory_widget.clear()
        for cate in self.category:
            if cate["cate_name"] == currentSubject:
                subject_cate = cate
                break
        
        if subject_cate is None:

            self.logger.error(f"showCateGory error: subject '{currentSubject}' not found.")

            InfoBar.error("加载错误",f"未找到学科 {currentSubject}", parent=self)

            # self.subject_input.setCurrentIndex(0)

            self.loading.hide()
            return

        # print(json.dumps(subject_cate))
        for cate in subject_cate["items"]:
            if cate["cate_name"] == currentState:
                state_cate = cate
                break
        
        if state_cate is None:
            self.logger.error(f"showCateGory error: subject '{currentSubject}' state '{currentState}' not found.")

            InfoBar.error("加载错误",f"未找到学科 {currentSubject} 的阶段 {currentState}", parent=self)

            # self.state_input.setCurrentIndex(0)

            self.loading.hide()
            return
        
        self.logger.info(f"Getting {currentState}: {currentSubject} categories.")
        
        for moudle in state_cate["items"]:
            moudle_item = QTreeWidgetItem([moudle["cate_name"]])
            moudle_item.id = moudle["id"]
            moudle_item.name = moudle["cate_name"]
            moudle_item.typ = "moudle"


            for chapter in moudle["items"]:
                chapter_item = QTreeWidgetItem([chapter["cate_name"]])
                chapter_item.id = chapter["id"]
                chapter_item.name = chapter["cate_name"]
                chapter_item.typ = "chapter"

                moudle_item.addChild(chapter_item)
            
                def finished(message):
                    if message[0]:
                        for point in message[1]["data"]:

                            point_item = QTreeWidgetItem([point["label"]])
                            point_item.id = point["value"]
                            point_item.name = point["label"]
                            point_item.typ = "point"

                            if self.config.get("cache.cache_categories", False):
                                pass
                        
                            self.workers[message[2]]["chapter"].addChild(point_item)


                    self.workers[message[2]]["finished"] = True

                    all = True
                    
                    for key in self.workers:

                        if not self.workers[key]["finished"]:
                            all = False
                            break

                    if all:
                        self.logger.info(f"Get {len(moudle["items"])} points for chapter all finished.")
                        self.loading.close()

             
                worker = GetPointsWorker(chapter["id"])
                
                self.workers[chapter["id"]] = {
                    "worker": worker,
                    "finished": False,
                    "chapter": chapter_item
                }

                worker.finished.connect(finished)
                worker.start()
            
            self.logger.info(f"Getting {len(moudle["items"])}points for chapter")


                # for point in chapter["items"]:
                #     point_item = QTreeWidgetItem([point["cate_name"]])
                    
                #     point_item.id = point["id"]
                #     point_item.name = point["cate_name"]
                #     point_item.typ = "point"

                #     chapter_item.addChild(point_item)

                

            self.catetory_widget.addTopLevelItem(moudle_item)
            self.catetory_widget.itemClicked.connect(self.changeItem)   

    def search(self):
        self.content_data_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        _layout_clear(self.content_data_layout)
        self.initSearchLoading()


        subject = self.subject_input.currentText()
        grade = self.state_input.currentText()
        store_type = self.type_input.currentText()
        year = self.time_input.value()
        
        assembly_grade = ""
        assembly_type = ""

        if store_type == "汇编":
            assembly_type = self.assembly_type_input.currentText()
            assembly_grade = self.assembly_grade_input.currentText()
            # print(assembly_grade, assembly_type)

        if store_type == "全部":
            store_type = ""

        if assembly_type == "全部":
            assembly_type = ""
        if year == 0:
            year = ""

        # print(subject, grade, store_type, year, assembly_grade, assembly_type, self.currentMoudle, self.currentChapter, self.currentPoint)

        def finished(data):
            self.search_loading.hide()
            _layout_clear(self.content_data_layout)
            self.content_data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            self.__started_search__ = False  


            if data[0]:
            
                count = data[1]["data"]["count"]

                if count % PREFERRED_DEFAULT_LIMIT == 0:
                    self.max_page = count // PREFERRED_DEFAULT_LIMIT
                else:
                    self.max_page = count // PREFERRED_DEFAULT_LIMIT + 1
                
                self.pageChange()

                if len(data[1]["data"]["list"]) == 0:
                    self.content_data_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.initSearchNull()
                
                for item in data[1]["data"]["list"]:
                    # print(item["store_name"])
                    if item["is_hot"] == 1:
                        is_hot = True
                    else:
                        is_hot = False

                    # item_widget = PreferredCard(
                    #     item["id"],
                    #     item["store_name"],
                    #     item["browse"],
                    #     item["upload_num"],
                    #     item["add_time"],
                    #     float(item["price"]),
                    #     item["paper_subject"],
                    #     int(item["store_year"]),
                    #     item["paper_grade"],
                    #     item["paper_type"],
                    #     True if item["is_hot"] == 1 else False,
                    #     self.config,
                    #     self.logger,
                    #     item,
                    #     self
                    # )
                    item_widget = ResultCard(
                        item["id"], item["store_name"],
                        item["browse"], item["upload_num"],
                        "菁师帮", item["add_time"], is_hot,
                        False, "" , "", 
                        item, self.config, self.logger, self,
                        f"{item["paper_subject"]} {item["store_year"]} {item["paper_grade"]} {item["paper_type"]}",
                        "preferred"
                    )
                    self.content_data_layout.addWidget(item_widget)

        self.search_worker = GetPapersListWorker(self.page,
                                                subject,
                                                grade,
                                                logger=self.logger
                                                ).setType(store_type)
        self.search_worker.setType(store_type).setYear(year).setModule(*self.currentMoudle)
        self.search_worker.setChapter(*self.currentChapter).setPoint(*self.currentPoint)
        self.search_worker.setAssembly(assembly_grade, assembly_type).setCatid(self.currentMoudle[0], self.currentChapter[0], self.currentPoint[0])
        self.search_worker.finished.connect(finished)

        self.__started_search__ = True

        self.search_worker.start()


