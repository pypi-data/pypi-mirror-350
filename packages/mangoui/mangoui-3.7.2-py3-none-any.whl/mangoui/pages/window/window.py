# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from mangoui import *


class WindowPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MangoLabel('窗口'))
        self.push_button = MangoPushButton('点击')
        self.layout.addWidget(self.push_button)
        self.push_button.clicked.connect(self.click)

    def click(self):
        self.parent.credits.update_label.emit('hhhh')
