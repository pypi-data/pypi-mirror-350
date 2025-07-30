from mangoui.models.models import AppConfig, MenusModel, Theme
from mangoui.styles.qss import *

THEME = Theme(**qss_dict_1)

STYLE = AppConfig(**{
    "app_name": "芒果pyside6组件库",
    "version": "3.5.1",
    "copyright": "Copyright © By: 芒果味  2022-2025",
    "year": 2021,
    "theme_name": "mango",
    "custom_title_bar": True,
    "lef_menu_size": {
        "minimum": 50,
        "maximum": 240
    },
    "left_menu_content_margins": 3,
    "left_column_size": {
        "minimum": 0,
        "maximum": 240
    },
    "right_column_size": {
        "minimum": 0,
        "maximum": 240
    },
})

MENUS = MenusModel(**{
    "left_menus": [
        {
            "btn_icon": ":/icons/home.svg",
            "btn_id": "home",
            "btn_text": "首页",
            "btn_tooltip": "首页",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": ":/icons/app_icon.svg",
            "btn_id": "layout",
            "btn_text": "布局",
            "btn_tooltip": "布局",
            "show_top": True,
            "is_active": False,
            "submenus": [
                {
                    "btn_id": "layout_page_1",
                    "btn_text": "布局1",
                    "btn_tooltip": "布局1",
                    "show_top": True,
                    "is_active": False
                },
                {
                    "btn_id": "layout_page_2",
                    "btn_text": "布局2",
                    "btn_tooltip": "布局2",
                    "show_top": True,
                    "is_active": False
                },

            ]
        },
        {
            "btn_icon": ":/icons/calendar_clock.svg",
            "btn_id": "input",
            "btn_text": "输入",
            "btn_tooltip": "输入",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/command.svg",
            "btn_id": "feedback",
            "btn_text": "反馈",
            "btn_tooltip": "反馈消息",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/compass.svg",
            "btn_id": "component",
            "btn_text": "公共",
            "btn_tooltip": "公共组件",
            "show_top": True,
            "is_active": False,
            "submenus": [
                {
                    "btn_id": "component_page_3",
                    "btn_text": "布局3",
                    "btn_tooltip": "布局3",
                    "show_top": True,
                    "is_active": False
                },
                {
                    "btn_id": "component_page_4",
                    "btn_text": "布局4",
                    "btn_tooltip": "布局4",
                    "show_top": True,
                    "is_active": False
                },

            ]
        },
        {
            "btn_icon": ":/icons/down.svg",
            "btn_id": "container",
            "btn_text": "容器",
            "btn_tooltip": "容器",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/fill.svg",
            "btn_id": "charts",
            "btn_text": "图表",
            "btn_tooltip": "图表",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/home.svg",
            "btn_id": "display",
            "btn_text": "显示",
            "btn_tooltip": "显示",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_add_user.svg",
            "btn_id": "graphics",
            "btn_text": "图形",
            "btn_tooltip": "图形",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_arrow_left.svg",
            "btn_id": "menu",
            "btn_text": "菜单",
            "btn_tooltip": "菜单",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_arrow_right.svg",
            "btn_id": "window",
            "btn_text": "窗口",
            "btn_tooltip": "窗口",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_info.svg",
            "btn_id": "miscellaneous",
            "btn_text": "其他",
            "btn_tooltip": "其他",
            "show_top": True,
            "is_active": False
        },

    ],
    "title_bar_menus": [
        {
            "btn_icon": ":/icons/project.ico",
            "btn_id": "project",
            "btn_tooltip": "请选择项目",
            "is_active": False
        }, {
            "btn_icon": ":/icons/env.ico",
            "btn_id": "test_env",
            "btn_tooltip": "请选择测试环境",
            "is_active": False
        }
    ]
})

dd = {
    "theme_name": "Default",
    "radius": "8",
    "border_size": "1",
    "dark_one": "#9d83a4",
    "dark_two": "#dad1dd",
    "dark_three": "#EDEDED",
    "dark_four": "#A8A8A8",
    "bg_one": "#ffffff",
    "bg_two": "#c2b2c6",
    "bg_three": "#A8A8A8",

    "icon_color": "#000000",
    "icon_hover": "#353037",
    "icon_pressed": "#626062",
    "icon_active": "#000000",

    "context_color": "#6db65a",
    "context_hover": "#c2b2c6",
    "context_pressed": "#a993af",

    "text_title": "#000000",
    "text_foreground": "#000000",
    "text_description": "#000000",
    "text_active": "#000000",
    "white": "#ffffff",
    "pink": "#FF82AB",
    "green": "#00FF7F",
    "red": "#EE3B3B",
    "yellow": "#fdb933",
    "blue": "#33a3dc",
    "orange": "#faa755",
    "font": {
        "family": "微软雅黑",
        "title_size": 11,
        "text_size": 10
    }
}

"""
    --primary-100:#3F51B5;
    --primary-200:#757de8;
    --primary-300:#dedeff;
    --accent-100:#2196F3;
    --accent-200:#003f8f;
    --text-100:#333333;
    --text-200:#5c5c5c;
    --bg-100:#FFFFFF;
    --bg-200:#f5f5f5;
    --bg-300:#cccccc;
      
"""
