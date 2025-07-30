# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-01 14:27
# @Author : 毛鹏
from mangoui import *


class FeedbackPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout_h = QHBoxLayout()
        self.success = MangoPushButton('成功')
        self.success.clicked.connect(self.success_click)
        self.layout_h.addWidget(self.success)
        self.warning = MangoPushButton('警告')
        self.warning.clicked.connect(self.warning_click)
        self.layout_h.addWidget(self.warning)
        self.info = MangoPushButton('提示')
        self.info.clicked.connect(self.info_click)
        self.layout_h.addWidget(self.info)
        self.error = MangoPushButton('失败')
        self.error.clicked.connect(self.error_click)
        self.layout_h.addWidget(self.error)
        self.layout.addLayout(self.layout_h)
        self.layout_h_2 = QHBoxLayout()
        self.success_msg = MangoPushButton('成功')
        self.success_msg.clicked.connect(self.success_message)
        self.layout_h_2.addWidget(self.success_msg)
        self.warning_msg = MangoPushButton('警告')
        self.warning_msg.clicked.connect(self.warning_message)
        self.layout_h_2.addWidget(self.warning_msg)
        self.info_msg = MangoPushButton('提示')
        self.info_msg.clicked.connect(self.info_message)
        self.layout_h_2.addWidget(self.info_msg)
        self.error_msg = MangoPushButton('失败')
        self.error_msg.clicked.connect(self.error_message)
        self.layout_h_2.addWidget(self.error_msg)
        self.layout.addLayout(self.layout_h_2)

    def success_click(self):
        success_notification(self, '这是一个成功的提示！')

    def info_click(self):
        info_notification(self, '这是一个info的提示！')

    def warning_click(self):
        warning_notification(self, '这是一个警告的提示！')

    def error_click(self):
        error_notification(self, '这是一个失败的提示！')

    def info_message(self):
        info_message(self, '这是一个info的提示啦啦啦啦啦啦啦啦啦这是一个info的提示')

    def error_message(self):
        error_message(self, '这是一个失败的提示')

    def success_message(self):
        success_message(self, '这是一个成功的提示')

    def warning_message(self):
        warning_message(self, '这是一个警告的提示')

    def show_data(self):
        pass
