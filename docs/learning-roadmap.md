# Qt 学习路线图

当前阶段：**Qt6 C++**
已完成：**PySide6 (Python) 核心部分**

---

## PySide6 核心知识体系

| # | 主题 | 阶段数 | 状态 | 备注 |
|---|------|--------|------|------|
| 1 | QObject 与对象树 | 3 | ✅ 完成 | 父子关系、生命周期、元对象系统 |
| 2 | 信号与槽 | 5 | ✅ 完成 | 定义/发射/多种连接/内置vs自定义/disconnect与ConnectionType |
| 3 | 事件系统 | 3 | ✅ 完成 | 事件循环、事件过滤器、自定义事件 |
| 4 | 布局系统 | 3 | ✅ 完成 | Layout 类型、尺寸策略、自适应 |
| 5 | 样式与绘制 | - | ⬜ 待定 | QSS 样式表、QPainter 自绘 |
| 6 | Model/View | 3 | ✅ 完成 | QStringListModel、QStandardItemModel、自定义模型+Delegate |
| 7 | 多线程 | 3 | ✅ 完成 | QThread+Worker、线程安全+取消暂停、串口模拟实战 |
| 8 | 文件与序列化 | - | ⬜ 待定 | QSettings、JSON/二进制读写 |
| 9 | 进程与 IPC | - | ⬜ 待定 | QProcess、管道、本地 socket |
| 10 | 自定义控件 | - | ⬜ 待定 | 组合控件、QWidget 子类化、属性系统 |

---

## Qt6 C++ 核心知识体系（后续）

| # | 主题 | 状态 | 备注 |
|---|------|------|------|
| 1 | QObject 与对象树 | ✅ 完成 | 与 PySide6 对应，关注内存管理差异 |
| 2 | 信号与槽 | ✅ 完成 | MOC、connect 语法、emit、自定义信号槽、跨对象通信 |
| 3 | 事件系统 | ✅ 完成 | 三层处理机制（eventFilter/event/xxxEvent）、override、虚函数重写 |
| 4 | 布局系统 | ✅ 完成 | VBox/HBox/Grid、嵌套、stretch、spacing、margins、SizePolicy |
| 5 | 样式与绘制 | 🔄 进行中 | QSS 已完成，QPainter 待练习 |
| 6 | Model/View | ⬜ 待定 | 性能优化、自定义 Model |
| 7 | 多线程 | ⬜ 待定 | QThread、QtConcurrent、线程安全 |
| 8 | 文件与序列化 | ⬜ 待定 | QDataStream、二进制格式 |
| 9 | 进程与 IPC | ⬜ 待定 | QProcess、D-Bus、共享内存 |
| 10 | 自定义控件 | ⬜ 待定 | Plugin 系统、Designer 集成 |
| 11 | 构建系统 | ⬜ 待定 | CMake、qmake、MOC/UIC/RCC |
| 12 | Python/C++ 互操作 | ⬜ 待定 | pybind11、Shiboken、ABI 边界 |

---

## 学习记录

| 日期 | 完成内容 |
|------|---------|
| 2026-06-09 | 信号与槽 阶段①~⑤ 全部完成 |
| 2026-06-09 | QObject 与对象树 开始 |
| 2026-06-16 | 多线程 阶段①~③ 全部完成（QThread+Worker、QMutex线程安全、串口模拟实战） |
| 2026-06-16 | PySide6 核心部分暂停，转入 Qt6 C++ 学习 |
| 2026-06-22 | QObject 与对象树完成（对象树、parent-child、内存管理、children 遍历） |
| 2026-06-22 | 信号与槽完成（自定义信号槽、emit、connect 四参数、跨对象通信、Sensor 练习） |
| 2026-06-22 | 事件系统完成（三层机制、eventFilter、override、mousePressEvent/keyPressEvent） |
| 2026-06-23 | 布局系统完成（Grid/HBox/VBox嵌套、stretch、spacing、margins、SizePolicy） |