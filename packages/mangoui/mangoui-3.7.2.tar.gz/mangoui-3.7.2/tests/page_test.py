import sys
from tests.异步支持1 import QComboCheckBox

from mangoui import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Tabs Example")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.tab_widget = QComboCheckBox()
        self.tab_widget.addItems(['选项1', '选项2', '选项3'])
        self.but = MangoPushButton('点击')
        self.but.clicked.connect(self.button_clicked)
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.but)

        self.setLayout(layout)

    def button_clicked(self):
        print(self.tab_widget.get_text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
