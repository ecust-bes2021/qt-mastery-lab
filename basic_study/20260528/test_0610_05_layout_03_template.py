"""
布局系统 阶段③：QFormLayout + QStackedLayout + 动态布局
- QFormLayout 表单布局
- QStackedLayout / QStackedWidget 页面切换
- 运行时动态添加/移除控件
- layout.removeWidget() / widget.setParent(None)
- layout.insertWidget() 插入到指定位置
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QStackedWidget,
)
from PySide6.QtCore import Qt


class DynamicLayoutDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout Practice - Phase 3: Form & Stacked & Dynamic")
        self.setObjectName("dynamic_layout_demo")
        self.setMinimumSize(500, 450)

        # ========== 区域1：QFormLayout 表单布局 ==========

        # TODO(1): 创建一个 QFormLayout
        #   使用 addRow(label, widget) 添加以下行：
        #     "姓名：" + QLineEdit
        #     "邮箱：" + QLineEdit
        #     "部门：" + QComboBox（添加选项 "研发", "测试", "产品"）
        #     "备注：" + QLineEdit
        #   思考：QFormLayout 和手动用 QHBoxLayout 嵌套 QLabel+QLineEdit 有什么区别？
        #         QFormLayout 在不同平台（Windows/macOS）上的对齐风格有什么不同？
        ???

        # ========== 区域2：QStackedWidget 页面切换 ==========

        # TODO(2): 创建一个 QComboBox 作为页面选择器
        #   添加选项 "页面1-基本信息", "页面2-高级设置", "页面3-关于"
        #   连接 currentIndexChanged 信号到 stacked widget 的 setCurrentIndex
        ???

        # TODO(3): 创建一个 QStackedWidget，添加 3 个页面
        #   页面1：一个 QLabel "这是基本信息页面"
        #   页面2：一个 QLabel "这是高级设置页面"
        #   页面3：一个 QLabel "这是关于页面"
        #   给每个页面的 label 设置居中对齐和边框样式
        #   思考：QStackedWidget 和 QTabWidget 有什么区别？
        ???

        # ========== 区域3：动态添加/移除控件 ==========

        # TODO(4): 创建一个容器 QVBoxLayout 用于动态控件
        #   初始为空
        ???

        # TODO(5): 创建 "添加标签" 按钮
        #   点击时调用 self._add_label，向动态容器中添加一个新 QLabel
        #   新 label 文本为 f"动态标签 #{self._counter}"，每次递增
        ???

        # TODO(6): 创建 "移除最后一个" 按钮
        #   点击时调用 self._remove_last，从动态容器中移除最后一个控件
        #   思考：移除控件时，只 removeWidget 够吗？还需要做什么？
        ???

        # TODO(7): 创建 "插入到第一个" 按钮
        #   点击时调用 self._insert_first，在动态容器的第 0 个位置插入新控件
        ???

        # TODO(8): 主布局组合所有区域
        #   加标题分隔 label
        ???

        self._counter = 0

    def _add_label(self):
        # TODO(9): 动态添加一个 QLabel 到动态容器布局
        #   self._counter += 1
        #   创建 QLabel，文本为 f"动态标签 #{self._counter}"
        #   设置边框样式
        #   addWidget 到动态容器布局
        ???

    def _remove_last(self):
        # TODO(10): 移除动态容器布局中的最后一个控件
        #   获取布局的 count()
        #   如果 count > 0：
        #     用 layout.takeAt(count - 1) 取出 layout item
        #     获取 item.widget()
        #     如果 widget 存在，调用 widget.setParent(None) 彻底移除
        #   思考：为什么不能只 removeWidget？为什么要 setParent(None)？
        #         takeAt 和 removeWidget 的区别是什么？
        ???

    def _insert_first(self):
        # TODO(11): 在动态容器布局的第 0 个位置插入新控件
        #   self._counter += 1
        #   创建 QLabel，文本为 f"插入的标签 #{self._counter}"
        #   设置不同颜色的边框样式（和普通添加区分）
        #   使用 layout.insertWidget(0, widget) 插入到第一个位置
        ???


def main():
    app = QApplication(sys.argv)
    w = DynamicLayoutDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()