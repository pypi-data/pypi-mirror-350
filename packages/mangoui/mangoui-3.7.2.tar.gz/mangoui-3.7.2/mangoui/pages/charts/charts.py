# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:19
# @Author : 毛鹏

from mangoui import *


class ChartsPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout(self)

        self.layout_v_1 = QVBoxLayout()
        self.layout.addLayout(self.layout_v_1, 3)

        self.label = MangoLabel(f'用例执行数')
        self.pie_plot_1 = MangoPiePlot()
        self.layout_v_1.addWidget(self.pie_plot_1)
        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(self.label, alignment=Qt.AlignCenter)  # type: ignore
        self.layout_v_1.addLayout(h_layout_1)

        self.layout_v_2 = QVBoxLayout()
        self.layout.addLayout(self.layout_v_2, 7)
        self.line_plot = MangoLinePlot('用例执行趋势图', '数量', '周')
        self.layout_v_2.addWidget(self.line_plot)

    def show_data(self):
        data = []
        response = {"api_count": [32, 19, 8, 10, 10, 12, 0, 3, 1, 1, 2, 0],
                    "ui_count": [15, 6, 1, 0, 0, 0, 0, 0, 0, 0, 2, 6]}
        data.append({'name': 'API', 'value': response.get('ui_count')})
        data.append({'name': 'UI', 'value': response.get('api_count')})
        self.line_plot.draw(data)
        self.pie_plot_1.draw([{"value": 177, "name": "前端"}, {"value": 180, "name": "接口"}])
