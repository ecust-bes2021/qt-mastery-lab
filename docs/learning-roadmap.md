# Qt 学习路线图

当前阶段：**PySide6 (Python)**
后续计划：**Qt6 C++**

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
| 7 | 多线程 | 3 | 🔄 进行中 | QThread+Worker、线程安全+取消暂停、串口模拟实战 |
| 8 | 文件与序列化 | - | ⬜ 待定 | QSettings、JSON/二进制读写 |
| 9 | 进程与 IPC | - | ⬜ 待定 | QProcess、管道、本地 socket |
| 10 | 自定义控件 | - | ⬜ 待定 | 组合控件、QWidget 子类化、属性系统 |

---

## Qt6 C++ 核心知识体系（后续）

| # | 主题 | 状态 | 备注 |
|---|------|------|------|
| 1 | QObject 与对象树 | ⬜ 待定 | 与 PySide6 对应，关注内存管理差异 |
| 2 | 信号与槽 | ⬜ 待定 | MOC、connect 语法（新旧）、类型安全 |
| 3 | 事件系统 | ⬜ 待定 | 事件循环、事件过滤器 |
| 4 | 布局系统 | ⬜ 待定 | 与 PySide6 基本一致 |
| 5 | 样式与绘制 | ⬜ 待定 | QPainter、QGraphicsView |
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