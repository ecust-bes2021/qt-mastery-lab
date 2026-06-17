"""
阶段②：信号携带不同类型/数量的参数
- Signal() 无参数信号
- Signal(int) 单参数信号
- Signal(str, int) 多参数信号
- 不同签名的信号需要连接到匹配的槽函数
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
)
from PySide6.QtCore import Signal


class SignalParamsDemo(QWidget):

    # TODO(1): 定义三个自定义信号：
    #   - no_arg_signal: 无参数信号
    #   - int_signal: 携带一个 int
    #   - multi_signal: 携带一个 str 和一个 int
    no_arg_signal = Signal()
    int_signal = Signal(int)
    multi_signal = Signal(str,int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Practice - Phase 2: Different Parameters")
        self._click_count = 0

        # TODO(2): 创建三个按钮和一个 QLabel 用于显示结果
        #   - btn_no_arg: "发射无参信号"
        #   - btn_int: "发射int信号"
        #   - btn_multi: "发射多参信号"
        #   - 一个 QLineEdit 用于输入文本（给 multi_signal 用）
        #   - 一个 QLabel 用于显示收到的信号信息
        self._btn_no_arg = QPushButton("发射无参信号")
        self._btn_int = QPushButton("发射int信号")
        self._btn_multi = QPushButton("发射多参信号")
        self._lineEdit = QLineEdit()
        self._label = QLabel()

        # TODO(3): 布局 - 用 QVBoxLayout 把所有控件放进去
        layout = QVBoxLayout()
        layout.addWidget(self._btn_no_arg)
        layout.addWidget(self._btn_int)
        layout.addWidget(self._btn_multi)
        layout.addWidget(self._lineEdit)
        layout.addWidget(self._label)
        self.setLayout(layout)

        # TODO(4): 连接三个按钮的 clicked 到各自的发射方法
        self._btn_int.clicked.connect(self._emit_int)
        self._btn_no_arg.clicked.connect(self._emit_no_arg)
        self._btn_multi.clicked.connect(self._emit_multi)

        # TODO(5): 连接三个自定义信号到各自的槽函数
        #   提示：无参信号连接的槽不带额外参数
        #         int信号连接的槽带一个 int
        #         multi信号连接的槽带 str 和 int
        #   问题：能不能让三个不同签名的信号连接到同一个槽函数？想想怎么处理。
        self.no_arg_signal.connect(self._on_no_arg)
        self.int_signal.connect(self._on_int)
        self.multi_signal.connect(self._on_multi)

    def _emit_no_arg(self):
        # TODO(6): 发射无参信号
        self.no_arg_signal.emit()

    def _emit_int(self):
        # TODO(7): _click_count 自增，然后发射 int_signal
        self._click_count+=1
        self.int_signal.emit(self._click_count)

    def _emit_multi(self):
        # TODO(8): 从 QLineEdit 获取文本，连同 _click_count 一起发射 multi_signal
        line_str = self._lineEdit.text()
        self.multi_signal.emit(line_str, self._click_count)

    def _on_no_arg(self):
        # TODO(9): 收到无参信号，更新 label 显示 "收到无参信号"
        self._label.setText("收到无参信号")

    def _on_int(self, value: int):
        # TODO(10): 收到 int 信号，更新 label 显示收到的数值
        self._label.setText(str(value))

    def _on_multi(self, text: str, count: int):
        # TODO(11): 收到多参信号，更新 label 显示文本和数值
        
        self._label.setText(f"{text} : {count}")


def main():
    app = QApplication(sys.argv)
    w = SignalParamsDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()