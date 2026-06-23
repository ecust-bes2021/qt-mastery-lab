#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // TODO(3): 创建中心 widget
    //   用 new 创建 QWidget，parent 传 this
    //   调用 setCentralWidget() 设置为主窗口的中心控件
    //   设置 objectName 为 "centralWidget"
    _centralWidget = new QWidget(this);
    this->setCentralWidget(_centralWidget);
    _centralWidget->setObjectName("centralWidget");

    // TODO(4): 创建子控件
    //   用 new 创建 QLabel 和 QPushButton，parent 传 _centralWidget
    //   设置每个控件的 objectName（"label1"、"label2"、"btn_print"）
    //   设置 label 的文本为 "设备A"、"设备B"
    //   设置按钮文本为 "打印对象树"
    //
    //   关键点：new QLabel(_centralWidget) 中的 _centralWidget 就是 parent
    //           这样就建立了对象树的父子关系

    _label1 = new QLabel("设备A", _centralWidget);
    _label1->setObjectName("label1");

    _label2 = new QLabel("设备B", _centralWidget);
    _label2->setObjectName("label2");

    _btn = new QPushButton("打印对象树", _centralWidget);
    _btn->setObjectName("btn_print");

    // TODO(5): 布局
    //   创建 QVBoxLayout
    //   把三个控件加入布局
    //   把布局设置给 _centralWidget
    //
    //   注意：C++ 里 layout 也用 new 创建，不需要手动 delete
    //         因为 setLayout 后 layout 的 parent 自动被设为 widget
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(_label1);
    layout->addWidget(_label2);
    layout->addWidget(_btn);
    _centralWidget->setLayout(layout);

    // TODO(6): 连接信号槽
    //   connect(_btn, &QPushButton::clicked, this, &MainWindow::onPrintTree);
    //
    //   对比 PySide6：self._btn.clicked.connect(self.on_print_tree)
    //   C++ 用 &类名::函数名 的方式指定槽函数（编译时类型安全）

    connect(_btn,&QPushButton::clicked,this, &MainWindow::onPrintTree);

    setWindowTitle("QObject 对象树练习");
    resize(400, 300);
}

MainWindow::~MainWindow()
{
    // TODO(7): 思考题
    //   这里不需要写任何 delete，为什么？
    //   如果你在 TODO(4) 里创建控件时没有传 parent，会发生什么？
    //   提示：没有 parent 的对象不在对象树里，MainWindow 销毁时不会自动释放它们 → 内存泄漏
}

// TODO(8): 实现槽函数 onPrintTree
//   遍历 _centralWidget 的所有子对象：
//     const QObjectList &children = _centralWidget->children();
//     for (QObject *child : children) {
//         qDebug() << "对象名:" << child->objectName()
//                  << "类型:" << child->metaObject()->className();
//     }
//
//   对比 PySide6：
//     for child in self._central_widget.children():
//         print(child.objectName(), type(child).__name__)
//
//   思考：children() 返回的列表里会不会包含 layout 对象？为什么？
 void MainWindow:: onPrintTree(){
    const QObjectList &children = _centralWidget->children();
    for(QObject *child :children){
        qDebug() << "对象名" << child->objectName()
                 << "类型：" << child->metaObject()->className();
    }

 }