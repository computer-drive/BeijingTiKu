from PyQt5.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QWidget
from PyQt5.QtCore import Qt
from qfluentwidgets import (SingleDirectionScrollArea, SmoothMode, LargeTitleLabel, BodyLabel,
                            ProgressBar, PushButton, SwitchButton, SpinBox, GroupHeaderCardWidget
                            )
from libs.consts import *
from ...widgets.material_icon import MaterialIcon as MIcon


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
