"""
QObject与对象树 阶段②：对象生命周期与销毁
- parent 销毁时子对象自动销毁（级联销毁）
- destroyed 信号的使用
- deleteLater() 延迟销毁
- Python 引用 vs Qt 对象生命周期冲突
"""
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import QObject, QTimer


class LifecycleDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject Practice - Phase 2: Lifecycle")
        self.setObjectName("lifecycle_demo")

        # TODO(1): 创建一个子 QObject（parent=self），objectName 设为 "child_a"
        #   连接它的 destroyed 信号到 self._on_destroyed
        #   思考：destroyed 信号的参数是什么？
        self.obj_a = QObject(parent=self,objectName="child_a")
        self.obj_a.destroyed.connect(self._on_destroyed)

        # TODO(2): 创建第二个子 QObject（parent=self），objectName 设为 "child_b"
        #   同样连接 destroyed 信号
        self.obj_b = QObject(parent=self,objectName="child_b")
        self.obj_b.destroyed.connect(self._on_destroyed)

        # TODO(3): 创建一个按钮 "删除 child_a (deleteLater)"
        #   点击时调用 self._delete_child_a
        self._btn_a = QPushButton("删除 child_a (deleteLater)")
        self._btn_a.clicked.connect(self._delete_child_a)

        # TODO(4): 创建一个按钮 "访问已销毁对象"
        #   点击时调用 self._access_deleted
        self._btn_ved = QPushButton("访问已销毁对象")
        self._btn_ved.clicked.connect(self._access_deleted)

        # TODO(5): 创建一个按钮 "销毁容器(演示级联)"
        #   点击时调用 self._cascade_destroy
        self._btn_vec = QPushButton("销毁容器（演示级联）")
        self._btn_vec.clicked.connect(self._cascade_destroy)

        # TODO(6): 布局
        layout = QVBoxLayout()
        layout.addWidget(self._btn_a)
        layout.addWidget(self._btn_ved)
        layout.addWidget(self._btn_vec)
        self.setLayout(layout)

    def _on_destroyed(self, obj):
        # TODO(7): 打印被销毁对象的信息
        #   格式：f"[destroyed] {obj.objectName()} 被销毁了"
        #   思考：这个回调触发时，obj 还能访问哪些信息？哪些已经不安全了？
        print(f"[destroyed] {obj.objectName()} 被销毁了")

    def _delete_child_a(self):
        # TODO(8): 使用 deleteLater() 销毁 child_a
        #   销毁前打印 "调用 deleteLater..."
        #   销毁后（在下一轮事件循环）child_a 的 C++ 对象会被释放
        #   思考：deleteLater() 和直接 del 有什么区别？
        #         为什么不能在信号槽处理过程中直接 delete？
        print("调用 deleteLater...")
        self.obj_a.deleteLater()

    def _access_deleted(self):
        # TODO(9): 尝试访问已经被 deleteLater 销毁的 child_a
        #   用 try/except 捕获 RuntimeError
        #   打印捕获到的异常信息
        #   思考：为什么 Python 变量还在，但访问会报错？
        #         这说明 Python wrapper 和 C++ 对象的关系是什么？
        try:
            print(self.obj_a.objectName())
        except RuntimeError as e:
            print(f"捕获异常：{e}")

    def _cascade_destroy(self):
        # TODO(10): 演示级联销毁
        #   创建一个临时的 QObject 容器 "container"
        #   在 container 下创建 3 个子对象 "item_0", "item_1", "item_2"
        #   给每个子对象都连接 destroyed 信号
        #   然后 del container 或 container.deleteLater()
        #   观察：3 个子对象是否都被自动销毁了？销毁顺序是什么？
        container = QObject(objectName="container")
    
        for i in range(3):
            child = QObject(parent=container, objectName=f"item_{i}")
            child.destroyed.connect(self._on_destroyed)
        
        container.destroyed.connect(self._on_destroyed)
        
        # 销毁树根
        del container


def main():
    app = QApplication(sys.argv)
    w = LifecycleDemo()
    w.show()

    print("=== 初始子对象 ===")
    for child in w.children():
        print(f"  {child.objectName()} ({type(child).__name__})")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()