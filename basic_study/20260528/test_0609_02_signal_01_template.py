"""
阶段①：自定义信号的定义与发射（模板）
- Signal(type) 定义在 class body
- emit() 发射信号
- connect() 连接信号到槽函数
- 最小闭环：按钮点击 -> emit 自定义信号 -> 槽函数更新 UI
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal


class SignalDemo(QWidget):

    # TODO(1): 定义自定义信号 count_updated，携带一个 int 参数
    ???

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Practice - Phase 1")
        self._count = 0

        # TODO(2): 创建 QLabel 显示计数，创建 QPushButton 触发点击
        ???

        # TODO(3): 用 QVBoxLayout 把 label 和 button 放进去
        ???

        # TODO(4): 把按钮 clicked 信号连接到 _on_click
        ???

        # TODO(5): 把自定义信号 count_updated 连接到 _on_count_updated
        ???

    def _on_click(self):
        # TODO(6): _count 自增 1，然后 emit count_updated 信号
        ???

    def _on_count_updated(self, value: int):
        # TODO(7): 更新 label 的文本为收到的 value（注意类型转换）
        ???


def main():
    app = QApplication(sys.argv)
    w = SignalDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()