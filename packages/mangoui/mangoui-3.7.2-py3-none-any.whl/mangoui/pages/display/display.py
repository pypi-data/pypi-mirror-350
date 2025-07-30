# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from mangoui import *


class DisplayPage(QWidget):
    table_menu = [
        {'name': '编辑', 'action': 'edit'},
        {'name': '删除', 'action': 'delete'}
    ]
    table_column = [
        {'key': 'id', 'name': 'ID', 'width': 7},
        {'key': 'name', 'name': '角色名称', 'width': 300},
        {'key': 'description', 'name': '角色描述', },
        {'key': 'label', 'name': '标签', 'type': 2},
        {'key': 'status', 'name': '状态', 'type': 3},
        {'key': 'ope', 'name': '操作', 'type': 1, 'width': 120},
    ]

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.page = 1
        self.page_size = 20
        self.layout = QVBoxLayout(self)
        self.table_column = [TableColumnModel(**i) for i in self.table_column]
        self.table_menu = [TableMenuItemModel(**i) for i in self.table_menu]
        self.table_widget = TableList(self.table_column, self.table_menu, )
        self.table_widget.pagination.click.connect(self.pagination_clicked)
        self.table_widget.clicked.connect(self.callback)
        self.table_widget.table_widget.toggle_click.connect(self.update_data)
        but = MangoPushButton('点击')
        but.clicked.connect(self.batch)
        self.layout.addWidget(but)
        self.layout.addWidget(self.table_widget)

    def show_data(self):
        data = []
        for i in range(50):
            data.append({
                "id": i,
                "create_time": "2023-07-13T12:39:57",
                "update_time": "2023-07-13T12:39:57",
                "name": "开发经理",
                "label": f"嘿嘿{i}",
                "status": 1,
                "description": "管理所有开发人员权限"
            })
        self.table_widget.set_data(data, 10)

    def update_data(self, data):
        print(data)

    def pagination_clicked(self, data):
        if data['action'] == 'prev':
            self.page = data['page']
        elif data['action'] == 'next':
            self.page = data['page']
        elif data['action'] == 'per_page':
            self.page_size = data['page']
        self.show_data()

    def callback(self, data):
        action = data.get('action')
        if action and hasattr(self, action):
            if data.get('row'):
                getattr(self, action)(row=data.get('row'))
            else:
                getattr(self, action)()

    def batch(self):
        print(self.table_widget.table_widget.get_selected_items())
