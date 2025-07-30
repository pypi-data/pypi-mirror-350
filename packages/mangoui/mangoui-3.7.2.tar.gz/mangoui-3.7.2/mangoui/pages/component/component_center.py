# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-08-28 16:33
# @Author : 毛鹏

from mangoui import *


class ComponentPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area = MangoScrollArea(vertical_off=True, horizontal_off=True)

        self.contents = QWidget()
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setText(QCoreApplication.translate("PagesWindow", u"页面组件", None))

        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.title_label)
        self.description_label = QLabel(self.contents)
        self.description_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.description_label.setText(QCoreApplication.translate("组件中心",
                                                                  u"以下是所有自定义小部件\n"
                                                                  "哈哈哈哈哈",
                                                                  None))
        self.description_label.setWordWrap(True)
        self.verticalLayout.addWidget(self.description_label)
        self.scroll_area.setWidget(self.contents)

        self.layout.addWidget(self.scroll_area)

    def load_data(self):
        # 模拟延迟加载数据
        QTimer.singleShot(3000, self.show_data)  # 3秒后调用show_data方法

    def show_data(self):
        pass
