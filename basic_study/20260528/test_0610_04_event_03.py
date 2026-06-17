"""
事件系统 阶段③：自定义事件
- QEvent 子类化，定义自己的事件类型
- QApplication.postEvent() 异步投递事件
- QApplication.sendEvent() 同步发送事件
- postEvent vs sendEvent 的区别
- 自定义事件的实际应用场景
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QEvent, QObject


# TODO(1): 定义一个自定义事件类 TaskFinishedEvent
#   继承 QEvent
#   使用 QEvent.registerEventType() 注册一个新的事件类型 ID
#   在 __init__ 中接收参数：task_name(str) 和 result(str)
#   提供属性方法访问 task_name 和 result
#   思考：为什么要用 registerEventType() 而不是随便写一个数字？
class TaskFinishedEvent(QEvent):
    Type = QEvent.registerEventType()

    def __init__(self, task_name: str, result: str):
        super().__init__(QEvent.Type(self.Type))
        self._task_name = task_name
        self._result = result

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def result(self) -> str:
        return self._result


# TODO(2): 定义第二个自定义事件类 ProgressEvent
#   继承 QEvent
#   注册新的事件类型 ID
#   在 __init__ 中接收参数：task_name(str) 和 percent(int, 0-100)
#   提供属性方法访问 task_name 和 percent
class ProgressEvent(QEvent):
    Type = QEvent.registerEventType()

    def __init__(self, task_name: str, percent: int):
        super().__init__(QEvent.Type(self.Type))
        self._task_name = task_name
        self._percent = percent

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def percent(self) -> int:
        return self._percent


class CustomEventDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Practice - Phase 3: Custom Events")
        self.setObjectName("custom_event_demo")
        self.setMinimumSize(400, 300)

        # TODO(3): 创建一个 QLabel 用于显示收到的事件信息
        #   objectName 设为 "event_display"，初始文本为 "等待自定义事件..."
        self._event_display = QLabel("等待自定义事件...", objectName="event_display")

        # TODO(4): 创建一个按钮 "发送 postEvent（异步）"
        #   objectName 设为 "btn_post"
        #   点击时调用 self._send_post_event
        self._btn_post = QPushButton("发送 postEvent（异步）", objectName="btn_post")
        self._btn_post.clicked.connect(self._send_post_event)

        # TODO(5): 创建一个按钮 "发送 sendEvent（同步）"
        #   objectName 设为 "btn_send"
        #   点击时调用 self._send_sync_event
        self._btn_send = QPushButton("发送 sendEvent（同步）", objectName="btn_send")
        self._btn_send.clicked.connect(self._send_sync_event)

        # TODO(6): 创建一个按钮 "模拟进度事件"
        #   objectName 设为 "btn_progress"
        #   点击时调用 self._send_progress_events
        self._btn_progress = QPushButton("模拟进度事件", objectName="btn_progress")
        self._btn_progress.clicked.connect(self._send_progress_events)

        # TODO(7): 布局
        layout = QVBoxLayout()
        layout.addWidget(self._event_display)
        layout.addWidget(self._btn_post)
        layout.addWidget(self._btn_send)
        layout.addWidget(self._btn_progress)
        self.setLayout(layout)

    def _send_post_event(self):
        # TODO(8): 使用 QApplication.postEvent() 异步投递自定义事件
        #   创建一个 TaskFinishedEvent，task_name="数据下载", result="成功，共1024字节"
        #   投递给 self
        #   投递后立即打印 "postEvent 已投递（异步，稍后处理）"
        #   思考：postEvent 之后事件什么时候被处理？
        #         事件的所有权交给了谁？（提示：投递后不能再访问 event 对象）
        event = TaskFinishedEvent("数据下载", "成功，共1024字节")
        QApplication.postEvent(self, event)
        print("postEvent 已投递（异步，稍后处理）")

    def _send_sync_event(self):
        # TODO(9): 使用 QApplication.sendEvent() 同步发送自定义事件
        #   创建一个 TaskFinishedEvent，task_name="配置解析", result="读取了15个参数"
        #   发送给 self
        #   发送后立即打印 "sendEvent 已返回（同步，已处理完毕）"
        #   思考：sendEvent 和 postEvent 的执行时机有什么区别？
        #         sendEvent 的事件对象在栈上还是堆上？谁负责释放？
        event = TaskFinishedEvent("配置解析", "读取了15个参数")
        QApplication.sendEvent(self, event)
        print("sendEvent 已返回（同步，已处理完毕）")

    def _send_progress_events(self):
        # TODO(10): 投递多个 ProgressEvent 模拟进度
        #   用循环投递 percent = 0, 25, 50, 75, 100
        #   每个都用 postEvent 投递给 self
        #   投递完毕后打印 "5个进度事件已全部投递"
        #   思考：这 5 个事件会在本方法返回后才被处理吗？为什么？
        for percent in (0, 25, 50, 75, 100):
            event = ProgressEvent("固件烧录", percent)
            QApplication.postEvent(self, event)
        print("5个进度事件已全部投递")

    def event(self, event: QEvent) -> bool:
        # TODO(11): 重写 event() 接收自定义事件
        #   如果事件类型是 TaskFinishedEvent 的类型：
        #     打印 f"[收到] 任务完成: {event.task_name} -> {event.result}"
        #     更新 event_display 文本
        #     return True
        #
        #   如果事件类型是 ProgressEvent 的类型：
        #     打印 f"[进度] {event.task_name}: {event.percent}%"
        #     更新 event_display 文本为 f"进度: {event.task_name} {event.percent}%"
        #     return True
        #
        #   其他事件交给父类处理：return super().event(event)
        #
        #   思考：为什么自定义事件要在 event() 里处理，而不是像 keyPressEvent 那样有专用方法？
        if event.type() == TaskFinishedEvent.Type:
            print(f"[收到] 任务完成: {event.task_name} -> {event.result}")
            self._event_display.setText(f"任务完成: {event.task_name} -> {event.result}")
            return True

        if event.type() == ProgressEvent.Type:
            print(f"[进度] {event.task_name}: {event.percent}%")
            self._event_display.setText(f"进度: {event.task_name} {event.percent}%")
            return True

        return super().event(event)


def main():
    app = QApplication(sys.argv)
    w = CustomEventDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()