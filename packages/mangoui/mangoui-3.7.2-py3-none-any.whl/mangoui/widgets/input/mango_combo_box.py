# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-04 17:32
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.models.models import ComboBoxDataModel, DialogCallbackModel
from mangoui.settings.settings import THEME


class MangoComboBoxMany(QComboBox):
    click = Signal(object)

    def __init__(self,
                 placeholder: str,
                 data: list[ComboBoxDataModel],
                 value: str = None,
                 parent=None):
        super().__init__(parent)
        self.dialog = None
        self.data = data
        self.parent = parent

        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.list_widget = QListWidget()
        self.list_widget.setContentsMargins(0, 0, 0, 0)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.list_widget)
        self.populate_list_widget()
        if placeholder:
            self.lineEdit().setPlaceholderText(placeholder)
            # 设置默认选项
        if value is not None:
            self.set_value(value)
        self.set_stylesheet()

    def populate_list_widget(self):
        for option in self.data:
            item = QListWidgetItem(option.name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # type: ignore
            item.setCheckState(Qt.Unchecked)  # type: ignore
            self.list_widget.addItem(item)

    def showPopup(self):
        if self.dialog is None:
            self.dialog = QDialog(self)
        else:
            self.dialog.setWindowTitle("选择项目")
            self.dialog.setFixedSize(200, 150)
            self.dialog.setLayout(self.layout)
            self.list_widget.itemChanged.connect(self.update_display)
            self.dialog.accepted.connect(self.update_display)
            self.dialog.exec()

    def update_display(self):
        selected_items = [self.list_widget.item(i).text() for i in range(self.list_widget.count()) if
                          self.list_widget.item(i).checkState() == Qt.Checked]  # type: ignore
        if selected_items:
            self.lineEdit().setText(", ".join(selected_items))
        else:
            self.lineEdit().clear()
            self.lineEdit().setPlaceholderText("选择项目")

    def get_value(self):
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count()) if
                self.list_widget.item(i).checkState() == Qt.Checked]  # type: ignore

    def set_value(self, value):
        try:
            value_list = eval(value) if isinstance(value, str) else value
        except Exception:
            value_list = [value]
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.text() in value_list:
                item.setCheckState(Qt.Checked)  # type: ignore
            else:
                item.setCheckState(Qt.Unchecked)  # type: ignore
        selected_values = [item.text() for i in range(self.list_widget.count()) if
                           self.list_widget.item(i).checkState() == Qt.Checked]  # type: ignore
        if selected_values:
            self.lineEdit().setText(", ".join(selected_values))
        else:
            self.lineEdit().clear()
            self.lineEdit().setPlaceholderText("选择项目")

        self.update_display()

    def set_stylesheet(self, icon=':/icons/down.svg'):

        style = f'''
        QComboBox {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius}px;
            border: {THEME.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {THEME.bg_100};
            selection-background-color: {THEME.color.color4};
            color: {THEME.text_100};
        }}
        QComboBox:focus {{
            border: {THEME.border};
            background-color: {THEME.bg_100};
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: transparent;
            background-image: url({icon}); /* 使用背景图像 */
            background-repeat: no-repeat;
            background-position: center;
            width: 20px; /* 设置下拉按钮的宽度 */
        }}
        '''
        self.setStyleSheet(style)
        self.setMinimumHeight(30)  # 设置最小高度


class MangoComboBox(QComboBox):
    click = Signal(object)

    def __init__(
            self,
            placeholder: str,
            data: list[ComboBoxDataModel],
            value: int | str = None,
            subordinate: str | None = None,
            is_form: bool = True,
            **kwargs,
    ):
        super().__init__()
        self.kwargs = kwargs
        self.placeholder = placeholder
        self.data = data
        self.value = value
        self.subordinate = subordinate
        self.is_form = is_form
        # 设置样式表
        self.set_stylesheet()
        self.currentIndexChanged.connect(self.combo_box_changed)
        self.set_select(self.data)
        self.setCurrentIndex(-1)
        self.set_value(self.value)
        if self.placeholder:
            self.setPlaceholderText(self.placeholder)

    def get_value(self):
        value = self.currentText()
        if self.data:
            data_dict = {item.name: item.id for item in self.data}
            return data_dict.get(value)

    def set_select(self, data: list[ComboBoxDataModel], clear: bool = False):
        if clear:
            self.clear()
        if data:
            self.data = data
            self.addItems([i.name for i in data])

    def set_value(self, value: str):
        if value is not None and value != '':
            for i in self.data:
                if i.id == str(value):
                    self.value = value
                    self.setCurrentText(i.name)
                    break
            else:
                self.value = ''
                self.setCurrentText('')
        elif value == '':
            self.value = ''
            self.setCurrentText('')

    def combo_box_changed(self, data):
        if self.is_form:
            if self.subordinate:
                self.click.emit(DialogCallbackModel(
                    key=self.kwargs.get('key'),
                    value=self.get_value(),
                    subordinate=self.subordinate,
                    input_object=self
                ))
        else:
            self.click.emit(self.get_value())

    def set_stylesheet(self, icon=':/icons/down.svg'):

        style = f'''
        QComboBox {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: {THEME.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {THEME.text_200};
            selection-background-color: {THEME.bg_100};
            color: {THEME.text_100};
        }}
        QComboBox:focus {{
            border: 1px solid {THEME.bg_300};
            background-color: {THEME.bg_100};
        }}
        QComboBox::drop-down {{
            border: none;
            background-color: transparent;
            background-image: url({icon}); /* 使用背景图像 */
            background-repeat: no-repeat;
            background-position: center;
            width: 20px; /* 设置下拉按钮的宽度 */
        }}
        '''
        self.setStyleSheet(style)
        self.setMinimumHeight(30)  # 设置最小高度
