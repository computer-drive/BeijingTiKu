from libs.widgets import MaterialIcon as MIcon
from libs.consts import *
from utility.format import format_capacity, format_time
from PyQt5.QtWidgets import  (QVBoxLayout, QHBoxLayout, QFrame,
                              QWidget, QSizePolicy, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import (PushButton, ComboBox, LineEdit, SpinBox, ToolButton, MessageBoxBase,
                            PrimaryPushButton, IndeterminateProgressBar,  ProgressBar, TitleLabel,
                            SwitchButton, SingleDirectionScrollArea, SmoothMode, IndeterminateProgressRing,
                            BodyLabel, LargeTitleLabel, CaptionLabel, FluentWindow,
                            NavigationItemPosition, TreeWidget, CardWidget, GroupHeaderCardWidget
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
        self.stage_input.addItems(SEARCH_STATE)
        
        args_layout.addWidget(self.stage_input)

        self.subject_input = ComboBox()
        self.subject_input.addItems(SEARCH_SUBJECT)
        args_layout.addWidget(self.subject_input)

        args_layout.addWidget(BodyLabel("年级:"))
        self.grade_input = ComboBox()
        self.grade_input.addItems(PRIMARY_GRADE)
        args_layout.addWidget(self.grade_input)

        args_layout.addWidget(BodyLabel("类型:"))
        self.type_input = ComboBox()
        self.type_input.addItems(SEARCH_PAPER_TYPE)
        args_layout.addWidget(self.type_input)

        args_layout.addWidget(BodyLabel("时间:"))
        self.time_input = SpinBox()
        args_layout.addWidget(self.time_input)

        args_layout.addWidget(BodyLabel("地区:"))
        self.region_input = ComboBox()
        self.region_input.addItems(SEARCH_REGION)
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
        self.scroll_area.setStyleSheet(SCROLL_AERA_STYLE)
        self.scroll_area.setWidgetResizable(True)
        
        self.content_data = QWidget()
        self.content_data.setStyleSheet(SCROLL_WIDGET_STYLE)
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

        self.path_label = BodyLabel()
        self.path_label.setStyleSheet("font-size: 20px;")
        v_layout.addWidget(self.path_label)

        v_layout.addLayout(self.initContent())

        self.page_layout = QHBoxLayout()
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addLayout(self.page_layout)
        
        self.page_back_button = ToolButton(FIF.LEFT_ARROW)
        self.page_back_button.setToolTip("上一页")
        self.page_layout.addWidget(self.page_back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page_label = BodyLabel("-/- 共 - 条")
        self.page_layout.addWidget(self.page_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.page_forward_button = ToolButton(FIF.RIGHT_ARROW)
        self.page_forward_button.setToolTip("下一页")
        self.page_layout.addWidget(self.page_forward_button, alignment=Qt.AlignmentFlag.AlignCenter)


        self.setLayout(v_layout)

    def initSearch(self):

        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)    

        search_layout.addWidget(BodyLabel("阶段&学科："))

        self.state_input = ComboBox()
        self.state_input.addItems(SEARCH_STATE)
        search_layout.addWidget(self.state_input)

        self.subject_input = ComboBox()
        self.subject_input.addItems(SEARCH_SUBJECT)
        search_layout.addWidget(self.subject_input)

        search_layout.addWidget(BodyLabel("类型："))

        self.type_input = ComboBox()
        self.type_input.addItems(SEARCH_PREFERRED_TYPE)
        search_layout.addWidget(self.type_input)

        self.assembly_type_label = BodyLabel("汇编类型：")
        self.assembly_type_label.setVisible(False)
        search_layout.addWidget(self.assembly_type_label)

        self.assembly_type_input = ComboBox()
        self.assembly_type_input.setVisible(False)
        self.assembly_type_input.addItems(SEARCH_ASSEMBLE_TYPE)
        self.assembly_type_input.setVisible(False)
        search_layout.addWidget(self.assembly_type_input)

        self.assembly_grade_label = BodyLabel("汇编年级：")
        self.assembly_grade_label.setVisible(False)
        search_layout.addWidget(self.assembly_grade_label)

        self.assembly_grade_input = ComboBox()
        self.assembly_grade_input.addItems(PRIMARY_GRADE)
        self.assembly_grade_input.setVisible(False)
        search_layout.addWidget(self.assembly_grade_input)


        search_layout.addWidget(BodyLabel("时间："))

        self.time_input = SpinBox()
        search_layout.addWidget(self.time_input)

        self.all_time_button = PrimaryPushButton("全部")
        search_layout.addWidget(self.all_time_button)


        return search_layout
    
    def initContent(self):
        content_layout = QHBoxLayout()

        self.catetory_widget = TreeWidget(self)
        self.catetory_widget.setFixedWidth(300)
        self.catetory_widget.setHeaderHidden(True)
        content_layout.addWidget(self.catetory_widget)

        scroll_area = SingleDirectionScrollArea(orient=Qt.Vertical)
        scroll_area.setStyleSheet(SCROLL_AERA_STYLE)
        scroll_area.setSmoothMode(SmoothMode.NO_SMOOTH)
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(SCROLL_WIDGET_STYLE)
        scroll_area.setWidget(scroll_widget)

        self.content_data_layout = QVBoxLayout()
        self.content_data_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget.setLayout(self.content_data_layout)

        content_layout.addWidget(scroll_area)

        return content_layout
    
    def initSearchLoading(self):
        self.search_loading = IndeterminateProgressRing()
        self.search_loading.setFixedSize(60, 60)
        self.content_data_layout.addWidget(self.search_loading, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

    def initSearchNull(self):
        
        self.icon_label = BodyLabel(SEARCH_NULL_TEXT)
        self.icon_label.setStyleSheet("font-size: 60px;")
        self.content_data_layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.null_label = BodyLabel("没有找到相关内容")
        self.null_label.setStyleSheet("font-size: 20px;")
        self.content_data_layout.addWidget(self.null_label, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

    
class LocalPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 本地窗口-标题
        v_layout.addWidget(LargeTitleLabel("本地"))

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
        socall_area.setStyleSheet(SCROLL_AERA_STYLE) # 删除背景和边框
        socall_area.setSmoothMode(SmoothMode.NO_SMOOTH) # 设置不平滑滚动
        self.v_layout.addWidget(socall_area)

        setting_widget = QWidget(self, objectName="setting_widget")
        setting_widget.setStyleSheet(SCROLL_WIDGET_STYLE) 
        socall_area.setWidget(setting_widget)

        v_layout = QVBoxLayout(setting_widget)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        setting_widget.setLayout(v_layout)


        v_layout.addWidget(LargeTitleLabel("设置"))


        cache_card = GroupHeaderCardWidget()
        cache_card.setBorderRadius(8)
        
        cache_card.setTitle("缓存设置")

        info_layout = QVBoxLayout()
        self.cache_info_label = BodyLabel("信息缓存大小：0.00 MB")
        info_layout.addWidget(self.cache_info_label)
        self.cache_file_label = BodyLabel("文件缓存大小：0.00 MB")
        info_layout.addWidget(self.cache_file_label)
        self.cache_progress = ProgressBar()
        info_layout.addWidget(self.cache_progress)
        self.cache_clear_button = PushButton("清理缓存")
        info_layout.addWidget(self.cache_clear_button)

        info_widget = QWidget()
        info_widget.setLayout(info_layout)

        cache_card.addGroup(MIcon("cached") ,"缓存管理", "查看和管理缓存信息", info_widget)

        self.cache_perferred_input = SwitchButton()
        self.cache_perferred_input.setOnText("开")
        self.cache_perferred_input.setOffText("关")
        cache_card.addGroup(MIcon("settings_heart"), "缓存优选信息", "获取优选信息时优先使用缓存", self.cache_perferred_input)

        self.cache_collect_input = SwitchButton()
        self.cache_collect_input.setOnText("开")
        self.cache_collect_input.setOffText("关")
        cache_card.addGroup(MIcon("star"), "缓存收藏信息", "收藏时缓存信息", self.cache_collect_input)

        self.cache_max_size_input = SpinBox()
        self.cache_max_size_input.setRange(0, 1024)
        cache_card.addGroup(MIcon("storage"), "缓存最大大小", "缓存最大大小(单位：MB)", self.cache_max_size_input)

        v_layout.addWidget(cache_card)



        update_card = GroupHeaderCardWidget()
        update_card.setTitle("更新")

        self.check_update_button = PushButton("检查更新")
        update_card.addGroup(MIcon("update"), "检查更新", "检查更新", self.check_update_button)

        self.change_log_button = PushButton("更新日志")
        update_card.addGroup(MIcon("change_circle"), "更新日志", "查看更新日志", self.change_log_button)

        v_layout.addWidget(update_card)

        beta_card = GroupHeaderCardWidget()
        beta_card.setTitle("Beta测试计划")

        self.beta_input = SwitchButton()
        self.beta_input.setOnText("开")
        self.beta_input.setOffText("关")
        beta_card.addGroup(MIcon("deployed_code_update"), "Beta测试计划", "参加Beta测试计划", self.beta_input)

        v_layout.addWidget(beta_card)

        self.info_card = GroupHeaderCardWidget()
        self.info_card.setTitle("信息")

        self.about_button = PushButton("关于")
        self.info_card.addGroup(MIcon("info"), "关于", "关于", self.about_button)

        v_layout.addWidget(self.info_card)


class LoginWindow(MessageBoxBase):
    def __init__(self, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout = QHBoxLayout()
        self.viewLayout.addLayout(top_layout)

        top_left_layout = QVBoxLayout()
        top_layout.addLayout(top_left_layout)

        top_left_layout.addWidget(TitleLabel("登录"))

        info_label = BodyLabel("请使用微信扫码登录")
        info_label.setStyleSheet("font-size: 20px;")
        top_left_layout.addWidget(info_label)

        close_button = ToolButton(FIF.CLOSE)
        close_button.clicked.connect(self.close)
        top_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)


        content_layout = QVBoxLayout()
        self.viewLayout.addLayout(content_layout)

        content_layout.addStretch()

        self.loading = IndeterminateProgressRing()
        self.loading.setFixedSize(*PROGRESS_RING_SIZE)
        content_layout.addWidget(self.loading, alignment=Qt.AlignmentFlag.AlignCenter)

        self.qrcode_label = QLabel()
        content_layout.addWidget(self.qrcode_label, alignment=Qt.AlignmentFlag.AlignCenter)

        content_layout.addStretch()

        self.yesButton.hide()
        self.cancelButton.hide()


        self.widget.setMinimumSize(400, 400)

        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()

        self.showEvent = self.whenShow

    def whenShow(self, event):

        self.loading.show()

        self.qrcode_label.clear()


class AccountPage(QFrame):
    def __init__(self, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger

        self.initUI()

        self.login_window = LoginWindow(config, logger, self)
        self.login_window.hide()


    def initUI(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        layout.addWidget(LargeTitleLabel("账户"))

        layout.addWidget(self.initCard())

        self.token_label = BodyLabel("Token:未登录")
        self.changeToken()
        self.token_label.setMaximumWidth(400)
        layout.addWidget(self.token_label)

        layout.addWidget(TitleLabel("为什么需要登录？"))
        layout.addWidget(BodyLabel("北京题库中的一个api，需要获取登录后的token，否则无法使用."))
        layout.addWidget(BodyLabel("api为北京题库获取优选信息的接口，登录后才可获取下载地址(若不使用优选功能或可以自行下载，则可不进行登录)."))
        layout.addWidget(BodyLabel("登录后token保存在本地，注意不要泄露你的token"))

        
        

    def login(self):
        self.login_window.show()


    def changeToken(self):
        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)
        token = self.config.get(CONFIG_ACCOUNT_TOKEN, "")

        # print(logined)
        if logined:
            self.token_label.setText(f"Token:{token}")
        else:
            self.token_label.setText("Token:未登录")
    
    def initCard(self):
        card = CardWidget()

        layout = QHBoxLayout()
        card.setLayout(layout)

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(left_layout)

        self.icon = QLabel()
        left_layout.addWidget(self.icon)

        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.addLayout(info_layout)

        self.name_label = TitleLabel()
        info_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.phone_label = BodyLabel()
        info_layout.addWidget(self.phone_label, alignment=Qt.AlignmentFlag.AlignLeft)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(right_layout)

        self.logout_button = PrimaryPushButton("退出登录")
        self.logout_button.setVisible(False)
        right_layout.addWidget(self.logout_button)

        self.login_button = PrimaryPushButton("登录")
        self.login_button.clicked.connect(self.login)
        self.login_button.setVisible(False)
        right_layout.addWidget(self.login_button)

        self.changeButton()

        self.changeText()

        return card

    def changeButton(self):
        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)

        if logined:
            self.login_button.hide()
            self.logout_button.show()
        else:
            self.login_button.show()
            self.logout_button.hide()

    def changeText(self):
        name = self.config.get(CONFIG_ACCOUNT_NAME, "未登录")
        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)
        is_vip = self.config.get(CONFIG_ACCOUNT_IS_VIP, False)
        phone = self.config.get(CONFIG_ACCOUNT_PHONE, "")

        if logined:
            avator = QIcon(AVATOR_PATH)

            if is_vip:
                vip_str = "会员"
            else:
                vip_str = "非会员"

        else:
            avator = FIF.PEOPLE.icon()
            vip_str = ""

        if phone is None:
            phone_str = "未绑定"
        else:
            phone_str = phone

        self.icon.setPixmap(avator.pixmap(32, 32))

        self.name_label.setText(name)
        self.phone_label.setText(f"{phone_str} {vip_str}")


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
        progress.setFixedSize(*PROGRESS_RING_SIZE)
        self.viewLayout.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)

        content_layout = QVBoxLayout()

        content_layout.addWidget(TitleLabel(title), alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_label = BodyLabel(content)
        content_layout.addWidget(self.content_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.viewLayout.addLayout(content_layout)


        self.buttonGroup.deleteLater()
        self.buttonLayout.deleteLater()


class MainWindow(FluentWindow):
    def __init__(self, config, logger):
        super().__init__()

        import libs.pages_logical as logical

        self.config = config
        self.logger = logger

        self.setWindowTitle(WINDOW_TITLE) # 设置窗口标题

        self.searchInterface = logical.SearchPage(config, logger, self)
        self.searchInterface.setObjectName("searchInterface")
        
        self.preferredInterface = logical.Preferred(config, logger, self)
        self.preferredInterface.setObjectName("preferredInterface")

        self.localInterface = logical.LocalPage(self)
        self.localInterface.setObjectName("localInterface")

        self.settingInterface = logical.SettingsPage(self)
        self.settingInterface.setObjectName("settingInterface")

        self.avatorInterface = logical.AccountPage(self.config, self.logger, self)
        self.avatorInterface.setObjectName("avatorInterface")

        self.initNavigation()
         
    def initNavigation(self):

        self.addSubInterface(self.searchInterface, FIF.DOCUMENT, "试卷")
        self.addSubInterface(self.preferredInterface, FIF.FLAG, "优选")

        self.addSubInterface(self.localInterface, FIF.FOLDER, "本地")

        self.initAvator()

        self.addSubInterface(self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)

    def initAvator(self):

        logined = self.config.get(CONFIG_ACCOUNT_LOGIN, False)
        name = self.config.get(CONFIG_ACCOUNT_NAME, "未登录")

        if logined:
            avator = QIcon(AVATOR_PATH)
        else:
            avator = FIF.PEOPLE

        self.addSubInterface(self.avatorInterface, avator, name, NavigationItemPosition.BOTTOM)

