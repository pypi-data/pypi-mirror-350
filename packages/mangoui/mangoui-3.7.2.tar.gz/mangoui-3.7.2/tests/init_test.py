from PySide6.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem

from mangoui.settings.settings import THEME


class MangoTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('mango_table')
        print("Current styleSheet:", self.styleSheet())  # 打印当前样式表
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['A', 'B', 'C'])
        self.setRowCount(2)
        self.setItem(0, 0, QTableWidgetItem('Test'))


def generate_qss(theme):
    return f"""
        MangoLinePlot {{
            background: {theme.bg_200};
            border-radius: {theme.border_radius};
            padding: 12px;
        }}
        MangoPiePlot {{
            background: {theme.bg_200};
            border-radius: {theme.border_radius};
            padding: 12px;
        }}

        MangoCard {{
            background-color: {theme.primary_300};
            border: 1px solid {theme.primary_300};
            border-radius: {theme.border_radius};
            padding: 10px;
        }}
        MangoCard > QFrame {{
            background-color: {theme.primary_300};
            border: 1px solid {theme.primary_300};
            border-radius: {theme.border_radius};
            padding: 10px;
        }}
        MangoLabel {{
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
        QTimeEdit {{
            background-color: {theme.bg_100};
            border-radius: {theme.border_radius};
            border: {theme.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {theme.bg_100};
            selection-background-color: {theme.primary_200};
            color: {theme.text_100};
        }}

        QTimeEdit:focus {{
            border: {theme.border};
            background-color: {theme.bg_200};
        }}
        QTimeEdit::up-button, QTimeEdit::down-button {{
            border: none; /* 去掉边框 */
            background: transparent; /* 背景透明 */
            width: 0; /* 设置宽度为0 */
            height: 0; /* 设置高度为0 */
            margin: 0; /* 去掉外边距 */
            padding: 0; /* 去掉内边距 */
        }}
        MangoCascade {{
          background-color: {theme.bg_100}; /* 按钮背景颜色 */
          border-radius: {theme.border_radius}; /* 按钮圆角半径 */
          border: {theme.border}; /* 按钮边框样式 */
          padding-left: 10px;
          padding-right: 10px;
          padding: 5px; /* 按钮内边距 */
          color: {theme.text_100};
        }}

        MangoCascade:focus {{
          border: {theme.border}; /* 焦点时边框颜色 */
          background-color: {theme.bg_200}; /* 焦点时背景颜色 */
        }}

        MangoCascade::menu-indicator {{
          image: url(:/icons/down.svg); /* 下拉指示器图像 */
        }}

    """


def apply_theme():
    qss_style = generate_qss(THEME)
    QApplication.instance().setStyleSheet(qss_style)


if __name__ == "__main__":
    app = QApplication([])
    apply_theme()  # 应用主题
    window = QMainWindow()
    table = MangoTable()
    window.setCentralWidget(table)
    window.show()
    app.exec()
