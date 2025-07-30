# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoCredits(QWidget):
    update_label = Signal(str)

    def __init__(self, copyright, version, ):
        super().__init__()
        self.copyright = copyright
        self.version = version

        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)

        style = f"""
        #bg_frame {{
            border-radius: {THEME.border_radius};
            background-color: {THEME.bg_300};
        }}
        .QLabel {{
            font: {THEME.font.text_size}pt "{THEME.font.family}";
            color: {THEME.text_100};
            padding-left: 10px;
            padding-right: 10px;
        }}
        """

        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(style)

        self.widget_layout.addWidget(self.bg_frame)

        self.bg_layout = QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)

        self.copyright_label = QLabel()
        self.copyright_label.setAlignment(Qt.AlignVCenter)  # type: ignore

        self.version_label = QLabel(f'{self.copyright}  Version：{self.version}')
        self.version_label.setAlignment(Qt.AlignVCenter)  # type: ignore

        self.separator = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # type: ignore

        self.bg_layout.addWidget(self.copyright_label)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)
        self.update_label.connect(self.set_text)

    def set_text(self, _str):
        self.copyright_label.setText(_str)
