# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from mangoui import *


class MenuPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.mango_tabs = MangoTabs()
        self.layout.addWidget(self.mango_tabs)

        self.layout_1 = QVBoxLayout(self)
        self.mango_tabs.add_tab(self.layout_1, 'tabs1', )
        self.layout_3 = QVBoxLayout(self)
        self.mango_tabs.add_tab(self.layout_3, 'tabs2', )
        self.layout_2 = QVBoxLayout(self)
        self.mango_tabs.add_tab(self.layout_2, '新增')
