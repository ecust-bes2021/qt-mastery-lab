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
        layout_1 = QFormLayout()
        layout_1.addRow("姓名：", QLineEdit())
        layout_1.addRow("邮箱：", QLineEdit())
        combo_dept = QComboBox()
        combo_dept.addItems(["研发","测试","产品"])
        layout_1.addRow("部门：", combo_dept)
        layout_1.addRow("备注：", QLineEdit())

        # ========== 区域2：QStackedWidget 页面切换 ==========

        # TODO(2): 创建一个 QComboBox 作为页面选择器
        #   添加选项 "页面1-基本信息", "页面2-高级设置", "页面3-关于"
        #   连接 currentIndexChanged 信号到 stacked widget 的 setCurrentIndex
        combo_pages = QComboBox()
        combo_pages.addItems(["页面1-基本信息","页面2-高级设置","页面3-关于"])
    

        # TODO(3): 创建一个 QStackedWidget，添加 3 个页面
        #   页面1：一个 QLabel "这是基本信息页面"
        #   页面2：一个 QLabel "这是高级设置页面"
        #   页面3：一个 QLabel "这是关于页面"
        #   给每个页面的 label 设置居中对齐和边框样式
        #   思考：QStackedWidget 和 QTabWidget 有什么区别？
        self._stacked_widget = QStackedWidget()
        label_1 = QLabel("这是基本信息页面")
        label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_1.setStyleSheet("border: 1px solid orange; padding: 5px")
        label_2 = QLabel("这是高级设置页面")
        label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_2.setStyleSheet("border: 1px solid orange; padding: 5px")
        label_3 = QLabel("这是关于页面")
        label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_3.setStyleSheet("border: 1px solid orange; padding: 5px")
        self._stacked_widget.addWidget(label_1)
        self._stacked_widget.addWidget(label_2)
        self._stacked_widget.addWidget(label_3)
        combo_pages.currentIndexChanged.connect(self._stacked_widget.setCurrentIndex)
        

        # ========== 区域3：动态添加/移除控件 ==========

        # TODO(4): 创建一个容器 QVBoxLayout 用于动态控件
        #   初始为空
        self.v_layout = QVBoxLayout()


        # TODO(5): 创建 "添加标签" 按钮
        #   点击时调用 self._add_label，向动态容器中添加一个新 QLabel
        #   新 label 文本为 f"动态标签 #{self._counter}"，每次递增
        self._btn_add_label = QPushButton("添加标签")
        self._btn_add_label.clicked.connect(self._add_label)
        self._counter = 0

        # TODO(6): 创建 "移除最后一个" 按钮
        #   点击时调用 self._remove_last，从动态容器中移除最后一个控件
        #   思考：移除控件时，只 removeWidget 够吗？还需要做什么？
        self._btn_remove_last = QPushButton("移除最后一个")
        self._btn_remove_last.clicked.connect(self._remove_last)

        # TODO(7): 创建 "插入到第一个" 按钮
        #   点击时调用 self._insert_first，在动态容器的第 0 个位置插入新控件
        self._btn_insert_first = QPushButton("插入到第一个")
        self._btn_insert_first.clicked.connect(self._insert_first)

        # TODO(8): 主布局组合所有区域
        #   加标题分隔 label
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        main_layout.addWidget(QLabel("========== 区域1：表单布局 =========="))
        main_layout.addLayout(layout_1)

        main_layout.addWidget(QLabel("========== 区域2：页面切换 =========="))
        main_layout.addWidget(combo_pages)
        main_layout.addWidget(self._stacked_widget)

        main_layout.addWidget(QLabel("========== 区域3：动态布局 =========="))
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._btn_add_label)
        btn_layout.addWidget(self._btn_remove_last)
        btn_layout.addWidget(self._btn_insert_first)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(self.v_layout)

        self.setLayout(main_layout)

    def _add_label(self):
        # TODO(9): 动态添加一个 QLabel 到动态容器布局
        #   self._counter += 1
        #   创建 QLabel，文本为 f"动态标签 #{self._counter}"
        #   设置边框样式
        #   addWidget 到动态容器布局
        self._counter+=1
        label = QLabel(f"动态标签 #{self._counter}")
        label.setStyleSheet("border: 1px solid red; padding: 5px")
        self.v_layout.addWidget(label)

    def _remove_last(self):
        # TODO(10): 移除动态容器布局中的最后一个控件
        #   获取布局的 count()
        #   如果 count > 0：
        #     用 layout.takeAt(count - 1) 取出 layout item
        #     获取 item.widget()
        #     如果 widget 存在，调用 widget.setParent(None) 彻底移除
        #   思考：为什么不能只 removeWidget？为什么要 setParent(None)？
        #         takeAt 和 removeWidget 的区别是什么？
        count = self.v_layout.count()
        if count > 0:
            item = self.v_layout.takeAt(count - 1)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def _insert_first(self):
        # TODO(11): 在动态容器布局的第 0 个位置插入新控件
        #   self._counter += 1
        #   创建 QLabel，文本为 f"插入的标签 #{self._counter}"
        #   设置不同颜色的边框样式（和普通添加区分）
        #   使用 layout.insertWidget(0, widget) 插入到第一个位置
        self._counter += 1
        label = QLabel(f"插入的标签 #{self._counter}")
        label.setStyleSheet("border: 1px solid green; padding: 5px")
        self.v_layout.insertWidget(0, label)


def main():
    app = QApplication(sys.argv)
    w = DynamicLayoutDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()