# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-31 9:51
# @Author : 毛鹏
import asyncio
import os
from threading import Thread

from mangoui.pages import *
from mangoui.settings.settings import STYLE, MENUS

os.environ["QT_FONT_DPI"] = "96"


class AsyncioThread(Thread):

    def __init__(self, loop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self) -> None:
        self._loop.run_forever()


def t():
    loop = asyncio.new_event_loop()
    thd = AsyncioThread(loop)
    thd.start()
    return loop


def main():
    page_dict = {
        'home': HomePage,
        'component': ComponentPage,
        'feedback': FeedbackPage,
        'container': ContainerPage,
        'charts': ChartsPage,
        'display': DisplayPage,
        'graphics': GraphicsPage,
        'input': InputPage,
        'layout': LayoutPage,
        'layout_page_1': Layout1Page,
        'layout_page_2': Layout2Page,
        'component_page_3': Layout3Page,
        'component_page_4': Layout4Page,
        'menu': MenuPage,
        'miscellaneous': MiscellaneousPage,
        'window': WindowPage,
    }

    app = QApplication([])
    login_window = MangoMain1Window(STYLE, MENUS, page_dict, t())
    login_window.show()
    app.exec()


main()
