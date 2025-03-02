from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import (IndeterminateProgressBar, LargeTitleLabel, PrimaryPushButton, SmoothMode,
                             LineEdit, BodyLabel, ComboBox, SpinBox, ToolButton,  SingleDirectionScrollArea
                             )
from qfluentwidgets import FluentIcon as FIF
from libs.consts import *


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