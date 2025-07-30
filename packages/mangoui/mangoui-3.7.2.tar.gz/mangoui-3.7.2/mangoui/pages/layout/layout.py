# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from mangoui import *


class LayoutPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MangoLabel('布局展示'))


class Layout1Page(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.mango_text = MangoTextEdit('')
        self.layout.addWidget(MangoLabel('布局展示1'))
        self.layout.addWidget(self.mango_text)
        # 初始化网络管理器
        self.network_manager = QNetworkAccessManager(self)

    def show_data(self):
        # 创建并发送请求
        url = QUrl("http://127.0.0.1:8000/test")
        request = QNetworkRequest(url)

        # 使用 lambda 直接处理响应
        self.network_manager.get(request).finished.connect(
            lambda reply: self.mango_text.set_value(
                reply.readAll().data().decode('utf-8') if not reply.error() else f"Error: {reply.errorString()}"
            )
        )

    # def get_data(self):
    #     import http.client
    #     conn = http.client.HTTPConnection("127.0.0.1", 8000)
    #     payload = ''
    #     headers = {}
    #     conn.request("GET", "/test", payload, headers)
    #     res = conn.getresponse()
    #     data = res.read()
    #     return data
    #
    # def show_data(self, data):
    #     self.mango_text.set_value(data.decode("utf-8"))


class Layout2Page(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MangoLabel('布局展示2'))


class Layout3Page(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MangoLabel('布局展示3'))


class Layout4Page(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MangoLabel('布局展示4'))
