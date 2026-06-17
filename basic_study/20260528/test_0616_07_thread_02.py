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
    progress = Signal(int)
    finished = Signal(str)
    log = Signal(str)

    def __init__(self):
        super().__init__()
        self._is_cancelled = False
        self._is_paused = False
        self._mutex = QMutex()

    def do_work(self):
        for i in range(20):
            with QMutexLocker(self._mutex):
                if self._is_cancelled:
                    self.finished.emit("已取消")
                    return

            while True:
                with QMutexLocker(self._mutex):
                    if not self._is_paused:
                        break
                time.sleep(0.05)

            time.sleep(0.2)
            self.progress.emit((i + 1) * 5)
            self.log.emit(f"步骤：{i + 1}")

        self.finished.emit("完成")

    def cancel(self):
        with QMutexLocker(self._mutex):
            self._is_cancelled = True

    def pause(self):
        with QMutexLocker(self._mutex):
            self._is_paused = True

    def resume(self):
        with QMutexLocker(self._mutex):
            self._is_paused = False

    def reset_flags(self):
        with QMutexLocker(self._mutex):
            self._is_cancelled = False
            self._is_paused = False


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
        self._label_status = QLabel("就绪")
        self._progressbar = QProgressBar()
        self._textedit_log = QTextEdit()
        self._textedit_log.setReadOnly(True)
        self._btn_start = QPushButton("开始")
        self._btn_stop_continue = QPushButton("暂停")
        self._btn_cancel = QPushButton("取消")
        self._btn_reset = QPushButton("重置")
        self._btn_start.clicked.connect(self._start_task)
        self._btn_stop_continue.clicked.connect(self._toggle_pause)
        self._btn_cancel.clicked.connect(self._cancel_task)
        self._btn_reset.clicked.connect(self._reset)

        self._btn_stop_continue.setEnabled(False)
        self._btn_cancel.setEnabled(False)

        # TODO(3): 布局
        #   按钮用 QHBoxLayout 水平排列
        #   整体用 QVBoxLayout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._btn_start)
        btn_layout.addWidget(self._btn_stop_continue)
        btn_layout.addWidget(self._btn_cancel)
        btn_layout.addWidget(self._btn_reset)

        layout = QVBoxLayout()
        layout.addWidget(self._label_status)
        layout.addWidget(self._progressbar)
        layout.addWidget(self._textedit_log)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

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
        self._thread = QThread()
        self._worker = CancellableWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.do_work)
        self._worker.progress.connect(self._on_progress)
        self._worker.progress.connect(self._progressbar.setValue)
        self._worker.log.connect(self._on_log)
        self._worker.finished.connect(self._on_finished)
        self._worker.finished.connect(self._thread.quit)

    def _start_task(self):
        # TODO(5): 启动任务
        #   检查线程是否在运行
        #   重置进度条为 0
        #   启动线程
        #   更新按钮状态（禁用开始，启用暂停/取消）
        if self._thread.isRunning():
            return
        self._worker.reset_flags()
        self._progressbar.setValue(0)
        self._thread.start()
        self._btn_start.setEnabled(False)
        self._btn_stop_continue.setEnabled(True)
        self._btn_cancel.setEnabled(True)
        self._btn_stop_continue.setText("暂停")
        self._label_status.setText("运行中...")

    def _toggle_pause(self):
        # TODO(6): 暂停/继续切换
        #   如果当前是暂停状态 → 调用 _worker.resume()，按钮文字改为"暂停"
        #   如果当前是运行状态 → 调用 _worker.pause()，按钮文字改为"继续"
        #
        #   思考：pause() 是在主线程调用的，为什么能影响子线程的行为？
        if not self._thread.isRunning():
            return
        with QMutexLocker(self._worker._mutex):
            is_paused = self._worker._is_paused

        if is_paused:
            self._worker.resume()
            self._btn_stop_continue.setText("暂停")
            self._label_status.setText("运行中...")
        else:
            self._worker.pause()
            self._btn_stop_continue.setText("继续")
            self._label_status.setText("已暂停")

    def _cancel_task(self):
        # TODO(7): 取消任务
        #   调用 _worker.cancel()
        #   更新状态标签
        if not self._thread.isRunning():
            return
        self._worker.cancel()
        self._label_status.setText("取消中...")

    def _on_progress(self, value):
        # TODO(8): 更新进度
        #   更新状态标签显示百分比
        self._label_status.setText(f"进度：{value}%")

    def _on_log(self, msg):
        # TODO(9): 追加日志
        self._textedit_log.append(msg)

    def _on_finished(self, result_msg):
        # TODO(10): 任务结束处理
        #   更新状态标签显示结果
        #   恢复按钮状态
        #   重置 Worker 内部的取消/暂停标志（准备下次使用）
        self._label_status.setText(f"结果：{result_msg}")
        self._btn_start.setEnabled(True)
        self._btn_stop_continue.setEnabled(False)
        self._btn_cancel.setEnabled(False)

    def _reset(self):
        # TODO(11): 重置界面
        #   清空日志、进度条归零、状态标签恢复
        self._textedit_log.clear()
        self._progressbar.setValue(0)
        self._label_status.setText("就绪")

    def closeEvent(self, event):
        # TODO(12): 安全关闭
        #   取消任务 + quit + wait
        if self._thread.isRunning():
            self._worker.cancel()
            self._thread.quit()
            self._thread.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)
    w = ThreadSafetyDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()