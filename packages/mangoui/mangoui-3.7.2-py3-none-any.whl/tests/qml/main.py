import sys
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qml_file = "main.qml"
    qml_url = QUrl.fromLocalFile(qml_file)
    qml_engine = QQmlApplicationEngine()

    # 加载QML文件并运行应用程序
    qml_engine.load(qml_url)

    if not qml_engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
