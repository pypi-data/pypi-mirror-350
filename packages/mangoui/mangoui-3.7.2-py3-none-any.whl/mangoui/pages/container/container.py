# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-19 11:29
# @Author : 毛鹏

from mangoui import *


class ContainerPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)

        for i in range(10):
            self.layout_g = QGridLayout()
            self.mango_card = MangoCard(self.layout_g)
            self.layout.addWidget(self.mango_card)
            self.layout_g.addWidget(MangoLabel(f'卡片--{i}'))
