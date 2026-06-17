"""
事件系统 阶段①：事件循环与事件处理方法重写
- Qt 事件循环的基本概念
- 常见事件类型：close、key、mouse、resize、paint
- 重写事件处理方法拦截事件
- event() 方法的角色
- accept() / ignore() 控制事件传播
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent, QMouseEvent, QCloseEvent


class EventBasicDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Practice - Phase 1: Event Handling")
        self.setObjectName("event_demo")
        self.setMinimumSize(400, 300)
        self._close_attempted = False

        # TODO(1): 创建一个 QLabel 用于显示事件信息
        #   objectName 设为 "event_log"，初始文本为 "事件信息将显示在这里"
        #   设置 alignment 为居中
        self._label_log = QLabel("事件信息将显示在这里",objectName="event_log")
        self._label_log.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # TODO(2): 创建一个 QLabel 显示按键提示
        #   文本为 "按任意键 / 点击鼠标 / 拖动窗口大小 / 关闭窗口 试试"
        self._label_tips = QLabel("按任意键 / 点击鼠标 / 拖动窗口大小 / 关闭窗口 试试")

        # TODO(3): 布局
        layout = QVBoxLayout()
        layout.addWidget(self._label_log)
        layout.addWidget(self._label_tips)
        self.setLayout(layout)

    def closeEvent(self, event: QCloseEvent):
        # TODO(4): 重写 closeEvent
        #   打印 "closeEvent 触发"
        #   第一次关闭时调用 event.ignore() 拒绝关闭，并更新 event_log 文本为 "关闭被拦截！再点一次才真正关闭"
        #   第二次关闭时调用 event.accept() 允许关闭
        #   思考：accept() 和 ignore() 对事件传播有什么影响？
        #         如果不调用 accept()，窗口会关闭吗？
        print("closeEvent 触发")
        if not self._close_attempted:
            self._close_attempted = True
            self._label_log.setText("关闭被拦截！再点一次才真正关闭")
            event.ignore()
        else:
            event.accept()



    def keyPressEvent(self, event: QKeyEvent):
        # TODO(5): 重写 keyPressEvent
        #   打印按下的键：event.key() 和 event.text()
        #   更新 event_log 显示按键信息，格式：f"按键: {event.text()} (key={event.key()})"
        #   如果按下 Escape 键，调用 self.close()
        #   思考：keyPressEvent 和 keyReleaseEvent 的触发时机分别是什么？
        print(event.key(),event.text())
        self._label_log.setText(f"按键： {event.text()} (key = {event.key()})")

    def mousePressEvent(self, event: QMouseEvent):
        # TODO(6): 重写 mousePressEvent
        #   打印鼠标点击位置：event.position() 和按钮：event.button()
        #   更新 event_log 显示点击信息
        #   格式：f"鼠标点击: ({x}, {y}) 按钮={button}"
        #   思考：position() 和 globalPosition() 的区别是什么？
        pos = event.position()
        x, y = pos.x(), pos.y()
        button = event.button()
        print(f"mousePressEvent: ({x}, {y}) button={button}")
        self._label_log.setText(f"鼠标点击: ({x:.0f}, {y:.0f}) 按钮={button}")

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # TODO(7): 重写 mouseDoubleClickEvent
        #   更新 event_log 显示 "鼠标双击！"
        #   思考：双击事件的触发顺序是什么？
        #         （提示：press → release → double_click → release）
        print("mouseDoubleClickEvent 触发")
        self._label_log.setText("鼠标双击！")

    def resizeEvent(self, event):
        # TODO(8): 重写 resizeEvent
        #   打印旧尺寸 event.oldSize() 和新尺寸 event.size()
        #   更新 event_log 显示尺寸变化
        #   格式：f"窗口大小: {w}x{h} (原来: {old_w}x{old_h})"
        #   思考：resizeEvent 在窗口第一次 show() 时会触发吗？
        old = event.oldSize()
        new = event.size()
        print(f"resizeEvent: {new.width()}x{new.height()} (was {old.width()}x{old.height()})")
        self._label_log.setText(
            f"窗口大小: {new.width()}x{new.height()} (原来: {old.width()}x{old.height()})"
        )

    def event(self, event: QEvent):
        # TODO(9): 重写 event() 方法
        #   在所有事件到达具体 handler 之前，先在这里打印事件类型
        #   打印格式：f"[event] type={event.type()}"
        #   但只打印以下几种类型，避免刷屏：
        #     QEvent.Type.KeyPress, QEvent.Type.MouseButtonPress,
        #     QEvent.Type.Close, QEvent.Type.Resize
        #   最后必须调用 super().event(event) 把事件继续分发下去
        #   思考：如果不调用 super().event(event) 会怎样？
        #         event() 和具体的 xxxEvent() 方法之间是什么关系？
        watched_types = (
            QEvent.Type.KeyPress,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.Close,
            QEvent.Type.Resize,
        )
        if event.type() in watched_types:
            print(f"[event] type={event.type()}")
        return super().event(event)


def main():
    app = QApplication(sys.argv)
    w = EventBasicDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()