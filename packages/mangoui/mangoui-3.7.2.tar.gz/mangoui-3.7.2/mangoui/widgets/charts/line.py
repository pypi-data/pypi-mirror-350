# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-23 17:42
# @Author : 毛鹏
import numpy
import pyqtgraph
from PySide6.QtWidgets import QVBoxLayout, QWidget

from mangoui.settings.settings import THEME


class MangoLinePlot(QWidget):
    def __init__(self, title, left, bottom):
        super().__init__()
        # 创建绘图窗口
        self.plot_widget = pyqtgraph.PlotWidget()
        # 设置卡片样式
        self.setStyleSheet(f"""
            background: {THEME.bg_200};
            border-radius: {THEME.border_radius};
            padding: 12px;
        """)

        # 设置图表样式
        self.plot_widget.setBackground('transparent')
        self.plot_widget.setTitle(title, color='#333333', size='20pt')
        self.plot_widget.setLabel('left', left, color='#666666', size='12pt')
        self.plot_widget.setLabel('bottom', bottom, color='#666666', size='12pt')

        # 优化图例
        legend = self.plot_widget.addLegend()
        legend.setBrush('#FFFFFF')
        legend.setPen('#CCCCCC')
        legend.setLabelTextColor('#333333')
        legend.setOffset((10, 10))  # 调整图例位置

        # 启用鼠标交互
        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.setMenuEnabled(False)

        # 布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def draw(self, data: list[dict]):
        self.plot_widget.clear()

        days = numpy.arange(len(data[0]['value'])) + 1
        # 使用更美观的颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                  '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                  '#bcbd22', '#17becf']

        for index, item in enumerate(data):
            color = colors[index % len(colors)]
            self.plot_widget.plot(
                days,
                item['value'],
                pen=pyqtgraph.mkPen(color, width=2.5),
                name=item['name'],
                width=2.5,
                symbol='o',
                symbolSize=8,
                symbolBrush=color,
                symbolPen='k',
                shadowPen=pyqtgraph.mkPen('#000000', width=1.5)
            )
