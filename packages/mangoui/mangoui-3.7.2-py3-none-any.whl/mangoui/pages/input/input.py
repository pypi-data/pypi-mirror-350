# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from mangoui import *


class InputPage(QWidget):
    cascade_data = [{"value": 8, "label": "智投", "parameter": None, "children": [
        {"value": 13, "label": "新智投", "parameter": None,
         "children": [{"value": 107, "label": "登录", "parameter": None, "children": []},
                      {"value": 106, "label": "项目", "parameter": None, "children": []},
                      {"value": 105, "label": "小红书实时看版", "parameter": None, "children": []},
                      {"value": 104, "label": "报数助手", "parameter": None, "children": []},
                      {"value": 103, "label": "用户中心", "parameter": None, "children": []},
                      {"value": 102, "label": "首页", "parameter": None, "children": []}]},
        {"value": 6, "label": "老智投", "parameter": None,
         "children": [{"value": 93, "label": "小红星日报-搜索推广", "parameter": None, "children": []},
                      {"value": 92, "label": "小红星日报-信息流", "parameter": None, "children": []},
                      {"value": 91, "label": "登录", "parameter": None, "children": []}]}]},
                    {"value": 4, "label": "DESK", "parameter": None,
                     "children": [{"value": 4, "label": "ZDesk-二代", "parameter": None, "children": []},
                                  {"value": 1, "label": "ZDesk-低代码", "parameter": None,
                                   "children": [{"value": 81, "label": "收票单", "parameter": None, "children": []},
                                                {"value": 80, "label": "供应商管理", "parameter": None, "children": []},
                                                {"value": 79, "label": "供应商付款单", "parameter": None,
                                                 "children": []},
                                                {"value": 78, "label": "垫款管理", "parameter": None, "children": []},
                                                {"value": 77, "label": "低代码后台", "parameter": None, "children": []},
                                                {"value": 76, "label": "二代-充值申请", "parameter": None,
                                                 "children": []},
                                                {"value": 75, "label": "二代系统", "parameter": None, "children": []},
                                                {"value": 74, "label": "保证金付款单", "parameter": None,
                                                 "children": []},
                                                {"value": 73, "label": "供应商政策", "parameter": None, "children": []},
                                                {"value": 72, "label": "供应商列表", "parameter": None, "children": []},
                                                {"value": 71, "label": "常规授信设置", "parameter": None,
                                                 "children": []},
                                                {"value": 70, "label": "信用评级设置", "parameter": None,
                                                 "children": []},
                                                {"value": 69, "label": "临时垫款设置", "parameter": None,
                                                 "children": []},
                                                {"value": 68, "label": "巨量行业对应关系", "parameter": None,
                                                 "children": []},
                                                {"value": 67, "label": "销售指导政策设置", "parameter": None,
                                                 "children": []},
                                                {"value": 66, "label": "开户银行列表", "parameter": None,
                                                 "children": []},
                                                {"value": 65, "label": "结算方式推单设置", "parameter": None,
                                                 "children": []},
                                                {"value": 64, "label": "系统单据链路设置", "parameter": None,
                                                 "children": []},
                                                {"value": 63, "label": "线索池管理", "parameter": None, "children": []},
                                                {"value": 62, "label": "媒体平台/业务线/执行部门对应关系",
                                                 "parameter": None, "children": []},
                                                {"value": 61, "label": "供应商服务费用单", "parameter": None,
                                                 "children": []},
                                                {"value": 60, "label": "其他服务费用单", "parameter": None,
                                                 "children": []},
                                                {"value": 59, "label": "运营服务费用单", "parameter": None,
                                                 "children": []},
                                                {"value": 58, "label": "运营结算", "parameter": None, "children": []},
                                                {"value": 57, "label": "勾稽", "parameter": None, "children": []},
                                                {"value": 56, "label": "其他结算", "parameter": None, "children": []},
                                                {"value": 55, "label": "项目结算", "parameter": None, "children": []},
                                                {"value": 54, "label": "消耗结算", "parameter": None, "children": []},
                                                {"value": 53, "label": "充值结算", "parameter": None, "children": []},
                                                {"value": 52, "label": "消耗匹配明细", "parameter": None,
                                                 "children": []},
                                                {"value": 51, "label": "消耗同步", "parameter": None, "children": []},
                                                {"value": 50, "label": "营销点评列表", "parameter": None,
                                                 "children": []},
                                                {"value": 49, "label": "媒体账户关系组", "parameter": None,
                                                 "children": []},
                                                {"value": 48, "label": "媒体账户列表", "parameter": None,
                                                 "children": []},
                                                {"value": 47, "label": "媒体账户绑定", "parameter": None,
                                                 "children": []},
                                                {"value": 42, "label": "预收款管理", "parameter": None, "children": []},
                                                {"value": 31, "label": "合同管理", "parameter": None, "children": []},
                                                {"value": 30, "label": "非充值模块", "parameter": None, "children": []},
                                                {"value": 29, "label": "流水管理", "parameter": None, "children": []},
                                                {"value": 27, "label": "商机管理", "parameter": None, "children": []},
                                                {"value": 26, "label": "客户管理", "parameter": None, "children": []},
                                                {"value": 25, "label": "客资管理", "parameter": None, "children": []},
                                                {"value": 22, "label": "充值业务", "parameter": None, "children": []},
                                                {"value": 13, "label": "登录", "parameter": None, "children": []}]}]},
                    {"value": 3, "label": "CDXP", "parameter": None,
                     "children": [{"value": 11, "label": "GrowKnows", "parameter": None, "children": []}]},
                    {"value": 1, "label": "AIGC", "parameter": None,
                     "children": [{"value": 12, "label": "AIGC-SaaS", "parameter": None, "children": []},
                                  {"value": 10, "label": "AIGC-TMS", "parameter": None, "children": []},
                                  {"value": 7, "label": "AIGC日报", "parameter": None,
                                   "children": [{"value": 35, "label": "首页", "parameter": None, "children": []},
                                                {"value": 11, "label": "笔记历史", "parameter": None, "children": []},
                                                {"value": 10, "label": "家具", "parameter": None, "children": []},
                                                {"value": 9, "label": "装修", "parameter": None, "children": []},
                                                {"value": 8, "label": "配饰", "parameter": None, "children": []},
                                                {"value": 7, "label": "服饰", "parameter": None, "children": []},
                                                {"value": 6, "label": "品牌管理", "parameter": None, "children": []},
                                                {"value": 5, "label": "创作记录", "parameter": None, "children": []},
                                                {"value": 4, "label": "关键字", "parameter": None, "children": []},
                                                {"value": 3, "label": "信息流", "parameter": None, "children": []},
                                                {"value": 2, "label": "日报生成", "parameter": None, "children": []},
                                                {"value": 1, "label": "登录", "parameter": None, "children": []}]},
                                  {"value": 5, "label": "AIGC-SaaS-C端", "parameter": None,
                                   "children": [{"value": 97, "label": "文生图", "parameter": None, "children": []},
                                                {"value": 96, "label": "权益兑换", "parameter": None, "children": []},
                                                {"value": 95, "label": "智豆管理", "parameter": None, "children": []},
                                                {"value": 94, "label": "会员权益", "parameter": None, "children": []},
                                                {"value": 89, "label": "AI课堂", "parameter": None, "children": []},
                                                {"value": 88, "label": "知识库", "parameter": None, "children": []},
                                                {"value": 87, "label": "历史记录", "parameter": None, "children": []},
                                                {"value": 86, "label": "应用", "parameter": None, "children": []},
                                                {"value": 82, "label": "登录", "parameter": None, "children": []}]},
                                  {"value": 3, "label": "AIGC-WEB", "parameter": None, "children": []},
                                  {"value": 2, "label": "AIGC-SaaS", "parameter": None,
                                   "children": [{"value": 85, "label": "AI课堂", "parameter": None, "children": []},
                                                {"value": 84, "label": "历史记录", "parameter": None, "children": []},
                                                {"value": 83, "label": "应用", "parameter": None, "children": []},
                                                {"value": 45, "label": "语义搜索", "parameter": None, "children": []},
                                                {"value": 43, "label": "模版市场", "parameter": None, "children": []},
                                                {"value": 34, "label": "Flow列表", "parameter": None, "children": []},
                                                {"value": 33, "label": "所有模板", "parameter": None, "children": []},
                                                {"value": 32, "label": "模板管理", "parameter": None, "children": []},
                                                {"value": 24, "label": "创作模板", "parameter": None, "children": []},
                                                {"value": 21, "label": "小红书运营百事通", "parameter": None,
                                                 "children": []},
                                                {"value": 20, "label": "知识库", "parameter": None, "children": []},
                                                {"value": 19, "label": "文档分类", "parameter": None, "children": []},
                                                {"value": 18, "label": "个人中心", "parameter": None, "children": []},
                                                {"value": 17, "label": "首页", "parameter": None, "children": []},
                                                {"value": 16, "label": "文档库", "parameter": None, "children": []},
                                                {"value": 15, "label": "服饰达人", "parameter": None, "children": []},
                                                {"value": 14, "label": "登录", "parameter": None, "children": []}]}]}]
    combo_box_data = [{"id": 0, "name": "高"}, {"id": 1, "name": "中"}, {"id": 2, "name": "低"},
                      {"id": 3, "name": "极低"}]

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.mango_time_edit = MangoTimeEdit()
        self.layout.addWidget(self.mango_time_edit)

        self.mango_cascade = MangoCascade('多级选择', CascaderModel.get_model(self.cascade_data))
        self.layout.addWidget(self.mango_cascade)

        self.mango_checkbox = MangoCheckBox()
        self.layout.addWidget(self.mango_checkbox)

        self.mango_combobox = MangoComboBox('选择框', ComboBoxDataModel.get_model(self.combo_box_data))
        self.layout.addWidget(self.mango_combobox)

        # self.mango_icon_button = MangoIconButton(self, self)
        # self.layout.addWidget(self.mango_icon_button)

        self.mango_line_edit = MangoLineEdit('请输入内容')
        self.layout.addWidget(self.mango_line_edit)

        self.mango_push_button = MangoPushButton('按钮')
        self.layout.addWidget(self.mango_push_button)

        self.mango_slider = MangoSlider()
        self.layout.addWidget(self.mango_slider)

        self.mango_text_edit = MangoTextEdit('多行输入框')
        self.layout.addWidget(self.mango_text_edit)

        self.mango_toggle = MangoToggle()
        self.layout.addWidget(self.mango_toggle)
