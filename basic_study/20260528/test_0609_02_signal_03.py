"""
阶段③：多种连接方式
- 一个信号连接多个槽（一对多）
- 多个信号连接同一个槽（多对一）
- 信号连接信号（信号转发）
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Signal


class SignalConnectionDemo(QWidget):

    # TODO(1): 定义两个自定义信号：
    #   - action_signal: 携带一个 str（描述动作）
    #   - forward_signal: 携带一个 str（用于演示信号连信号）
    action_signal = Signal(str)
    forward_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Practice - Phase 3: Connection Patterns")

        # TODO(2): 创建控件
        #   - btn_action: "执行动作" 按钮
        #   - btn_a: "信号A" 按钮
        #   - btn_b: "信号B" 按钮
        #   - label_1: 第一个显示标签
        #   - label_2: 第二个显示标签
        #   - label_forward: 显示转发信号结果的标签
        self.btn_action = QPushButton("执行动作")
        self._btn_a = QPushButton("信号A")
        self._btn_b = QPushButton("信号B")
        self.label_1 = QLabel()
        self.label_2 = QLabel()
        self.label_forward = QLabel()

        # TODO(3): 布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_action)
        layout.addWidget(self._btn_a)
        layout.addWidget(self._btn_b)
        layout.addWidget(self.label_1)
        layout.addWidget(self.label_2)
        layout.addWidget(self.label_forward)
        self.setLayout(layout)

        # ========== 一信号连多槽 ==========
        # TODO(4): 把 action_signal 同时连接到 _on_action_slot1 和 _on_action_slot2
        #   思考：两个槽的执行顺序是怎样的？
        self.action_signal.connect(self._on_action_slot1)
        self.action_signal.connect(self._on_action_slot2)

        # TODO(5): 把 btn_action 的 clicked 连接到 _emit_action
        self.btn_action.clicked.connect(self._emit_action)

        # ========== 多信号连一槽 ==========
        # TODO(6): 把 btn_a 和 btn_b 的 clicked 都连接到同一个槽 _on_any_button_clicked
        #   思考：在槽函数里能知道是哪个按钮触发的吗？
        self._btn_a.clicked.connect(self._on_any_button_clicked)
        self._btn_b.clicked.connect(self._on_any_button_clicked)

        # ========== 信号连信号 ==========
        # TODO(7): 把 action_signal 连接到 forward_signal（信号转发信号）
        #   然后把 forward_signal 连接到 _on_forwarded
        self.action_signal.connect(self.forward_signal)
        self.forward_signal.connect(self._on_forwarded)

    def _emit_action(self):
        # TODO(8): 发射 action_signal，携带字符串 "Action!"
        self.action_signal.emit("Action!")

    def _on_action_slot1(self, msg: str):
        # TODO(9): 更新 label_1，显示 "槽1收到: " + msg
        self.label_1.setText(f"槽1收到：{msg}")

    def _on_action_slot2(self, msg: str):
        # TODO(10): 更新 label_2，显示 "槽2收到: " + msg
        self.label_2.setText(f"槽2收到：{msg}")

    def _on_any_button_clicked(self):
        # TODO(11): 更新 label_1，显示 "某个按钮被点击了"
        #   进阶思考：如何区分是哪个按钮？（提示：self.sender()）
        btn = self.sender()
        self.label_1.setText(f"{btn.text()} 按钮被点击了")

    def _on_forwarded(self, msg: str):
        # TODO(12): 更新 label_forward，显示 "转发收到: " + msg
        self.label_forward.setText(f"转发收到：{msg}")


def main():
    app = QApplication(sys.argv)
    w = SignalConnectionDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()