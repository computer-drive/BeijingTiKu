from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from qfluentwidgets import (PushButton, ComboBox, LineEdit, SpinBox,
                            PrimaryPushButton, IndeterminateProgressBar, 
                            CardWidget, IconWidget, ProgressBar, ComboBoxSettingCard, OptionsSettingCard, SwitchSettingCard,
                            SwitchButton, InfoBar, SingleDirectionScrollArea, SmoothMode, QConfig, OptionsConfigItem, OptionsValidator
                            )
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TitleLabel, BodyLabel, LargeTitleLabel, CaptionLabel, SubtitleLabel
from typing import Literal

class SearchPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        progress = IndeterminateProgressBar()
        progress.setVisible(False)
        v_layout.addWidget(progress)
        
        # 搜索窗口-标题
        v_layout.addWidget(LargeTitleLabel("搜索"))

        v_layout.addLayout(self.initSearch())


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
        search_button = PrimaryPushButton("搜索")
        args_layout.addWidget(search_button)

        return h_layout
    
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

        socall_area = SingleDirectionScrollArea(orient=Qt.Vertical)
        socall_area.setWidgetResizable(True)
        socall_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        socall_area.setStyleSheet("QScrollArea{background: transparent; border: none}")
        socall_area.setSmoothMode(SmoothMode.NO_SMOOTH)
        self.v_layout.addWidget(socall_area)

        setting_widget = QWidget(self, objectName="setting_widget")
        setting_widget.setStyleSheet("QWidget{background: transparent;}") 

        v_layout = QVBoxLayout(setting_widget)

        # 设置窗口-标题
        test = LargeTitleLabel("设置")
        test.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_layout.addWidget(test, stretch=1)

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
        v_layout.addWidget(self.show_advanced_setting, alignment=Qt.AlignmentFlag.AlignLeft)

        self.advanced_frame = QFrame(self)
        # self.advanced_frame.setHidden(True)


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
            [self.show_delay_input, self.dalay_input]
        ))
        self.advanced_frame.setLayout(advanced_layout)


        v_layout.addWidget(self.advanced_frame)

        setting_widget.setLayout(v_layout)
        
        socall_area.setWidget(setting_widget)

        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)




if __name__ == "__main__":
    app = QApplication([])
    w = SettingsPage()
    w.show()

    app.exec_()