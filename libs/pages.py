from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QSizePolicy, QLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import (PushButton, ComboBox, LineEdit, SpinBox, ToolButton,
                            PrimaryPushButton, IndeterminateProgressBar, 
                            CardWidget, IconWidget, ProgressBar, TogglePushButton, InfoBadge,
                            SwitchButton, InfoBar, SingleDirectionScrollArea, SmoothMode, InfoBarPosition
                            )
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TitleLabel, BodyLabel, LargeTitleLabel, CaptionLabel, SubtitleLabel
from typing import Literal
from datetime import datetime
from libs.worker import download_file
import os
from libs.cache import *
from utility.config import JsonConfig

def _get_widgets(layout:QLayout):
    widgets = []
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if isinstance(item, QLayout):
            widgets.extend(_get_widgets(item))
        else:
            widgets.append(item.widget())
    return widgets

def _layout_clear(layout:QLayout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            _layout_clear(item.layout())

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
                config: JsonConfig,
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
                        
        super().__init__(parent) # * parent=SearchPage
        
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
        elif os.path.exists(f"cache/files/{self.title}.pdf"):
            os.system(f"start cache/files/{self.title}.pdf")
        else:
            download_file(f"https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com{self.pdf_file}", f"cache/files/{self.title}.pdf", f"正在下载{self.title}", parent=self._parent) 
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
        elif os.path.exists(f"cache/files/{self.title}.docx"):
            os.system(f"start cache/files/{self.title}.docx")
        else:
            download_file(f"https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com{self.word_file}", f"cache/files/{self.title}.docx", f"正在下载{self.title}", parent=self._parent)
            self.download_word_button.setText("查看Word文件")

    def viewWeb(self):
        os.system(f"start https://www.jingshibang.com/home/detailPaper/?id={self.id}&title={self.title}")
    
    def viewPdf(self):
        os.system(f"start https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com{self.pdf_file}")

    def refreshButton(self):
        if os.path.exists(f"cache/files/{self.title}.pdf"):
            self.download_pdf_button.setText("查看PDF文件")
        else:
            self.download_pdf_button.setText("下载PDF文件")
        
        if os.path.exists(f"cache/files/{self.title}.docx"):
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
        

        
    
class SearchPage(QFrame):
    def __init__(self, config, parent=None): 

        super().__init__(parent)
        self.config = config

        self.page = 1
        self.max_page = 0

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.progress = IndeterminateProgressBar()
        self.progress.setVisible(False)
        v_layout.addWidget(self.progress)
        
        # 搜索窗口-标题
        v_layout.addWidget(LargeTitleLabel("搜索"))

        v_layout.addLayout(self.initSearch())

        self.initContentData()

        v_layout.addWidget(self.scroll_area)
        v_layout.addLayout(self.page_layout)
        # v_layout.addWidget(self.)

        self.setLayout(v_layout)

    
    def initSearch(self):
        h_layout = QHBoxLayout()
            
        # 搜索布局-表单布局
        form_layout = QVBoxLayout()

        # 搜索布局-表单布局-搜索框
        self.search_input = LineEdit()
        self.search_input.setPlaceholderText("搜索")
        form_layout.addWidget(self.search_input)

        # 搜索布局-表单布局-参数布局
        args_layout = QHBoxLayout()
        args_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        args_layout.addWidget(BodyLabel("阶段&学科:"))
        self.stage_input = ComboBox()
        self.stage_input.addItems(["小学", "初中", "高中"])
        self.stage_input.currentIndexChanged.connect(self.stageChange)
        args_layout.addWidget(self.stage_input)

        self.subject_input = ComboBox()
        self.subject_input.addItems(["语文", "数学", "英语", "道法", "物理", "地理", "生物", "历史", "化学"])
        args_layout.addWidget(self.subject_input)

        args_layout.addWidget(BodyLabel("年级:"))
        self.grade_input = ComboBox()
        self.grade_input.addItems(["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"])
        args_layout.addWidget(self.grade_input)

        args_layout.addWidget(BodyLabel("类型:"))
        self.type_input = ComboBox()
        self.type_input.addItems([
            '全部', '真题', '(上)期中', '(上)期末', '(下)期中', '(下)期末', '一模', '二模', '月考',
            '合格考试', '分班考试', '真题汇编', '(上)期中汇编', '(上)期末汇编', '(下)期中汇编', '(下)期末汇编',
            '一模汇编', '二模汇编', '合格考汇编'
            ])
        args_layout.addWidget(self.type_input)

        args_layout.addWidget(BodyLabel("时间:"))
        year = datetime.now().year
        self.time_input = SpinBox()
        self.time_input.setRange(2000, year)
        self.time_input.setValue(year)
        args_layout.addWidget(self.time_input)

        args_layout.addWidget(BodyLabel("地区:"))
        self.region_input = ComboBox()
        self.region_input.addItems([
        '北京', '海淀', '西城', '朝阳', '东城', '房山', '石景山', '顺义', '昌平',
        '通州', '大兴', '门头沟', '延庆', '怀柔', '密云', '经开', '燕山', '延庆'
        ])
        args_layout.addWidget(self.region_input)


        form_layout.addLayout(args_layout)

    
        h_layout.addLayout(form_layout)


        # 搜索布局-表单布局-按钮布局
        self.search_button = PrimaryPushButton("搜索")
        args_layout.addWidget(self.search_button)

        return h_layout
    
    def initContentData(self):
        self.scroll_area = SingleDirectionScrollArea(orient=Qt.Vertical)
        self.scroll_area.setSmoothMode(SmoothMode.NO_SMOOTH)
        self.scroll_area.setStyleSheet("QScrollArea{background: transparent; border: none}")
        self.scroll_area.setWidgetResizable(True)
        
        self.content_data = QWidget()
        self.content_data.setStyleSheet("QWidget{background: transparent}")
        self.scroll_area.setWidget(self.content_data)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(50, 0, 50, 0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_data.content_layout = content_layout

        self.content_data.setLayout(self.content_data.content_layout)

        self.page_layout = QHBoxLayout()
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.page_back_button = ToolButton(FIF.LEFT_ARROW)
        self.page_back_button.setToolTip("上一页")
        self.page_layout.addWidget(self.page_back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page_label = BodyLabel("-/- 共 - 条")
        self.page_layout.addWidget(self.page_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page_forward_button = ToolButton(FIF.RIGHT_ARROW)
        self.page_forward_button.setToolTip("下一页")
        self.page_layout.addWidget(self.page_forward_button, alignment=Qt.AlignmentFlag.AlignCenter)
        



    
        
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

    
        

    
class LocalPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 本地窗口-标题
        v_layout.addWidget(LargeTitleLabel("本地"))

        self.setLayout(v_layout)

class CollectsPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 收藏窗口-标题
        v_layout.addWidget(LargeTitleLabel("收藏"))

        self.setLayout(v_layout)
    
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
class SettingsPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        self.setup_ui()

    def setup_ui(self):

        socall_area = SingleDirectionScrollArea(orient=Qt.Vertical) # 创建垂直方向滚动区域
        socall_area.setWidgetResizable(True) # 设置可调整大小
        socall_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        socall_area.setStyleSheet("QScrollArea{background: transparent; border: none}") # 删除背景和边框
        socall_area.setSmoothMode(SmoothMode.NO_SMOOTH) # 设置不平滑滚动
        self.v_layout.addWidget(socall_area)

        setting_widget = QWidget(self, objectName="setting_widget")
        setting_widget.setStyleSheet("QWidget{background: transparent;}") 

        v_layout = QVBoxLayout(setting_widget)

        # 设置窗口-标题
        v_layout.addWidget(LargeTitleLabel("设置"))

        v_layout.addWidget(SubtitleLabel("个性化"))

        self.theme_input = ComboBox()
        self.theme_input.addItems(["浅色", "深色", "跟随系统"])
        v_layout.addWidget(SettingCard(FIF.BRUSH, "主题", "调整应用的主题外观", [self.theme_input]))

        self.color_input = ComboBox()
        v_layout.addWidget(SettingCard(FIF.PALETTE, "颜色", "调整应用的主题颜色", [self.color_input]))

        v_layout.addWidget(SubtitleLabel("本地缓存"))

        self.cache_info_size = CaptionLabel("试卷信息缓存：0.0 MB")
        self.cache_file_size=  CaptionLabel("试卷文件缓存：0.0 MB")
        self.cache_total_size = CaptionLabel("总计：0.0 MB")
        self.cache_size_progress = ProgressBar()
        self.clear_button = PrimaryPushButton("清除缓存")

        v_layout.addWidget(SettingCard(
            FIF.CLOUD, "缓存", "管理本地缓存",
            [self.cache_info_size, self.cache_file_size, self.cache_total_size, self.cache_size_progress, self.clear_button],
            "v_layout"
        ))

        
        self.allow_cache_info = SwitchButton()
        self.allow_cache_info.setOffText("关")
        self.allow_cache_info.setOnText("开")

        v_layout.addWidget(SettingCard(
            FIF.MENU, "允许缓存试卷信息", "搜索时缓存试卷信息",
            [self.allow_cache_info]
        ))

        

        self.allow_cache_file = SwitchButton()
        self.allow_cache_file.setOffText("关")
        self.allow_cache_file.setOnText("开")

        v_layout.addWidget(SettingCard(
            FIF.FOLDER, "允许缓存试卷文件" , "下载时缓存文件",
            [self.allow_cache_file]
        ))

        v_layout.addWidget(SubtitleLabel("高级"))
        tip_label = CaptionLabel("*注意：以下设置仅供开发者调试使用，普通用户请不要随意更改。您可以通过点击'显示高级设置'来查看。")
        tip_label.setTextColor("#ffcb0d", "#ffcb0d")
        v_layout.addWidget(tip_label)

        self.show_advanced_setting = PushButton("显示高级设置")
        self.show_advanced_setting.clicked.connect(lambda: self.advanced_frame.setHidden(False))
        v_layout.addWidget(self.show_advanced_setting, alignment=Qt.AlignmentFlag.AlignLeft)

        self.advanced_frame = QFrame(self)
        self.advanced_frame.setHidden(True)


        advanced_layout = QVBoxLayout()

        self.custom_url_input = LineEdit()
        advanced_layout.addWidget(SettingCard(
            FIF.WIFI, "自定义服务器地址", "自定义服务器地址，留空使用默认", [self.custom_url_input]
        ))

        self.custom_user_agent_input = LineEdit()
        advanced_layout.addWidget(SettingCard(
            FIF.PEOPLE, "自定义User-Agent", "自定义User-Agent，留空使用默认", [self.custom_user_agent_input]
        ))

        self.show_delay_input = SwitchButton()
        self.show_delay_input.setOnText("开")
        self.show_delay_input.setOffText("关")

        self.dalay_input = SpinBox()
        advanced_layout.addWidget(SettingCard(
            FIF.CLOUD_DOWNLOAD, "搜索延迟设置", "搜索后为防止被网站拉黑，短时间内进行多次上搜索时提醒",
            [self.show_delay_input, self.dalay_input],
            "v_layout"
        ))
        self.advanced_frame.setLayout(advanced_layout)


        v_layout.addWidget(self.advanced_frame)

        v_layout.addWidget(CaptionLabel("其他"))

        self.reset_button = PushButton("重置所有设置")
        v_layout.addWidget(SettingCard(
            FIF.REMOVE_FROM, "重置所有设置", "重置所有设置至默认，注意：此操作不可逆", 
            [self.reset_button]
        ))

        v_layout.addWidget(SettingCard(
            FIF.INFO, "关于", "查看软件信息",
            [PushButton("查看")]
        ))


        setting_widget.setLayout(v_layout)
        
        socall_area.setWidget(setting_widget)

        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)






if __name__ == "__main__":
    app = QApplication([])
    
    w = SearchPage()

    for i in range(10):
        w.content_data.content_layout.addWidget(ItemCard(
        0,
        "测试标题",
        1145, 1919,
        "测试作者", "1919-05-04",
        False, True,
        "...", ""
    ))
    w.show()

    app.exec_()