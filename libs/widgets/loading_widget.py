from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QFrame
from qfluentwidgets import IndeterminateProgressRing, BodyLabel

class LoadingWidget(QWidget):
    def __init__(self, error_title:str, error_subtitle:str, null_title:str, null_subtitle:str, parent=None):
        super().__init__(parent)

        self.error_title = error_title
        self.error_subtitle = error_subtitle

        self.null_title = null_title
        self.null_subtitle = null_subtitle
    
    def initLoading(self):
        widget = QFrame()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(IndeterminateProgressRing())
        
        return widget
        
    def initError(self):
        widget = QFrame()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        title = BodyLabel(self.error_title)
        title.setStyleSheet("font-size: 60px;")
        layout.addWidget(title)

        subtitle = BodyLabel(self.error_subtitle)
        subtitle.setStyleSheet("font-size: 20px;")
        layout.addWidget()

        return widget

    def initNull(self):
        widget = QFrame()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        title = BodyLabel(self.null_title)
        title.setStyleSheet("font-size: 60px;")
        layout.addWidget(title)

        subtitle = BodyLabel(self.null_subtitle)
        subtitle.setStyleSheet("font-size: 20px;")
        layout.addWidget()

    def initUi(self):
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        self.stacked_widget = QStackedWidget()

        self.stacked_widget.addWidget(self.initLoading())
        self.stacked_widget.addWidget(self.initError())
        self.stacked_widget.addWidget(self.initNull())

        self.stacked_widget.setCurrentIndex(0)
        
    def showError(self):
        self.stacked_widget.setCurrentIndex(1)

    def showNull(self):
        self.stacked_widget.setCurrentIndex(2)

