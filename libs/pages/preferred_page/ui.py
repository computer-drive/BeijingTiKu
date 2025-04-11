from libs.consts import *
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import (
    LargeTitleLabel,
    BodyLabel,
    ToolButton,
    ComboBox,
    IndeterminateProgressRing,
    SpinBox,
    TreeWidget,
    PrimaryPushButton,
    SmoothMode,
    SingleDirectionScrollArea,
)
from qfluentwidgets import FluentIcon as FIF


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
        self.page_layout.addWidget(
            self.page_back_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.page_label = BodyLabel("-/- 共 - 条")
        self.page_layout.addWidget(
            self.page_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.page_forward_button = ToolButton(FIF.RIGHT_ARROW)
        self.page_forward_button.setToolTip("下一页")
        self.page_layout.addWidget(
            self.page_forward_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

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
        self.content_data_layout.addWidget(
            self.search_loading,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
        )

    def initSearchNull(self):

        self.icon_label = BodyLabel(SEARCH_NULL_TEXT)
        self.icon_label.setStyleSheet("font-size: 60px;")
        self.content_data_layout.addWidget(
            self.icon_label,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
        )

        self.null_label = BodyLabel("没有找到相关内容")
        self.null_label.setStyleSheet("font-size: 20px;")
        self.content_data_layout.addWidget(
            self.null_label,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
        )
