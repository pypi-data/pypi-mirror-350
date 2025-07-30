# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoFrame(QFrame):

    def __init__(
            self,
            parent,
            layout=Qt.Vertical,  # type: ignore
            margin=0,
            spacing=2,
            text_font="9pt 'Segoe UI'",
            enable_shadow=True
    ):
        super().__init__()
        self.parent = parent
        self.layout = layout
        self.margin = margin
        self.text_font = text_font
        self.enable_shadow = enable_shadow

        self.setObjectName("pod_bg_app")

        self.set_stylesheet()

        if layout == Qt.Vertical:  # type: ignore
            self.layout = QHBoxLayout(self)
        else:
            self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(spacing)

        if enable_shadow:
            self.shadow = QGraphicsDropShadowEffect()
            self.shadow.setBlurRadius(20)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 160))
            self.setGraphicsEffect(self.shadow)

    def set_stylesheet(self, border_radius=None, border_size=None):

        style = f"""
            #pod_bg_app {{
                background-color: {THEME.bg_100};
                border-radius: {THEME.border_radius};
                border: {border_size if border_size else '1'}px solid {border_radius if border_radius else THEME.border};
            }}
            QFrame {{ 
                color: {THEME.text_100};
                font: {self.text_font};
            }}
            """
        self.setStyleSheet(style)
