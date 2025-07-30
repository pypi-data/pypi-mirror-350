# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-01-28 16:03
# @Author : 毛鹏
from PySide6.QtWidgets import QApplication


def generate_qss(theme):
    return f"""
        MangoLinePlot#mango_line_plot {{
            background: {theme.bg_200};
            border-radius: {theme.border_radius};
            padding: 12px;
        }}
        MangoPiePlot#mango_pie_plot {{
            background: {theme.bg_200};
            border-radius: {theme.border_radius};
            padding: 12px;
        }}

        MangoCard#mango_card {{
            background-color: {theme.primary_300};
            border: 1px solid {theme.primary_300};
            border-radius: {theme.border_radius};
            padding: 10px;
        }}
        MangoCard#mango_card > QFrame {{
            background-color: {theme.primary_300};
            border: 1px solid {theme.primary_300};
            border-radius: {theme.border_radius};
            padding: 10px;
        }}
        MangoLabel#mango_label {{
            background-color: transparent;
            color: black;
        }}

        MangoTable#mango_table {{
            background-color: {theme.bg_100};
            padding: 5px;
            border-radius: {theme.border_radius};
            gridline-color: {theme.bg_100};
            color: {theme.text_100};
            border: 0;
        }}
        MangoTable#mango_table::item {{
            border-color: none;
            padding-left: 5px;
            padding-right: 5px;
            border-bottom: {theme.border};
        }}
        MangoTable#mango_table::item:selected {{
            background-color: {theme.bg_200};
            color: {theme.text_100};
        }}

        MangoTable#mango_table QHeaderView::section {{
            background-color: {theme.primary_200};
            max-width: 30px;
            border: 1px solid {theme.bg_300};
            border-style: none;
            border-bottom: 1px solid {theme.bg_300};
            border-right: 1px solid {theme.bg_300};
        }}
        MangoTable#mango_table::horizontalHeader {{
            background-color: {theme.primary_200};
        }}
        MangoTable#mango_table QTableCornerButton::section {{
            border: none;
            background-color: {theme.bg_200};
            padding: 3px;
            border-top-left-radius: {theme.border_radius};
        }}
        MangoTable#mango_table QHeaderView::section:horizontal {{
            border: none;
            background-color: {theme.primary_200};
            padding: 3px;
        }}
        MangoTable#mango_table QHeaderView::section:vertical {{
            border: none;
            background-color: {theme.primary_200};
            padding-left: 5px;
            padding-right: 5px;
            border-bottom: {theme.border};
            margin-bottom: 1px;
        }}

        QScrollBar:horizontal {{
            border: none;
            background: {theme.bg_200};
            height: 8px;
            margin: 0px 21px 0 21px;
            border-radius: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {theme.bg_300};
            min-width: 25px;
            border-radius: 4px;
        }}
        QScrollBar::add-line:horizontal {{
            border: none;
            background: {theme.bg_300};
            width: 20px;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:horizontal {{
            border: none;
            background: {theme.accent_100};
            width: 20px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {{
            background: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}

        QScrollBar:vertical {{
            border: none;
            background: {theme.bg_100};
            width: 8px;
            margin: 21px 0 21px 0;
            border-radius: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {theme.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        QScrollBar::add-line:vertical {{
            border: none;
            background: {theme.bg_300};
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical {{
            border: none;
            background: {theme.bg_300};
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
            background: none;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        MangoTimeEdit#mango_time_edit {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius};
            border: {theme.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {theme.bg_100};
            selection-background-color: {theme.primary_200};
            color: {theme.text_100};
        }}
        
        MangoTimeEdit#mango_time_edit:focus {{
            border: {theme.border};
            background-color: {theme.bg_200};
        }}
        MangoTimeEdit::up-button, MangoTimeEdit::down-button {{
            border: none; /* 去掉边框 */
            background: transparent; /* 背景透明 */
            width: 0; /* 设置宽度为0 */
            height: 0; /* 设置高度为0 */
            margin: 0; /* 去掉外边距 */
            padding: 0; /* 去掉内边距 */
        }}
        MangoCascade#mango_cascade {{
          background-color: {theme.bg_100}; /* 按钮背景颜色 */
          border-radius: {theme.border_radius}; /* 按钮圆角半径 */
          border: {theme.border}; /* 按钮边框样式 */
          padding-left: 10px;
          padding-right: 10px;
          padding: 5px; /* 按钮内边距 */
          color: {theme.text_100};
        }}

        MangoCascade#mango_cascade:focus {{
          border: {theme.border}; /* 焦点时边框颜色 */
          background-color: {theme.bg_200}; /* 焦点时背景颜色 */
        }}

        MangoCascade#mango_cascade::menu-indicator {{
          image: url(:/icons/down.svg); /* 下拉指示器图像 */
        }}
        
        MangoCascade#mango_cascade QMenu {{
          background-color: {theme.bg_100}; /* 菜单背景颜色 */
          border: {theme.border}; /* 菜单边框样式 */
          padding: 0; /* 菜单内边距 */
        }}

        MangoCascade#mango_cascade QMenu::item {{
          padding: 10px 15px; /* 菜单项的内边距 */
          color: {theme.text_100}; /* 菜单项字体颜色 */
        }}

        MangoCascade#mango_cascade QMenu::item:selected {{
          background-color: {theme.bg_200}; /* 选中菜单项的背景颜色 */
          color: {theme.text_100}; /* 选中菜单项的字体颜色 */
        }}
        MangoComboBoxMany#mango_combo_box_many {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius}px;
            border: {theme.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {theme.bg_100};
            selection-background-color: {theme.text_100};
            color: {theme.text_100};
        }}
        MangoComboBoxMany#mango_combo_box_many:focus {{
            border: {theme.border};
            background-color: {theme.bg_100};
        }}
        MangoComboBoxMany#mango_combo_box_many::drop-down {{
            border: none;
            background-color: transparent;
            background-image: url(:/icons/down.svg); /* 使用背景图像 */
            background-repeat: no-repeat;
            background-position: center;
            width: 20px; /* 设置下拉按钮的宽度 */
        }}
        MangoComboBox#mango_combo_box {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius};
            border: {theme.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {theme.text_200};
            selection-background-color: {theme.bg_100};
            color: {theme.text_100};
        }}
        MangoComboBox#mango_combo_box:focus {{
            border: 1px solid {theme.bg_300};
            background-color: {theme.bg_100};
        }}
        MangoComboBox#mango_combo_box::drop-down {{
            border: none;
            background-color: transparent;
            background-image: url(:/icons/down.svg); /* 使用背景图像 */
            background-repeat: no-repeat;
            background-position: center;
            width: 20px; /* 设置下拉按钮的宽度 */
        }}
        MangoLineEdit#mango_line_edit {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius};
            border: {theme.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {theme.text_100};
            selection-background-color: {theme.bg_300};
            color: {theme.text_100};
        }}
        MangoLineEdit#mango_line_edit:focus {{
            border: {theme.border};
            background-color: {theme.bg_200};
        }}
        QPushButton#mango_push_button {{
            border: {theme.border};
            color: {theme.text_100};
            border-radius: {theme.border_radius};	
            background-color: {theme.primary_100};
        }}
        QPushButton#mango_push_button:hover {{
            background-color: {theme.primary_200};
        }}
        QPushButton#mango_push_button:pressed {{	
            background-color: {theme.primary_300};
        }}
        MangoTextEdit#mango_text_edit {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius};
            border: {theme.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {theme.text_100};
            selection-background-color: {theme.bg_300};
            color: {theme.text_100};
        }}
        MangoTextEdit#mango_text_edit:focus {{
            border: {theme.border};
            background-color: {theme.bg_200};
        }}
        MangoTabs#mango_tabs {{
                background-color: {theme.bg_100};
                border-radius: 8px;
        }}
        MangoDialog#mango_dialog {{
            background-color: {theme.bg_100}; /* 主体背景颜色 */
        }}
        MangoDialog#mango_dialog::title {{
            background-color: {theme.bg_100}; /* 标题栏背景颜色 */
            color: {theme.text_100}; /* 标题栏文字颜色 */
        }}
        MangoTree#mango_tree {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius};
            border: {theme.border};
            color: {theme.text_100};
        }}
    
        MangoTree#mango_tree::item {{
            padding: 5px;
            background-color: {theme.bg_100};
            color: {theme.text_100};
        }}
    
        MangoTree#mango_tree::item:selected {{
            background-color: {theme.bg_100};
            color: {theme.text_100};
        }}
        
        MangoTree#mango_tree::item:hover {{
            background-color: {theme.primary_200};
        }}
    """


# 切换主题
def apply_theme(theme):
    qss_style = generate_qss(theme)
    QApplication.instance().setStyleSheet(qss_style)
