from libs.pages import (SearchPage, Preferred, LocalPage,
                         CollectsPage, SettingsPage, LoadingWindow,
                         AccountPage,)
from libs.widgets import ItemCard, PreferredCard
from libs.worker import (SearchWorker, GetCategoryWorker,
                          GetPointsWorker, GetPapersListWorker, LoginWorker)
from qfluentwidgets import InfoBar, MessageBox
from PyQt5.QtWidgets import  QTreeWidgetItem
from PyQt5.QtGui import  QPixmap, QImage
from PyQt5.QtCore import Qt
from datetime import datetime
import os 

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
            self.assembly_grade_input.addItems(["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"])
        elif current == 1:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(["初一", "初二", "初三"])
        elif current == 2:
            self.assembly_grade_input.clear()
            self.assembly_grade_input.addItems(["高一", "高二", "高三"])

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

                if count % 10 == 0:
                    self.max_page = count // 10
                else:
                    self.max_page = count // 10 + 1
                
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

                    item_widget = PreferredCard(
                        item["id"],
                        item["store_name"],
                        item["browse"],
                        item["upload_num"],
                        item["add_time"],
                        float(item["price"]),
                        item["paper_subject"],
                        int(item["store_year"]),
                        item["paper_grade"],
                        item["paper_type"],
                        True if item["is_hot"] == 1 else False,
                        self.config,
                        self.logger,
                        self
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

class AccountPage(AccountPage):
    def __init__(self, config, logger, parent=None):
        super().__init__(config, logger, parent)


        self.login_worker = LoginWorker(logger)

        self.login_worker.got_qrcode.connect(self.workerGotQrcode)
        self.login_worker.logined.connect(self.workerLogined)
        self.login_worker.error.connect(self.workerError)
        self.login_worker.got_avator.connect(self.workerGotAvator)

        self.login_window.showEvent = self.workerStart
        self.login_window.closeEvent = self.windowClose

        self.logout_button.clicked.connect(self.logout)

    
    def windowClose(self, event):
        self.login_worker.__stop__ = True

    def logout(self):
        self.config.set("account.login", False)
        self.config.set("account.name", "")
        self.config.set("account.phone", "")
        self.config.set("account.is_vip", False)
        self.config.set("account.token", "")

        self.changeButton()
        self.changeText()
        self.changeToken()

    def workerStart(self, event):
        self.login_worker.start()

    def workerGotQrcode(self, data):
        # self.login_window.qrcode_label.setFixedSize(128, 128)
        self.login_window.loading.hide()

        image = QImage().fromData(data)
        image = image.scaled(256, 256,)
        self.login_window.qrcode_label.setPixmap(QPixmap.fromImage(image))

    def workerLogined(self, data):
        self.config.set("account.login", True)
        self.config.set("account.token", data[0])
        self.config.set("account.name", data[1])
        self.config.set("account.phone", data[2])
        self.config.set("account.is_vip", data[3])
    
    def workerError(self, data):
        match data[0]:
            case "getQrcode":
                window = MessageBox("登录失败", f"获取二维码失败：\n{data[1]}", self)
                window.cancelButton.hide()
                window.exec()
            case "login":
                window = MessageBox("登录失败", f"登录失败：\n{data[1]}", self)
                window.cancelButton.hide()
                window.exec()
            case "avator":
                window = MessageBox("登录失败", f"获取头像失败：\n{data[1]}", self)
                window.cancelButton.hide()
                window.exec()
            case _:
                pass

        
        self.login_window.close()

    def workerGotAvator(self, data):
        
        self.login_window.close()

        self.changeButton()
        self.changeText()
        self.changeToken()

                

   



        
        



                
                



        

