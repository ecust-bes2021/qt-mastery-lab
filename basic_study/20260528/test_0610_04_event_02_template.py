"""
事件系统 阶段②：事件过滤器（Event Filter）
- installEventFilter() 安装事件过滤器
- eventFilter() 拦截其他对象的事件
- 事件过滤器 vs 重写事件方法的区别
- 多个过滤器的优先级
- 过滤器的典型应用场景
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, QEvent, QObject
from PySide6.QtGui import QKeyEvent, QMouseEvent


class EventFilterDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Practice - Phase 2: Event Filter")
        self.setObjectName("filter_demo")
        self.setMinimumSize(400, 300)

        # TODO(1): 创建一个 QLineEdit 作为输入框
        #   objectName 设为 "input_box"
        #   placeholder 设为 "在这里输入（数字键会被过滤掉）"
        ???

        # TODO(2): 创建一个 QLabel 用于显示过滤日志
        #   objectName 设为 "filter_log"，初始文本为 "过滤器日志"
        ???

        # TODO(3): 创建一个 QPushButton "悬停检测按钮"
        #   objectName 设为 "hover_btn"
        #   这个按钮我们将用事件过滤器监控它的鼠标进入/离开事件
        ???

        # TODO(4): 创建一个 QLabel 显示悬停状态
        #   objectName 设为 "hover_status"，初始文本为 "鼠标未悬停在按钮上"
        ???

        # TODO(5): 布局
        ???

        # TODO(6): 给 input_box 安装事件过滤器（self 作为过滤器）
        #   self 会收到 input_box 的所有事件
        #   思考：为什么用事件过滤器而不是子类化 QLineEdit 重写 keyPressEvent？
        ???

        # TODO(7): 给 hover_btn 也安装事件过滤器（self 作为过滤器）
        ???

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # TODO(8): 实现事件过滤器
        #   这个方法会收到所有安装了过滤器的对象的事件
        #   参数 watched 是事件的目标对象，event 是事件本身
        #
        #   规则1：如果 watched 是 input_box 且事件是 KeyPress：
        #     - 检查按键是否是数字键（0-9）
        #     - 如果是数字键，拦截它（return True），并更新 filter_log 显示
        #       f"[过滤] 数字键 '{key_text}' 被拦截"
        #     - 如果不是数字键，放行（让事件继续传递）
        #
        #   规则2：如果 watched 是 hover_btn：
        #     - 如果事件类型是 QEvent.Type.Enter，更新 hover_status 为 "鼠标进入按钮！"
        #     - 如果事件类型是 QEvent.Type.Leave，更新 hover_status 为 "鼠标离开按钮"
        #     - 不拦截这些事件（return False），让按钮正常工作
        #
        #   其他情况：调用 super().eventFilter(watched, event)
        #
        #   思考：return True 和 return False 的区别是什么？
        #         True = 事件被吃掉，目标对象收不到
        #         False = 事件继续传递给目标对象
        ???


def main():
    app = QApplication(sys.argv)
    w = EventFilterDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()