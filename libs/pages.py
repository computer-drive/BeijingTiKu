from libs.widgets import SettingCard
from utility.format import format_capacity, format_time
from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout, QFrame, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from qfluentwidgets import (PushButton, ComboBox, LineEdit, SpinBox, ToolButton, MessageBoxBase,
                            PrimaryPushButton, IndeterminateProgressBar,  ProgressBar, TitleLabel,
                            SwitchButton, SingleDirectionScrollArea, SmoothMode, IndeterminateProgressRing,
                            BodyLabel, LargeTitleLabel, CaptionLabel, SubtitleLabel, FluentWindow,
                            NavigationItemPosition, TreeWidget
                            )
from qfluentwidgets import FluentIcon as FIF


    
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
        v_layout.addWidget(LargeTitleLabel("试卷"))

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
        self.time_input = SpinBox()
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
        
    

class Preferred(QFrame):
    def __init__(self, config, parent=None):
        super().__init__(parent)

        self.config = config

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        v_layout.addWidget(LargeTitleLabel("优选"))

        v_layout.addLayout(self.initSearch())

        v_layout.addLayout(self.initContent())

        self.setLayout(v_layout)

    def initSearch(self):

        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)    

        search_layout.addWidget(BodyLabel("阶段&学科："))

        self.state_input = ComboBox()
        self.state_input.addItems(["小学", "初中", "高中"])
        search_layout.addWidget(self.state_input)

        self.subject_input = ComboBox()
        self.subject_input.addItems(["语文", "数学", "英语", "物理", "化学", "生物", "历史", "地理", "道法"])
        search_layout.addWidget(self.subject_input)

        search_layout.addWidget(BodyLabel("类型："))

        self.type_input = ComboBox()
        self.type_input.addItems(["全部","汇编", "测试", "课件", "讲义", "知识", "专辑"])
        search_layout.addWidget(self.type_input)

        self.assembly_type_label = BodyLabel("汇编类型：")
        self.assembly_type_label.setVisible(False)
        search_layout.addWidget(self.assembly_type_label)

        self.assembly_type_input = ComboBox()
        self.assembly_type_input.setVisible(False)
        self.assembly_type_input.addItems(["全部", "(上)期末汇编", "(上)其中汇编", "一模汇编", "二模汇编", "(下)期中汇编", "(下)期末汇编", "合格考汇编"])
        self.assembly_type_input.setVisible(False)
        search_layout.addWidget(self.assembly_type_input)

        self.assembly_grade_label = BodyLabel("汇编年级：")
        search_layout.addWidget(self.assembly_grade_label)

        self.assembly_grade_input = ComboBox()
        self.assembly_grade_input.addItems(["一年级", "二年级", "三年级", "四年级", "五年级", "六年级"])
        self.assembly_grade_input.setVisible(False)
        search_layout.addWidget(self.assembly_grade_input)


        search_layout.addWidget(BodyLabel("时间："))

        self.time_input = SpinBox()
        search_layout.addWidget(self.time_input)    


        return search_layout
    
    def initContent(self):
        content_layout = QHBoxLayout()

        self.catetory_widget = TreeWidget(self)
        self.catetory_widget.setHeaderHidden(True)
        content_layout.addWidget(self.catetory_widget)

        self.content_data_layout = QVBoxLayout()
        content_layout.addLayout(self.content_data_layout)

        return content_layout

        


    
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


class ProgressWindow(MessageBoxBase):
    def __init__(self, content: str, parent=None):
        super().__init__(parent)


        self.viewLayout.addWidget(TitleLabel(content))

        self.progress = ProgressBar()
        self.progress.setRange(0, 100)
        self.viewLayout.addWidget(self.progress)

        info_layout = QHBoxLayout()
        self.viewLayout.addLayout(info_layout)

        self.count_label = CaptionLabel("0.00 MB / 0.00 MB 0.00 KB/S")
        info_layout.addWidget(self.count_label)

        self.eta_label = CaptionLabel("00:00:00 100%")
        info_layout.addWidget(self.eta_label, alignment=Qt.AlignmentFlag.AlignRight)

        self.widget.setMinimumWidth(450)

        self.yesButton.hide()
        # self.cancelButton.hide()

    def update_(self, data):
        count, total, speed, eta, progress = data

            

        if eta == -1:
            eta = "--:--:--"
            

        self.count_label.setText(f"{format_capacity(count)} / {format_capacity(total)} {format_capacity(speed)}/S")
        self.eta_label.setText(f"{format_time(eta)} {progress}%") 

        self.progress.setValue(progress)

class LoadingWindow(MessageBoxBase):
    def __init__(self, title:str, content:str, parent=None):
        super().__init__(parent)

        self.setMinimumSize(500,300)

        progress = IndeterminateProgressRing()
        progress.setFixedSize(45, 45)
        self.viewLayout.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)

        content_layout = QVBoxLayout()

        content_layout.addWidget(TitleLabel(title), alignment=Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(BodyLabel(content), alignment=Qt.AlignmentFlag.AlignCenter)

        self.viewLayout.addLayout(content_layout)


        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()


class MainWindow(FluentWindow):
    def __init__(self, config, logger):
        super().__init__()

        import libs.pages_logical as logical

        self.config = config
        self.logger = logger

        self.setWindowTitle("BeijingTiKu") # 设置窗口标题

        self.searchInterface = logical.SearchPage(config, logger, self)
        self.searchInterface.setObjectName("searchInterface")
        
        self.preferredInterface = logical.Preferred(config, logger, self)
        self.preferredInterface.setObjectName("preferredInterface")

        self.localInterface = logical.LocalPage(self)
        self.localInterface.setObjectName("localInterface")

        self.collectsInterface = logical.CollectsPage(self)
        self.collectsInterface.setObjectName("collectsInterface")

        self.settingInterface = logical.SettingsPage(self)
        self.settingInterface.setObjectName("settingInterface")

        self.initNavigation()
         
    def initNavigation(self):

        self.addSubInterface(self.searchInterface, FIF.DOCUMENT, "试卷")
        self.addSubInterface(self.preferredInterface, FIF.FLAG, "优选")

        self.addSubInterface(self.localInterface, FIF.FOLDER, "本地")
        self.addSubInterface(self.collectsInterface, FIF.HEART, "收藏")


        self.addSubInterface(self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)



# if __name__ == "__main__":
#     app = QApplication([])
    
#     w = SearchPage()

#     for i in range(10):
#         w.content_data.content_layout.addWidget(ItemCard(
#         0,
#         "测试标题",
#         1145, 1919,
#         "测试作者", "1919-05-04",
#         False, True,
#         "...", ""
#     ))
#     w.show()

#     app.exec_()