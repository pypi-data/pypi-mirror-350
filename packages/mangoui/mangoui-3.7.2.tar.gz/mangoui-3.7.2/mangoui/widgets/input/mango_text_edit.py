# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-18 11:11
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoTextEdit(QTextEdit):
    click = Signal(object)

    def __init__(self, placeholder, value: str | None = None, subordinate: str | None = None):
        super().__init__()
        self.value = value
        self.subordinate = subordinate

        if placeholder:
            self.setPlaceholderText(placeholder)

        if self.value:
            self.set_value(self.value)
        self.set_stylesheet()

    def set_value(self, text: str):
        self.setPlainText(text)

    def get_value(self):
        return self.toPlainText()

    def set_stylesheet(self):
        style = f"""
        QTextEdit {{
        	background-color: {THEME.bg_100};
        	border-radius: {THEME.border_radius};
        	border: {THEME.border};
        	padding-left: 10px;
            padding-right: 10px;
        	selection-color: {THEME.text_100};
        	selection-background-color: {THEME.bg_300};
            color: {THEME.text_100};
        }}

        QTextEdit:focus {{
            border: {THEME.border};
            background-color: {THEME.bg_200};
        }}
        """
        self.setStyleSheet(style)
