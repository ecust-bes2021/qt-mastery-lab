"""
阶段⑤：disconnect 与 ConnectionType
- disconnect()：动态断开信号与槽的连接
- Qt.ConnectionType：DirectConnection / QueuedConnection / AutoConnection
- 理解连接类型对执行时机和线程安全的影响
"""
import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Signal, Qt, QThread, QObject


# ========== Part A: disconnect ==========

class DisconnectDemo(QWidget):

    notify = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Practice - Phase 5A: Disconnect")

        # TODO(1): 创建控件
        #   - btn_send: "发送信号" 按钮
        #   - btn_connect: "连接" 按钮
        #   - btn_disconnect: "断开" 按钮
        #   - label: 显示接收到的信号内容
        self._btn_send = QPushButton("发送信号")
        self._btn_connect = QPushButton("连接")
        self._btn_disconnect = QPushButton("断开")
        self._label = QLabel()


        # TODO(2): 布局
        layout = QVBoxLayout()
        layout.addWidget(self._btn_send)
        layout.addWidget(self._btn_connect)
        layout.addWidget(self._btn_disconnect)
        layout.addWidget(self._label)
        self.setLayout(layout)

        # TODO(3): 连接按钮 clicked
        #   - btn_send -> _emit_notify
        #   - btn_connect -> _do_connect
        #   - btn_disconnect -> _do_disconnect
        self._btn_send.clicked.connect(self._emit_notify)
        self._btn_connect.clicked.connect(self._do_connect)
        self._btn_disconnect.clicked.connect(self._do_disconnect)

        # TODO(4): 初始连接 notify -> _on_notify
        self.notify.connect(self._on_notify)

    def _emit_notify(self):
        # TODO(5): emit notify 信号，携带 "Hello!"
        self.notify.emit("Hello!")

    def _on_notify(self, msg: str):
        # TODO(6): 更新 label 显示收到的消息
        self._label.setText(msg)

    def _do_disconnect(self):
        # TODO(7): 断开 notify 信号与 _on_notify 的连接
        #   思考：如果已经断开了，再次 disconnect 会怎样？
        #   提示：用 try/except RuntimeError 保护
        self.notify.disconnect(self._on_notify)
        # try:
        #     self.notify.disconnect(self._on_notify)
        # except RuntimeError:
        #     print("重复断开")


    def _do_connect(self):
        # TODO(8): 重新连接 notify -> _on_notify
        #   思考：如果重复 connect 两次，emit 时槽会被调用几次？
        self.notify.connect(self._on_notify)


# ========== Part B: ConnectionType ==========

class Worker(QObject):

    work_done = Signal(str)

    def do_work(self):
        # TODO(9): 模拟耗时操作（sleep 1秒），然后 emit work_done
        #   注意：这个方法会在子线程中被调用
        time.sleep(5)
        self.work_done.emit("已完成！")


class ConnectionTypeDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Practice - Phase 5B: ConnectionType")

        # TODO(10): 创建控件
        #   - btn_start: "开始工作" 按钮
        #   - label_status: 显示状态
        #   - label_thread: 显示线程信息（用于验证跨线程行为）
        self._btn_start = QPushButton("开始工作")
        self._label_status = QLabel()
        self._label_thread = QLabel()

        # TODO(11): 布局
        layout = QVBoxLayout()
        layout.addWidget(self._btn_start)
        layout.addWidget(self._label_status)
        layout.addWidget(self._label_thread)
        self.setLayout(layout)

        # TODO(12): 创建 QThread 和 Worker
        #   - 创建 QThread 实例
        #   - 创建 Worker 实例
        #   - 把 worker moveToThread 到子线程
        #   思考：moveToThread 之后，worker 的槽函数在哪个线程执行？
        self._thread = QThread()
        self._worker = Worker()
        self._worker.moveToThread(self._thread)

        # TODO(13): 连接信号
        #   - btn_start.clicked -> worker.do_work
        #     注意：这里有个陷阱！clicked 在主线程 emit，
        #     如果用 DirectConnection，do_work 会在主线程执行（阻塞 UI）
        #     如果用 AutoConnection（默认），因为 worker 在子线程，会用 QueuedConnection
        #   - worker.work_done -> _on_work_done
        #   - thread.started 可选连接（用于调试）
        self._btn_start.clicked.connect(self._worker.do_work)
        self._worker.work_done.connect(self._on_work_done)

        # TODO(14): 启动线程
        self._thread.start()

    def _on_work_done(self, result: str):
        # TODO(15): 更新 label_status 显示结果
        #   同时显示当前是在哪个线程收到的（验证 QueuedConnection 回到了主线程）
        #   提示：QThread.currentThread().objectName() 或 id
        self._label_status.setText(f"{QThread.currentThread().objectName()}: {result}")

    def closeEvent(self, event):
        # TODO(16): 窗口关闭时安全退出线程
        #   - 调用 thread.quit()
        #   - 调用 thread.wait()
        self._thread.quit()
        self._thread.wait()


def main():
    app = QApplication(sys.argv)

    w1 = DisconnectDemo()
    w1.show()

    w2 = ConnectionTypeDemo()
    w2.move(500, 100)
    w2.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()