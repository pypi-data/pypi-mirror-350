import asyncio

import sys
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class AsyncWorker(QObject):
    finished = Signal()
    progress = Signal(str)

    async def do_async_work(self):
        for i in range(10):
            await asyncio.sleep(1)  # 模拟异步工作
            self.progress.emit(f"Progress: {i + 1} seconds")
        self.finished.emit()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.start_button = QPushButton("Start Async Work")
        self.progress_label = QLabel("Progress: 0 seconds")
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.progress_label)
        self.setLayout(self.layout)

        self.worker = AsyncWorker()
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.async_task_finished)

        self.start_button.clicked.connect(self.start_async_task)

        self.timer = QTimer()
        self.timer.timeout.connect(self.run_pending)
        self.loop = asyncio.new_event_loop()  # 创建新的事件循环

    def start_async_task(self):
        self.timer.start(100)  # 每100毫秒检查一次
        asyncio.run_coroutine_threadsafe(self.worker.do_async_work(), self.loop)

    def run_pending(self):
        try:
            self.loop.run_until_complete(asyncio.sleep(0))  # 处理待处理的异步事件
        except Exception as e:
            print(f"Error: {e}")

    def update_progress(self, message):
        self.progress_label.setText(message)

    def async_task_finished(self):
        print(3)
        self.timer.stop()
        self.progress_label.setText("Task finished!")


# 创建 QApplication 实例
app = QApplication(sys.argv)

widget = MyWidget()
widget.show()

# 启动事件循环
app.exec()
