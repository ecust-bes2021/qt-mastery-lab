"""
多线程 阶段①：QThread 基础 + Worker 模式
- QThread 的正确用法（Worker + moveToThread）
- 为什么不能在子线程直接操作 UI
- 信号跨线程通信
- 线程的启动与结束
"""
import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QTextEdit,
)
from PySide6.QtCore import Qt, QThread, QObject, Signal, Slot


# TODO(1): 创建 Worker 类，继承 QObject
#   这个 Worker 模拟一个耗时任务（比如固件烧录、数据采集）
#
#   定义信号：
#     progress = Signal(int)      — 报告进度（0~100）
#     finished = Signal()         — 任务完成
#     log = Signal(str)           — 输出日志信息
#
#   实现方法：
#     do_work(self) — 模拟耗时操作
#       用 for 循环 + time.sleep(0.3) 模拟 10 步操作
#       每步发射 progress 和 log 信号
#       全部完成后发射 finished 信号
#
#   思考：为什么 Worker 要继承 QObject 而不是 QThread？
#         为什么耗时操作不能直接写在主线程？
class Worker(QObject):
    ???


class ThreadDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thread Practice - Phase 1: Worker + moveToThread")
        self.setObjectName("thread_demo_01")
        self.setMinimumSize(400, 350)

        # TODO(2): 创建 UI 控件
        #   一个 QLabel 显示当前状态（"空闲" / "运行中..." / "完成"）
        #   一个 QTextEdit 显示日志（设为只读）
        #   一个 QPushButton "开始任务"
        #   一个 QPushButton "重置"
        ???

        # TODO(3): 布局
        ???

        # TODO(4): 创建 QThread 和 Worker 实例
        #   self._thread = QThread()
        #   self._worker = Worker()
        #   使用 moveToThread 将 Worker 移动到子线程
        #   连接信号：
        #     _thread.started → _worker.do_work（线程启动时自动执行任务）
        #     _worker.progress → self._on_progress（更新进度显示）
        #     _worker.log → self._on_log（追加日志）
        #     _worker.finished → self._on_finished（任务完成处理）
        #     _worker.finished → _thread.quit（任务完成后停止线程）
        #
        #   思考：为什么用 moveToThread 而不是继承 QThread？
        #         started 信号连接 do_work 后，do_work 在哪个线程执行？
        ???

    def _start_task(self):
        # TODO(5): 启动任务
        #   检查线程是否已在运行（isRunning()）
        #   如果没在运行，启动线程：self._thread.start()
        #   更新状态标签为 "运行中..."
        #   禁用开始按钮
        ???

    def _on_progress(self, value):
        # TODO(6): 更新进度显示
        #   更新状态标签显示百分比
        ???

    def _on_log(self, msg):
        # TODO(7): 追加日志到 QTextEdit
        ???

    def _on_finished(self):
        # TODO(8): 任务完成后的处理
        #   更新状态标签为 "完成"
        #   重新启用开始按钮
        ???

    def _reset(self):
        # TODO(9): 重置界面
        #   清空日志
        #   状态标签恢复为 "空闲"
        ???

    def closeEvent(self, event):
        # TODO(10): 窗口关闭时安全停止线程
        #   如果线程正在运行：
        #     调用 _thread.quit()
        #     调用 _thread.wait()（等待线程真正结束）
        #   然后 accept 事件
        #
        #   思考：如果不 wait() 直接关闭会怎样？
        ???


def main():
    app = QApplication(sys.argv)
    w = ThreadDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()