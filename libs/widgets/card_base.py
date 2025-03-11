from typing import Literal, Callable
from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QToolButton
from PySide6.QtCore import Qt
from qfluentwidgets import (CardWidget, TitleLabel, SubtitleLabel,
                             BodyLabel, InfoBadge, PushButton)

class CardBase(CardWidget):
    def __init__(self, left: QWidget, right: QWidget, config, logger, parent=None):
        super().__init__(parent)

        self.config = config
        self.logger = logger
        self.parent_ = parent

        self.left_widget = left
        self.right_widget = right

        h_layout = QHBoxLayout()

        h_layout.addWidget(left)

        h_layout.addWidget(right)

        self.setLayout(h_layout)


class ItemCard(CardBase):
    def __init__(self, config, logger, parent=None):
        super().__init__( QWidget(), QWidget(), config, logger, parent)

        self.config = config
        self.logger = logger
        self.parent_ = parent

        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.left_widget.setLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.right_widget.setLayout(self.right_layout)


    def addText(self, content:str, style:Literal["title", "subtitle", "body", "badge"]="body", color:str="", stylesheet:str=""):
        match style:
            case "title":
                label = TitleLabel(content)
            case "subtitle":
                label = SubtitleLabel(content)
            case "body":
                label = BodyLabel(content)
            case "badge":
                label = InfoBadge.custom(content, color, color)
        
        if style != "":
            label.setStyleSheet(stylesheet)

        self.left_layout.addWidget(label)

        return label

    def addTexts(self, contents: list[tuple[str, Literal["title", "subtitle", "body", "badge"], str, str]]):
        layout = QHBoxLayout()
        for content in contents:
            layout.addWidget(self.addText(*content))


    def addButton(self, button: QPushButton | QToolButton | list[tuple[PushButton | QToolButton, Callable]], func: Callable = None):
        if isinstance(button, QPushButton) or isinstance(button, QToolButton):
            self.right_layout.addWidget(button)
            if func is not None:
                button.clicked.connect(func)
            
            return button

        elif isinstance(button, list):
            button_layout = QHBoxLayout()

            return_data = []

            for btn, func in button:
                btn.clicked.connect(func)
                button_layout.addWidget(btn)
                return_data.append(btn)

            self.right_layout.addLayout(button_layout)

            return return_data

        else:
            raise TypeError("button must be QPushButton, QToolButton or list[tuple[QPushButton | QToolButton, Callable]]")