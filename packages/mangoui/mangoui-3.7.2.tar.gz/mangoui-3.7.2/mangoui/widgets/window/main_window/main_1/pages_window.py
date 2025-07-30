# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME
from mangoui.widgets.display.mango_label import MangoLabel


class PagesWindow:

    def __init__(self, parent, content_area_left_frame, page_dict):
        self.parent = parent
        self.content_area_left_frame = content_area_left_frame
        self.page_dict = page_dict

        self.loading_indicator = MangoLabel("数据加载中...")
        self.loading_indicator.setAlignment(Qt.AlignCenter)  # type: ignore
        self.loading_indicator.setStyleSheet(f"font-size: 16px; color: {THEME.bg_100};")

        self.main_pages_layout = QVBoxLayout(self.content_area_left_frame)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setContentsMargins(0, 0, 0, 0)
        self.pages = QStackedWidget(self.content_area_left_frame)
        self.main_pages_layout.addWidget(self.pages)
        QMetaObject.connectSlotsByName(self.content_area_left_frame)

    def set_page(self, page: str, data: dict | None = None):
        page_class = self.page_dict.get(page)
        if page_class is not None:
            page = page_class(self.parent)
        else:
            return
        page.data = data if data is not None and isinstance(data, dict) else {}
        if hasattr(page, 'show_data'):
            page.show_data()
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)

# import time
#
# from PySide6.QtCore import QThread, Signal
# from PySide6.QtWidgets import QVBoxLayout
#
# from mangoui.init import QStackedWidget, QApplication, QMetaObject, Qt
# from mangoui.settings.settings import THEME
# from mangoui.widgets.display.mango_label import MangoLabel
#
#
# class DataFetcher(QThread):
#     data_fetched = Signal(object)  # 信号，用于传递获取到的数据
#
#     def __init__(self, page):
#         super().__init__()
#         self.page = page
#
#     def run(self):
#         if hasattr(self.page, 'show_data'):
#             data = self.page.get_data()
#             self.data_fetched.emit({'page': self.page, 'data': data})
#
#
# class PagesWindow:
#
#     def __init__(self, parent, content_area_left_frame, page_dict):
#         self.parent = parent
#         self.content_area_left_frame = content_area_left_frame
#         self.page_dict = page_dict
#
#         self.loading_indicator = MangoLabel("数据加载中...")
#         self.loading_indicator.setAlignment(Qt.AlignCenter)  # type: ignore
#         self.loading_indicator.setStyleSheet(f"font-size: 16px; color: {THEME.icon_color};")
#
#         self.main_pages_layout = QVBoxLayout(self.content_area_left_frame)
#         self.main_pages_layout.setSpacing(0)
#         self.main_pages_layout.setContentsMargins(0, 0, 0, 0)
#         self.pages = QStackedWidget(self.content_area_left_frame)
#         self.main_pages_layout.addWidget(self.pages)
#         QMetaObject.connectSlotsByName(self.content_area_left_frame)
#
#     def set_page(self, page: str, data: dict | None = None):
#         s = time.time()
#         self.pages.addWidget(self.loading_indicator)
#         self.pages.setCurrentWidget(self.loading_indicator)
#
#         page_class = self.page_dict.get(page, None)
#         if page_class is None:
#             return
#         page = page_class(self.parent)
#
#         current_widget = self.pages.currentWidget()
#         if current_widget and current_widget != self.loading_indicator:
#             self.pages.removeWidget(current_widget)
#         if data is not None and isinstance(data, dict):
#             page.data = data
#         else:
#             page.data = {}
#         self.data_fetcher = DataFetcher(page)
#         self.data_fetcher.data_fetched.connect(self.on_data_fetched)
#         self.data_fetcher.start()
#         self.pages.addWidget(page)
#         self.pages.setCurrentWidget(page)
#
#     def on_data_fetched(self, page):
#         if page.get('page') != {}:
#             page.get('page').show_data(page.get('data'))
