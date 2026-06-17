"""
布局系统 阶段②：尺寸策略与拉伸
- QSizePolicy 尺寸策略
- stretch 拉伸因子
- setMinimumSize / setMaximumSize / setFixedSize 尺寸约束
- addStretch() 弹簧
- 拖动窗口观察不同策略下控件的缩放行为
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class SizePolicyDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout Practice - Phase 2: Size Policy & Stretch")
        self.setObjectName("size_policy_demo")
        self.setMinimumSize(500, 400)

        # ========== 区域1：stretch 拉伸因子 ==========

        # TODO(1): 创建一个 QHBoxLayout，添加 3 个 QLabel
        #   label_a 文本 "1份"，label_b 文本 "2份"，label_c 文本 "3份"
        #   给每个 label 设置边框样式和居中对齐
        #   addWidget 时使用 stretch 参数：
        #     addWidget(label_a, 1)   → 占 1 份空间
        #     addWidget(label_b, 2)   → 占 2 份空间
        #     addWidget(label_c, 3)   → 占 3 份空间
        #   拖动窗口宽度观察：三个 label 的宽度比例是否始终是 1:2:3？
        ???

        # ========== 区域2：addStretch 弹簧 ==========

        # TODO(2): 创建一个 QHBoxLayout，添加 2 个 QPushButton
        #   用 addStretch() 实现"按钮靠右"效果：
        #     先 addStretch(1)   → 左边放一个弹簧
        #     再 addWidget(btn_ok)
        #     再 addWidget(btn_cancel)
        #   思考：addStretch(1) 的参数 1 是什么意思？
        #         如果两边都加 addStretch 会怎样？（按钮居中）
        ???

        # ========== 区域3：QSizePolicy ==========

        # TODO(3): 创建一个 QVBoxLayout，添加 3 个控件演示不同尺寸策略
        #   label_fixed: QLabel，设置 setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #     再设置 setFixedSize(150, 30)
        #     文本 "Fixed: 不会缩放"
        #
        #   label_preferred: QLabel，设置 setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #     文本 "Preferred: 有推荐尺寸，但可以缩放"
        #
        #   text_expanding: QTextEdit，设置 setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #     setText("Expanding: 会尽量占满剩余空间")
        #
        #   给每个控件设置边框样式
        #   拖动窗口大小观察：哪个控件在变大？哪个不动？
        #   思考：Fixed / Preferred / Expanding 三者的区别是什么？
        ???

        # ========== 区域4：最小/最大尺寸约束 ==========

        # TODO(4): 创建一个 QHBoxLayout，添加 2 个 QLabel
        #   label_min: 设置 setMinimumWidth(200)，文本 "最小宽度200"
        #   label_max: 设置 setMaximumWidth(150)，文本 "最大宽度150"
        #   给每个 label 设置边框样式
        #   拖动窗口宽度观察：
        #     缩小窗口时 label_min 是否会小于 200？
        #     放大窗口时 label_max 是否会超过 150？
        ???

        # ========== 主布局 ==========

        # TODO(5): 创建主 QVBoxLayout 组合所有区域
        #   加标题分隔 label
        #   setContentsMargins(10, 10, 10, 10)
        #   setSpacing(8)
        ???


def main():
    app = QApplication(sys.argv)
    w = SizePolicyDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()