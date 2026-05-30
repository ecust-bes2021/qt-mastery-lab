"""
minimal_ui_demo.py - PySide6 最小 UI 教学参考

覆盖的基础点：
1. QApplication 创建与事件循环
2. QWidget 作为顶层窗口
3. 基本控件：QLabel / QPushButton / QLineEdit
4. 布局管理器：QVBoxLayout
5. 信号-槽连接
6. app.exec() 启动事件循环

运行方式：
    python minimal_ui_demo.py

Qt6 C++ 对应机制:
    - QApplication(argc, argv) 在 C++ 中需要 int& argc，PySide6 自动处理
    - C++ 中 QWidget 默认不显示，必须调用 show()，PySide6 相同
    - C++ 中布局生效需要 setLayout()，PySide6 相同
    - C++ 中 connect() 是静态/成员函数，PySide6 用更 Pythonic 的 signal.connect(slot)
    - C++ 中的 moc 预处理在 PySide6 中由 Shiboken 自动生成
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
)
from PySide6.QtCore import Qt


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Minimal Demo")
        self.resize(400, 200)

        self._label = QLabel("输入后点击按钮")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._line_edit = QLineEdit()
        self._line_edit.setPlaceholderText("在这里输入一些文字...")

        self._button = QPushButton("显示输入内容")

        layout = QVBoxLayout()
        layout.addWidget(self._label)
        layout.addWidget(self._line_edit)
        layout.addWidget(self._button)
        self.setLayout(layout)

        # 信号-槽：按钮点击 -> 更新标签文本
        self._button.clicked.connect(self._on_button_clicked)

    # ---- 槽函数 ----

    def _on_button_clicked(self):
        text = self._line_edit.text().strip()
        if text:
            self._label.setText(f"你输入了: {text}")
        else:
            self._label.setText("输入内容为空")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()