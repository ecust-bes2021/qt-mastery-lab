"""
QObject与对象树 阶段③：元对象系统
- metaObject() 获取元对象信息
- className() 获取类名
- inherits() 判断继承关系
- setProperty() / property() 动态属性
- 动态属性配合 QSS 样式表
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import QObject


class MetaObjectDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject Practice - Phase 3: Meta-Object System")
        self.setObjectName("meta_demo")

        # TODO(1): 创建一个 QLabel 和一个 QPushButton（parent=self）
        #   label objectName 设为 "info_label"，文本为 "元对象系统演示"
        #   button objectName 设为 "btn_meta"，文本为 "打印元对象信息"
        ???

        # TODO(2): 创建一个按钮 "检查继承关系"
        #   objectName 设为 "btn_inherits"
        #   点击时调用 self._check_inherits
        ???

        # TODO(3): 创建一个按钮 "设置动态属性"
        #   objectName 设为 "btn_property"
        #   点击时调用 self._set_dynamic_property
        ???

        # TODO(4): 创建一个按钮 "读取动态属性"
        #   objectName 设为 "btn_read_prop"
        #   点击时调用 self._read_dynamic_property
        ???

        # TODO(5): 创建一个 QLabel 用于演示 QSS 动态属性样式切换
        #   objectName 设为 "status_label"，文本为 "状态: 正常"
        ???

        # TODO(6): 创建一个按钮 "切换状态样式"
        #   objectName 设为 "btn_toggle_style"
        #   点击时调用 self._toggle_status
        ???

        # TODO(7): 布局
        ???

        # TODO(8): 连接 btn_meta 的 clicked 信号到 self._print_meta_info
        ???

        # TODO(9): 设置 QSS 样式表，利用动态属性选择器
        #   QLabel[status="normal"] { color: green; }
        #   QLabel[status="warning"] { color: orange; font-weight: bold; }
        #   QLabel[status="error"] { color: red; font-weight: bold; }
        #   思考：动态属性改变后，样式会自动更新吗？需要做什么？
        ???

    def _print_meta_info(self):
        # TODO(10): 打印 self 和 info_label 的元对象信息
        #   使用 metaObject() 获取元对象
        #   打印 className()
        #   打印 metaObject().propertyCount() — 该对象有多少个属性
        #   打印 metaObject().methodCount() — 该对象有多少个方法（包括信号和槽）
        #   思考：propertyCount 包含的是哪些属性？只有你手动设的，还是包括 Qt 内置的？
        ???

    def _check_inherits(self):
        # TODO(11): 使用 inherits() 检查继承关系
        #   检查 info_label 是否 inherits("QLabel")
        #   检查 info_label 是否 inherits("QWidget")
        #   检查 info_label 是否 inherits("QObject")
        #   检查 info_label 是否 inherits("QPushButton")
        #   打印每个检查的结果
        #   思考：inherits() 是基于 C++ 继承链还是 Python 的 isinstance？
        ???

    def _set_dynamic_property(self):
        # TODO(12): 给 info_label 设置动态属性
        #   setProperty("priority", 5)
        #   setProperty("category", "display")
        #   打印 "动态属性已设置"
        #   思考：动态属性和 Python 的实例属性（self.xxx）有什么区别？
        #         动态属性存在哪里？能被 QSS 选择器使用吗？
        ???

    def _read_dynamic_property(self):
        # TODO(13): 读取 info_label 的动态属性
        #   使用 property("priority") 读取
        #   使用 property("category") 读取
        #   尝试读取一个不存在的属性 property("nonexist")，观察返回值
        #   打印所有结果
        ???

    def _toggle_status(self):
        # TODO(14): 切换 status_label 的状态动态属性
        #   读取当前 property("status")
        #   按 "normal" -> "warning" -> "error" -> "normal" 循环切换
        #   设置新属性值后，更新 label 文本为 f"状态: {new_status}"
        #   调用 self.style().unpolish(self._status_label)
        #   调用 self.style().polish(self._status_label)
        #   思考：为什么改了属性后需要 unpolish/polish？
        #         QSS 引擎什么时候会重新评估样式规则？
        ???


def main():
    app = QApplication(sys.argv)
    w = MetaObjectDemo()
    w.show()

    print("=== 元对象基本信息 ===")
    w._print_meta_info()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()