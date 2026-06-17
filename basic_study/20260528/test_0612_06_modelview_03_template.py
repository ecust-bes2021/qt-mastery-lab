"""
Model/View 阶段③：自定义 QAbstractTableModel + Delegate
- 子类化 QAbstractTableModel 实现自定义模型
- 必须实现的方法：rowCount, columnCount, data
- 可选实现：headerData, setData, flags
- 自定义 Delegate（QStyledItemDelegate）实现自定义编辑器和渲染
- 大数据量展示的性能优势
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QHeaderView,
    QStyledItemDelegate,
    QSpinBox,
    QComboBox,
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor


# TODO(1): 自定义模型类 SensorDataModel，继承 QAbstractTableModel
#   模拟一组传感器数据：
#   内部数据结构用列表嵌套字典：
#     [{"name": "温度传感器", "value": 25.3, "unit": "℃", "status": "正常"},
#      {"name": "湿度传感器", "value": 60.1, "unit": "%", "status": "正常"},
#      {"name": "压力传感器", "value": 101.3, "unit": "kPa", "status": "警告"},
#      ...]
#   列定义：["传感器名称", "数值", "单位", "状态"]
#
#   必须实现：
#     rowCount(parent) — 返回行数
#     columnCount(parent) — 返回列数
#     data(index, role) — 返回指定单元格的数据
#       DisplayRole: 返回对应字段的值
#       BackgroundRole: 如果 status=="警告" 返回浅黄色，"异常" 返回浅红色
#       TextAlignmentRole: 数值列居中对齐
#     headerData(section, orientation, role) — 返回表头文字
#     flags(index) — 数值列和状态列可编辑（返回 Qt.ItemIsEditable）
#     setData(index, value, role) — 允许编辑数值和状态
#
#   思考：为什么自定义模型比 QStandardItemModel 更适合大数据？
#         （提示：QStandardItem 每个单元格都是一个对象，内存开销大）
???


# TODO(2): 自定义代理类 StatusDelegate，继承 QStyledItemDelegate
#   用于"状态"列的编辑——弹出一个 QComboBox 让用户选择状态
#
#   实现方法：
#     createEditor(parent, option, index) — 创建 QComboBox，添加 "正常","警告","异常"
#     setEditorData(editor, index) — 把模型当前值设到 ComboBox 上
#     setModelData(editor, model, index) — 把 ComboBox 选择的值写回模型
#
#   思考：Delegate 解决了什么问题？
#         如果不用 Delegate，双击单元格编辑时默认是什么控件？
???


class CustomModelDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model/View Practice - Phase 3: Custom Model & Delegate")
        self.setObjectName("mv_custom_demo")
        self.setMinimumSize(600, 400)

        # TODO(3): 创建 SensorDataModel 实例
        ???

        # TODO(4): 创建 QTableView，设置模型
        #   设置列宽自适应
        #   给"状态"列（第3列）设置 StatusDelegate
        #   使用 setItemDelegateForColumn(column, delegate)
        ???

        # TODO(5): 创建按钮 "添加传感器"
        #   点击时调用 self._add_sensor
        ???

        # TODO(6): 创建按钮 "模拟数据更新"
        #   点击时调用 self._update_values，随机修改传感器数值
        #   观察：视图是否自动刷新？
        ???

        # TODO(7): 创建一个 QLabel 显示说明
        #   文本："双击数值或状态列可以编辑"
        ???

        # TODO(8): 布局
        ???

    def _add_sensor(self):
        # TODO(9): 向模型中添加一行新传感器数据
        #   需要调用 beginInsertRows / endInsertRows 通知视图
        #   思考：为什么自定义模型修改数据时需要手动通知？
        #         QStandardItemModel 为什么不需要？
        ???

    def _update_values(self):
        # TODO(10): 随机更新某些传感器的数值
        #   修改内部数据后，发射 dataChanged 信号通知视图刷新
        #   使用 self._model.dataChanged.emit(top_left_index, bottom_right_index)
        #   思考：如果不发射 dataChanged，视图会怎样？
        ???


def main():
    app = QApplication(sys.argv)
    w = CustomModelDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()