"""
多线程 阶段②：线程安全与进度反馈
- QMutex 保护共享数据
- 取消/暂停正在运行的任务
- QProgressBar 进度条更新
- 多个 Worker 并发运行
"""
import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QProgressBar,
)
from PySide6.QtCore import Qt, QThread, QObject, Signal, Slot, QMutex, QMutexLocker


# TODO(1): 创建 CancellableWorker 类，继承 QObject
#   模拟一个可取消、可暂停的耗时任务
#
#   定义信号：
#     progress = Signal(int)      — 报告进度（0~100）
#     finished = Signal(str)      — 任务完成，带结果消息（"完成" 或 "已取消"）
#     log = Signal(str)           — 输出日志
#
#   内部状态（需要用 QMutex 保护）：
#     _is_cancelled = False       — 是否被请求取消
#     _is_paused = False          — 是否被请求暂停
#     _mutex = QMutex()           — 互斥锁
#
#   实现方法：
#     do_work(self) — 耗时操作（20步，每步 sleep 0.2s）
#       每步检查 _is_cancelled，如果为 True 则提前退出
#       每步检查 _is_paused，如果为 True 则循环等待直到恢复
#       每步发射 progress 和 log
#
#     cancel(self) — 外部调用，设置 _is_cancelled = True
#     pause(self)  — 外部调用，设置 _is_paused = True
#     resume(self) — 外部调用，设置 _is_paused = False
#
#   思考：为什么修改 _is_cancelled 需要加锁？
#         如果不加锁，最坏情况下会发生什么？
#         cancel() 和 do_work() 分别在哪个线程执行？
class CancellableWorker(QObject):
    ???


class ThreadSafetyDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thread Practice - Phase 2: Safety & Progress")
        self.setObjectName("thread_demo_02")
        self.setMinimumSize(450, 400)

        # TODO(2): 创建 UI 控件
        #   一个 QLabel 显示当前状态
        #   一个 QProgressBar 显示进度
        #   一个 QTextEdit 显示日志（只读）
        #   按钮："开始"、"暂停/继续"、"取消"、"重置"
        ???

        # TODO(3): 布局
        #   按钮用 QHBoxLayout 水平排列
        #   整体用 QVBoxLayout
        ???

        # TODO(4): 创建线程和 Worker
        #   创建 QThread 和 CancellableWorker
        #   moveToThread
        #   连接信号：
        #     _thread.started → _worker.do_work
        #     _worker.progress → self._on_progress
        #     _worker.progress → _progress_bar.setValue
        #     _worker.log → self._on_log
        #     _worker.finished → self._on_finished
        #     _worker.finished → _thread.quit
        ???

    def _start_task(self):
        # TODO(5): 启动任务
        #   检查线程是否在运行
        #   重置进度条为 0
        #   启动线程
        #   更新按钮状态（禁用开始，启用暂停/取消）
        ???

    def _toggle_pause(self):
        # TODO(6): 暂停/继续切换
        #   如果当前是暂停状态 → 调用 _worker.resume()，按钮文字改为"暂停"
        #   如果当前是运行状态 → 调用 _worker.pause()，按钮文字改为"继续"
        #
        #   思考：pause() 是在主线程调用的，为什么能影响子线程的行为？
        ???

    def _cancel_task(self):
        # TODO(7): 取消任务
        #   调用 _worker.cancel()
        #   更新状态标签
        ???

    def _on_progress(self, value):
        # TODO(8): 更新进度
        #   更新状态标签显示百分比
        ???

    def _on_log(self, msg):
        # TODO(9): 追加日志
        ???

    def _on_finished(self, result_msg):
        # TODO(10): 任务结束处理
        #   更新状态标签显示结果
        #   恢复按钮状态
        #   重置 Worker 内部的取消/暂停标志（准备下次使用）
        ???

    def _reset(self):
        # TODO(11): 重置界面
        #   清空日志、进度条归零、状态标签恢复
        ???

    def closeEvent(self, event):
        # TODO(12): 安全关闭
        #   取消任务 + quit + wait
        ???


def main():
    app = QApplication(sys.argv)
    w = ThreadSafetyDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()