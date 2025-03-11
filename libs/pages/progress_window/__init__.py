from qfluentwidgets import MessageBoxBase, TitleLabel, ProgressBar, CaptionLabel
from PySide6.QtWidgets import QHBoxLayout
from utility.format import format_time, format_capacity
from PySide6.QtCore import Qt

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
