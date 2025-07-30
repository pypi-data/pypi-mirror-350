# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-08-24 17:16
# @Author : 毛鹏

from PySide6.QtWidgets import *


class MangoCheckBox(QCheckBox):
    def __init__(self, text=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.get_style()

    def get_style(self):
        # self.setStyleSheet()
        pass

    def isChecked(self):
        return super().isChecked()

    def setChecked(self, checked):
        super().setChecked(checked)
