from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from libs.consts import *
import os


class MaterialIcon(QIcon):
    def __init__(self, name: str, width: int = 32, height: int = 32):
        if os.path.exists(f"{ICON_PATH}{name}.svg"):
            super().__init__(
                QPixmap(f"{ICON_PATH}{name}.svg").scaled(
                    width, height, Qt.KeepAspectRatio
                )
            )

        else:
            raise ValueError(f"Icon {name} not found.")
