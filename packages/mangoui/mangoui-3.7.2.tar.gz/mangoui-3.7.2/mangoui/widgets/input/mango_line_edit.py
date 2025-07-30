# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from mangoui.models.models import DialogCallbackModel
from mangoui.settings.settings import THEME


class MangoLineEdit(QLineEdit):
    click = Signal(object)
    mouse_remove = Signal(object)

    def __init__(
            self,
            placeholder,
            value: str | None = None,
            subordinate: str | None = None,
            is_password: bool = False,
            **kwargs
    ):
        super().__init__()
        self.editingFinished.connect(self.line_edit_changed)
        self.subordinate = subordinate
        self.value = value
        self.kwargs = kwargs
        if is_password:
            self.setEchoMode(QLineEdit.Password)  # type: ignore
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.set_value(self.value)
        self.set_stylesheet()

    def get_value(self):
        return self.text()

    def set_value(self, value):
        self.value = value
        if self.value is not None:
            self.setText(str(self.value))

    def line_edit_changed(self, ):
        if self.subordinate:
            self.click.emit(DialogCallbackModel(
                key=self.kwargs.get('key'),
                value=self.text(),
                subordinate=self.subordinate,
                input_object=self
            ))
        else:
            self.click.emit(self.get_value())

    def focusOutEvent(self, event):
        self.click.emit(self.get_value())
        super().focusOutEvent(event)

    def set_stylesheet(self):
        style = f"""
        QLineEdit {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: {THEME.border};
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {THEME.text_100};
            selection-background-color: {THEME.bg_300};
            color: {THEME.text_100};
        }}

        QLineEdit:focus {{
            border: {THEME.border};
            background-color: {THEME.bg_200};
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(30)
