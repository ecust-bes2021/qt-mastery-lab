"""
多线程 阶段③：实战 — 模拟串口持续读取 + UI 实时刷新
- 后台线程持续产生数据（模拟串口/传感器读取）
- UI 线程实时显示最新数据
- 优雅启动和停止后台线程
- 数据缓冲与批量更新
"""
import sys
import time
import random
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt, QThread, QObject, Signal, Slot, QMutex, QTimer, QMutexLocker


# TODO(1): 创建 SerialReader 类，继承 QObject
#   模拟串口持续读取传感器数据
#
#   定义信号：
#     data_received = Signal(dict)  — 收到一组数据
#       数据格式：{"timestamp": float, "temp": float, "humidity": float, "pressure": float}
#     error = Signal(str)           — 发生错误
#     connected = Signal()          — 连接成功
#     disconnected = Signal()       — 断开连接
#
#   内部状态：
#     _running = False              — 是否持续运行
#     _mutex = QMutex()
#     _interval = 0.5               — 采样间隔（秒）
#
#   实现方法：
#     start_reading(self) — 开始持续读取
#       发射 connected 信号
#       循环：while _running:
#         生成随机传感器数据（温度 20~35，湿度 40~80，气压 99~103）
#         发射 data_received 信号
#         time.sleep(_interval)
#       循环结束后发射 disconnected 信号
#
#     stop_reading(self) — 停止读取（设 _running = False）
#
#   思考：为什么用 while 循环而不是 QTimer？
#         这种"持续运行"的 Worker 和 Phase 1 的"一次性任务"有什么区别？
#         stop_reading 在主线程调，_running 在子线程读，需要锁吗？
class SerialReader(QObject):
    data_received = Signal(dict)
    error = Signal(str)
    connected = Signal()
    disconnected = Signal()
    def __init__(self):
        super().__init__()
        self._running = False
        self._mutex = QMutex()
        self._interval = 0.5
    
    def start_reading(self):
        self.connected.emit()
        while self._running:
            
            self.data_received.emit()
            time.sleep(self._interval)
        self.disconnected.emit()
    
    def stop_reading(self):
        with QMutexLocker(self._mutex):
            self._running = False



class SerialMonitorDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thread Practice - Phase 3: Serial Monitor Simulation")
        self.setObjectName("thread_demo_03")
        self.setMinimumSize(550, 450)

        # TODO(2): 创建 UI 控件
        #   一个 QLabel 显示连接状态（"未连接" / "已连接 - 读取中" / "已断开"）
        #   一个 QTableWidget 显示最近 N 条数据（4列：时间、温度、湿度、气压）
        #     设置列标题
        #     设置列宽自适应
        #     设为不可编辑
        #   一个 QTextEdit 显示事件日志（只读）
        #   按钮："连接"、"断开"、"清空数据"
        self._label = QLabel("未连接")
        self._tableWidget = QTableWidget()
        self._tableWidget.setColumnCount(4)
        self._tableWidget.setHorizontalHeaderLabels(["时间","温度","湿度","气压"])
        header = self._tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self._tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self._textEdit = QTextEdit()
        self._textEdit.setReadOnly(True)

        # TODO(3): 布局
        ???

        # TODO(4): 创建线程和 SerialReader
        #   创建 QThread 和 SerialReader
        #   moveToThread
        #   连接信号：
        #     _thread.started → _reader.start_reading
        #     _reader.data_received → self._on_data_received
        #     _reader.connected → self._on_connected
        #     _reader.disconnected → self._on_disconnected
        #     _reader.disconnected → _thread.quit
        #     _reader.error → self._on_error
        ???

        # TODO(5): 创建一个 QTimer 用于限制 UI 刷新频率（可选）
        #   如果数据来得太快，每条都刷新 UI 会卡
        #   可以用 Timer 做批量刷新：每 200ms 把缓冲区的数据一次性更新到表格
        #   self._data_buffer = []
        #   self._refresh_timer = QTimer()
        #   self._refresh_timer.timeout.connect(self._flush_buffer)
        #   self._refresh_timer.start(200)
        #
        #   思考：为什么高频数据不能每条都直接更新 UI？
        #         QTimer 在哪个线程运行？
        ???

    def _connect_serial(self):
        # TODO(6): 连接（启动线程）
        #   检查线程是否已运行
        #   启动线程
        #   更新按钮状态
        ???

    def _disconnect_serial(self):
        # TODO(7): 断开（停止读取）
        #   调用 _reader.stop_reading()
        #   注意：不要直接 _thread.quit()，等 Worker 循环自己退出后触发 disconnected → quit
        #
        #   思考：为什么不能直接 terminate() 线程？
        ???

    def _on_data_received(self, data):
        # TODO(8): 收到数据
        #   方式A（简单）：直接更新表格，在末尾插入一行
        #     如果行数超过 100，删除最早的行
        #   方式B（高性能）：放入缓冲区，等 Timer flush
        #
        #   表格插入一行：
        #     row = self._table.rowCount()
        #     self._table.insertRow(row)
        #     self._table.setItem(row, 0, QTableWidgetItem(str(data["timestamp"])))
        #     ...
        ???

    def _on_connected(self):
        # TODO(9): 连接成功回调
        #   更新状态标签
        #   追加日志
        ???

    def _on_disconnected(self):
        # TODO(10): 断开连接回调
        #   更新状态标签
        #   追加日志
        #   恢复按钮状态
        ???

    def _on_error(self, msg):
        # TODO(11): 错误处理
        #   追加日志
        #   可选：自动断开
        ???

    def _clear_data(self):
        # TODO(12): 清空表格数据
        #   清空 QTableWidget：setRowCount(0)
        ???

    def closeEvent(self, event):
        # TODO(13): 安全关闭
        #   如果线程在运行：stop_reading → quit → wait
        #   停止 refresh timer
        ???


def main():
    app = QApplication(sys.argv)
    w = SerialMonitorDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()