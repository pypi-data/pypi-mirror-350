# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-14 17:30
# @Author : 毛鹏
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget, QWidget

from mangoui.settings.settings import THEME


class MangoTabs(QTabWidget):
    clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.previous_index = 0
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""
            QTabWidget {{
                background-color: {THEME.bg_100};
                border-radius: 8px;
            }}
            
            QTabBar {{
                background: transparent;
                border-bottom: 2px solid {THEME.border};
                spacing: 4px;
            }}
            
            QTabBar::tab {{
                background: transparent;
                border: none;
                padding: 8px 16px;
                margin: 0 4px;
                color: {THEME.text_100};
                font-size: {THEME.font.text_size};
                border-radius: 4px 4px 0 0;
                transition: all 0.2s ease;
            }}
            
            QTabBar::tab:selected {{
                color: {THEME.text_100};
                border-bottom: 1px solid {THEME.bg_300};
                font-weight: 500;
            }}
            
            QTabBar::tab:hover {{
                background: {THEME.primary_200};
                color: {THEME.text_100};
            }}
            
            QTabBar::tab:pressed {{
                color: {THEME.text_100};
            }}
            
            QTabBar::tab:!selected:hover {{
                border-bottom: 2px solid {THEME.primary_200};
                color: {THEME.text_100};
            }}
            
            QTabBar::tab:!selected:pressed {{
                color: {THEME.text_100};
            }}
            
            QTabWidget::pane {{
                border: none;
                padding: 12px;
                border-radius: 0 0 8px 8px;
            }}
            
            QTabBar::close-button {{
                image: url(:/icons/icon_close.svg);
                subcontrol-position: right;
                padding: 4px;
            }}
            
            QTabBar::close-button:hover {{
                background: {THEME.primary_200};
                border-radius: 4px;
            }}
        """)

    def add_tab(self, layout, tab_name):
        new_tab = QWidget()
        new_tab.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 5, 0, 0)
        new_tab.setLayout(layout)
        self.addTab(new_tab, tab_name)
