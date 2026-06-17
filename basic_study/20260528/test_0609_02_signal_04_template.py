"""
阶段④：内置信号 vs 自定义信号（模板）
- 内置信号：Qt 控件预定义的信号，由控件自身在特定时机自动 emit
- 自定义信号：你在自己的类里定义，由你决定什么时候 emit
- 理解"谁定义、谁发射、什么时机发射"的区别
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QSlider,
    QVBoxLayout,
)
from PySide6.QtCore import Signal, Qt


class BuiltinVsCustomDemo(QWidget):

    # TODO(1): 定义一个自定义信号 threshold_reached，携带一个 int
    #   用途：当 slider 值超过阈值时，由你手动 emit
    ???

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Practice - Phase 4: Builtin vs Custom")
        self._threshold = 80

        # TODO(2): 创建控件
        #   - QSlider(水平方向)，范围 0~100
        #   - QLabel 显示当前 slider 值
        #   - QLineEdit 用于输入文本
        #   - QLabel 显示文本长度（由内置信号驱动）
        #   - QLabel 显示阈值警告（由自定义信号驱动）
        ???

        # TODO(3): 布局
        ???

        # ========== 内置信号 ==========
        # TODO(4): 连接 QSlider 的内置信号 valueChanged(int) 到 _on_slider_changed
        #   思考：valueChanged 是谁 emit 的？你需要手动 emit 它吗？
        ???

        # TODO(5): 连接 QLineEdit 的内置信号 textChanged(str) 到 _on_text_changed
        #   思考：textChanged 什么时候被 emit？
        ???

        # ========== 自定义信号 ==========
        # TODO(6): 连接 threshold_reached 到 _on_threshold
        ???

    def _on_slider_changed(self, value: int):
        # TODO(7): 更新 slider 值的 label 显示
        #   然后判断：如果 value >= self._threshold，emit threshold_reached
        #   思考：这里体现了内置信号和自定义信号的协作模式
        ???

    def _on_text_changed(self, text: str):
        # TODO(8): 更新文本长度的 label，显示 "长度: X"
        ???

    def _on_threshold(self, value: int):
        # TODO(9): 更新警告 label，显示 "⚠ 超过阈值! 当前: X"
        ???


def main():
    app = QApplication(sys.argv)
    w = BuiltinVsCustomDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()