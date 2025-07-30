# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-19 11:29
# @Author : 毛鹏
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoCard(QWidget):
    clicked = Signal(str)

    def __init__(self, layout, title: str | None = None, parent=None, name='', **kwargs):
        super().__init__(parent)
        self.name = name  # 唯一标识
        self.kwargs = kwargs
        layout.setContentsMargins(10, 0, 10, 0)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame()
        if title:
            self.frame_layout = QVBoxLayout()
            self.frame_layout.setContentsMargins(0, 0, 0, 0)
            self.frame.setLayout(self.frame_layout)
            title_label = QLabel(title)
            font = QFont()
            font.setPointSize(18)  # 设置字体大小
            font.setBold(True)  # 设置为粗体
            title_label.setFont(font)
            self.frame_layout.addWidget(title_label, 1)
            self.frame.setLayout(self.frame_layout)
            self.frame_layout_h = QHBoxLayout()
            self.frame_layout_h.setContentsMargins(10, 0, 0, 0)
            self.frame_layout_h.addLayout(layout)
            self.frame_layout.addLayout(self.frame_layout_h, 9)
        else:
            self.frame.setLayout(layout)
        self.layout.addWidget(self.frame)

        self.setLayout(self.layout)
        self.set_stylesheet()

    def enterEvent(self, event):
        if self.name:
            self.setCursor(Qt.PointingHandCursor)  # type: ignore
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self.name:
            self.setCursor(Qt.ArrowCursor)  # type: ignore
            super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # type: ignore
            self.clicked.emit(self.name)  # 发送点击信号
        super().mousePressEvent(event)  # 确保调用父类方法

    def set_stylesheet(self):
        self.setObjectName('mangoCard')
        background_color = self.kwargs.get('background_color')
        if background_color is None:
            background_color = THEME.bg_200
        style = f"""
        QWidget#mangoCard {{
            background-color: {background_color};
            border: 1px solid {background_color};
            border-radius: {THEME.border_radius};
            padding: 10px;
        }}
        QWidget#mangoCard > QFrame {{
            background-color: {background_color};
            border: 1px solid {background_color};
            border-radius: {THEME.border_radius};
            padding: 10px;
        }}

        """
        self.setStyleSheet(style)
