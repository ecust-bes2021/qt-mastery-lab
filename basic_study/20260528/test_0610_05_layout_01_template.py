"""
布局系统 阶段①：基础布局
- QVBoxLayout 垂直布局
- QHBoxLayout 水平布局
- QGridLayout 网格布局
- 布局嵌套
- addWidget / addLayout 的用法
- 边距（margins）和间距（spacing）
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)
from PySide6.QtCore import Qt


class LayoutBasicDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout Practice - Phase 1: Basic Layouts")
        self.setObjectName("layout_demo")
        self.setMinimumSize(500, 400)

        # ========== 区域1：垂直布局 ==========

        # TODO(1): 创建一个 QVBoxLayout
        #   添加 3 个 QLabel：  "垂直-1"  "垂直-2"  "垂直-3"
        #   给每个 label 设置居中对齐和边框样式（方便观察）
        #   样式：setStyleSheet("border: 1px solid blue; padding: 5px;")
        ???

        # ========== 区域2：水平布局 ==========

        # TODO(2): 创建一个 QHBoxLayout
        #   添加 3 个 QPushButton：  "按钮A"  "按钮B"  "按钮C"
        ???

        # ========== 区域3：网格布局 ==========

        # TODO(3): 创建一个 QGridLayout
        #   按照 2行 x 3列 布局 6 个 QLabel：
        #     (0,0)="格0,0"  (0,1)="格0,1"  (0,2)="格0,2"
        #     (1,0)="格1,0"  (1,1)="格1,1"  (1,2)="格1,2"
        #   给每个 label 设置边框样式和居中对齐
        #   思考：addWidget(widget, row, col) 的 row 和 col 从几开始？
        ???

        # ========== 区域4：嵌套布局 ==========

        # TODO(4): 创建一个模拟"登录表单"的嵌套布局
        #   整体是 QVBoxLayout
        #   第一行：QHBoxLayout 包含 QLabel("用户名") + QLineEdit
        #   第二行：QHBoxLayout 包含 QLabel("密码") + QLineEdit
        #   第三行：QHBoxLayout 包含 QPushButton("登录") + QPushButton("取消")
        #   思考：addLayout() 和 addWidget() 有什么区别？
        ???

        # ========== 主布局 ==========

        # TODO(5): 创建一个主 QVBoxLayout 把上面 4 个区域组合起来
        #   每个区域之间用 QLabel 作为标题分隔，如 "=== 垂直布局 ==="
        #   设置主布局的边距 setContentsMargins(10, 10, 10, 10)
        #   设置主布局的间距 setSpacing(8)
        #   思考：margins 和 spacing 分别控制什么？
        ???


def main():
    app = QApplication(sys.argv)
    w = LayoutBasicDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()