# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoPushButton(QPushButton):
    def __init__(
            self,
            text,
            parent=None,
            **kwargs
    ):
        super().__init__()
        self.setText(text)
        self.kwargs = kwargs

        if parent:
            self.setParent(parent)

        self.set_stylesheet()
        self.setCursor(Qt.PointingHandCursor)  # type: ignore

    def set_stylesheet(self, height=35, width=60):
        style = f'''
        QPushButton {{
            border: {THEME.border};
            color: {THEME.text_100};
            border-radius: {THEME.border_radius};	
            background-color: {self.kwargs.get('color') if self.kwargs.get('color') else THEME.primary_100};
        }}
        QPushButton:hover {{
            background-color: {THEME.primary_200};
        }}
        QPushButton:pressed {{	
            background-color: {THEME.primary_300};
        }}
        '''
        self.setStyleSheet(style)
        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
