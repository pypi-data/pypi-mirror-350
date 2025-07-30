# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoSlider(QSlider):
    def __init__(self):
        super().__init__()

        self.set_style_sheet()

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        /* HORIZONTAL */
        QSlider {{ margin: {0}px; }}
        QSlider::groove:horizontal {{
            border-radius: {10}px;
            height: {0}px;
        	margin: 0px;
        	background-color: {THEME.bg_200};
        }}
        QSlider::groove:horizontal:hover {{ background-color: {THEME.primary_200}; }}
        QSlider::handle:horizontal {{
            border: none;
            height: {16}px;
            width: {16}px;
            margin: {2}px;
        	border-radius: {THEME.border_radius}px;
            background-color: {THEME.bg_300};
        }}
        QSlider::handle:horizontal:hover {{ background-color: {THEME.primary_100}; }}
        QSlider::handle:horizontal:pressed {{ background-color: {THEME.primary_200}; }}

        /* VERTICAL */
        QSlider::groove:vertical {{
            border-radius: {10}px;
            width: {20}px;
            margin: 0px;
        	background-color: {THEME.primary_100};
        }}
        QSlider::groove:vertical:hover {{ background-color: {THEME.primary_100}; }}
        QSlider::handle:vertical {{
        	border: none;
            height: {16}px;
            width: {16}px;
            margin: {2}px;
        	border-radius: {8}px;
            background-color: {THEME.accent_200};
        }}
        QSlider::handle:vertical:hover {{ background-color: {THEME.primary_100}; }}
        QSlider::handle:vertical:pressed {{ background-color: {THEME.primary_200}; }}
        """)
