"""
Model/View 阶段①：基础概念与 QStringListModel
- Model/View 架构的核心思想：数据和展示分离
- QStringListModel — 最简单的模型
- QListView — 列表视图
- 通过模型操作数据，视图自动更新
- 选择模型（QItemSelectionModel）
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QListView,
    QPushButton,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, QStringListModel, QModelIndex


class ModelViewBasicDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model/View Practice - Phase 1: Basics")
        self.setObjectName("mv_basic_demo")
        self.setMinimumSize(400, 400)

        # TODO(1): 创建一个 QStringListModel
        #   初始数据为 ["苹果", "香蕉", "橘子", "葡萄", "西瓜"]
        #   思考：模型负责什么？视图负责什么？它们之间怎么通信？
        ???

        # TODO(2): 创建一个 QListView，把模型设置给它
        #   使用 setModel() 关联模型和视图
        #   思考：如果同一个模型设置给两个不同的视图，会怎样？
        ???

        # TODO(3): 创建一个 QLineEdit 用于输入新项目
        #   placeholder 设为 "输入新水果名称"
        ???

        # TODO(4): 创建按钮 "添加到末尾"
        #   点击时调用 self._add_item
        ???

        # TODO(5): 创建按钮 "删除选中项"
        #   点击时调用 self._remove_selected
        ???

        # TODO(6): 创建按钮 "修改选中项"
        #   点击时调用 self._edit_selected
        ???

        # TODO(7): 创建一个 QLabel 显示当前模型数据
        #   objectName 设为 "data_display"
        ???

        # TODO(8): 创建按钮 "打印模型数据"
        #   点击时调用 self._print_model_data
        #   把模型中所有数据打印到 data_display
        ???

        # TODO(9): 布局
        ???

    def _add_item(self):
        # TODO(10): 向模型末尾添加一项
        #   获取 QLineEdit 中的文本
        #   获取当前模型的行数：model.rowCount()
        #   在末尾插入一行：model.insertRow(row_count)
        #   设置新行的数据：model.setData(model.index(row_count), text)
        #   清空 QLineEdit
        #   思考：为什么不直接操作视图，而是操作模型？
        ???

    def _remove_selected(self):
        # TODO(11): 删除当前选中的项
        #   获取选中的索引：self._list_view.currentIndex()
        #   检查索引是否有效：index.isValid()
        #   如果有效，用 model.removeRow(index.row()) 删除
        #   思考：删除后视图会自动更新吗？你做了什么来触发更新？
        ???

    def _edit_selected(self):
        # TODO(12): 修改当前选中项的文本
        #   获取选中的索引
        #   获取 QLineEdit 中的新文本
        #   用 model.setData(index, new_text) 修改
        #   思考：setData 的第三个参数 role 默认是什么？
        ???

    def _print_model_data(self):
        # TODO(13): 打印模型中所有数据
        #   用 model.stringList() 获取全部数据
        #   或者用循环遍历：for i in range(model.rowCount()):
        #     model.data(model.index(i), Qt.DisplayRole)
        #   更新 data_display 的文本
        ???


def main():
    app = QApplication(sys.argv)
    w = ModelViewBasicDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()