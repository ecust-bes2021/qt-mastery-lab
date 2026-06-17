"""
QObject与对象树 阶段①：父子关系与对象树（模板）
- parent 参数的作用
- children() 获取子对象列表
- findChild() / findChildren() 查找子对象
- 对象树的结构与遍历
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import QObject


class ParentChildDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject Practice - Phase 1: Parent-Child")

        # TODO(1): 给自己设置 objectName 为 "main_widget"
        ???

        # TODO(2): 创建控件时传入 parent 参数（self）
        #   - QLabel("标签A", parent=self)，objectName 设为 "label_a"
        #   - QLabel("标签B", parent=self)，objectName 设为 "label_b"
        #   - QPushButton("查看对象树", parent=self)，objectName 设为 "btn_tree"
        #   思考：传 parent=self 和不传 parent 有什么区别？
        ???

        # TODO(3): 创建一个没有 parent 的 QObject，objectName 设为 "orphan"
        #   思考：这个对象会出现在 self.children() 里吗？
        ???

        # TODO(4): 布局
        ???

        # TODO(5): 连接按钮 clicked 到 _print_tree
        ???

    def _print_tree(self):
        # TODO(6): 打印 self 的所有子对象
        #   使用 self.children() 遍历，打印每个子对象的 objectName 和类型
        #   格式：f"  {child.objectName()} ({type(child).__name__})"
        ???

    def _find_child_demo(self):
        # TODO(7): 使用 findChild 按 objectName 查找 "label_a"
        #   打印找到的对象的 text()
        #   思考：findChild 的查找范围是什么？（直接子对象 or 递归所有后代？）
        ???

    def _find_children_demo(self):
        # TODO(8): 使用 findChildren 查找所有 QLabel 类型的子对象
        #   打印每个找到的 QLabel 的 text()
        ???


def main():
    app = QApplication(sys.argv)
    w = ParentChildDemo()
    w.show()

    print("=== 对象树结构 ===")
    w._print_tree()

    print("\n=== findChild 演示 ===")
    w._find_child_demo()

    print("\n=== findChildren 演示 ===")
    w._find_children_demo()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()