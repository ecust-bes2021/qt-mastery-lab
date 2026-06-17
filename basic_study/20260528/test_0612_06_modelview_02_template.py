"""
Model/View 阶段②：QStandardItemModel + 多列视图
- QStandardItemModel — 通用的标准模型
- QTableView — 表格视图
- QTreeView — 树形视图
- 数据角色（Qt.DisplayRole, Qt.EditRole, Qt.DecorationRole 等）
- QStandardItem 的使用
- 多列数据、表头设置
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QTableView,
    QTreeView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QHeaderView,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon
from PySide6.QtCore import Qt


class StandardModelDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model/View Practice - Phase 2: StandardItemModel")
        self.setObjectName("mv_standard_demo")
        self.setMinimumSize(600, 500)

        # ========== 区域1：QTableView ==========

        # TODO(1): 创建一个 QStandardItemModel，设置 4 列
        #   设置表头标签：["姓名", "年龄", "部门", "工号"]
        #   使用 setHorizontalHeaderLabels()
        ???

        # TODO(2): 向模型中添加几行数据
        #   使用 appendRow([QStandardItem, QStandardItem, ...])
        #   添加 3-4 行员工数据
        #   思考：QStandardItem 和直接的字符串有什么区别？
        ???

        # TODO(3): 给某些单元格设置不同的角色数据
        #   使用 item.setData(value, role) 设置：
        #     Qt.BackgroundRole — 设置背景色 QColor("lightyellow")
        #     Qt.ToolTipRole — 设置悬停提示文字
        #     Qt.TextAlignmentRole — 设置对齐方式
        #   思考：一个单元格可以同时存储多种角色的数据吗？
        #         DisplayRole 和 EditRole 的区别是什么？
        ???

        # TODO(4): 创建一个 QTableView，设置模型
        #   设置列宽自适应：header().setSectionResizeMode(QHeaderView.Stretch)
        #   启用排序：setSortingEnabled(True)
        ???

        # ========== 区域2：QTreeView ==========

        # TODO(5): 创建一个树形的 QStandardItemModel
        #   根节点下添加部门节点
        #   部门节点下添加员工节点
        #   结构如：
        #     研发部
        #       ├── 张三
        #       └── 李四
        #     测试部
        #       ├── 王五
        #       └── 赵六
        ???

        # TODO(6): 创建一个 QTreeView，设置模型
        #   展开所有节点：expandAll()
        ???

        # ========== 操作按钮 ==========

        # TODO(7): 创建按钮 "添加一行"
        #   点击时向表格模型末尾添加新数据
        ???

        # TODO(8): 创建按钮 "删除选中行"
        #   点击时从表格模型中删除 QTableView 当前选中的行
        ???

        # TODO(9): 布局
        ???

    def _add_table_row(self):
        # TODO(10): 向表格模型添加一行
        #   使用 appendRow
        ???

    def _remove_table_row(self):
        # TODO(11): 删除表格中选中的行
        #   获取 QTableView 的 currentIndex()
        #   用 model.removeRow(index.row()) 删除
        ???


def main():
    app = QApplication(sys.argv)
    w = StandardModelDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()