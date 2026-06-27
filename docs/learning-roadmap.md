# Qt 学习路线图

当前阶段：**每日一练（基本功强化）**
已完成：**PySide6 (Python) 核心部分** + **Qt6 C++ 核心知识体系 #1~#12 全部完成**

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
| 5 | 样式与绘制 | ✅ 完成 | QSS 样式表、QPainter 基本图形、仪表盘（drawArc/cos/sin） |
| 6 | Model/View | ✅ 完成 | QStandardItemModel+QTableView、自定义Model（QAbstractTableModel）、role/flags/begin-endInsertRows |
| 7 | 多线程 | ✅ 完成 | QThread+Worker+moveToThread、QAtomicInteger、deleteLater、信号连接链、生命周期管理 |
| 8 | 文件与序列化 | ✅ 完成 | QFile/QTextStream、QJsonDocument/QJsonObject、QDataStream二进制序列化 |
| 9 | 进程与 IPC | ✅ 完成 | QProcess阻塞调用、start+waitForFinished+readAllStandardOutput |
| 10 | 自定义控件 | ✅ 完成 | 继承QWidget自绘（paintEvent/mousePressEvent/sizeHint）、LED指示灯控件、update()重绘机制、信号暴露、Plugin系统、Designer集成 |
| 11 | 构建系统 | ✅ 完成 | CMake/AUTOMOC/AUTOUIC/AUTORCC（已在实践中掌握，跳过单独练习） |
| 12 | Python/C++ 互操作 | ✅ 完成 | pybind11（CRC demo）、ctypes原理、Shiboken了解、ABI边界、Plugin系统、Designer集成（Plugin/提升控件/纯代码三种方式） |

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
| 2026-06-23 | 样式与绘制完成（QSS、QPainter 基本图形集合、仪表盘圆弧/刻度/指针） |
| 2026-06-24 | Model/View完成（QStandardItemModel快速上手、自定义Model底层机制、role/flags/dataChanged通知） |
| 2026-06-24 | 多线程完成（QThread+Worker+moveToThread、原子标志位、deleteLater、信号连接链、生命周期管理） |
| 2026-06-24 | 文件与序列化+进程完成（QFile/QTextStream/JSON读写/QDataStream二进制/QProcess调用外部程序） |
| 2026-06-26 | 自定义控件完成（继承QWidget自绘LED指示灯、paintEvent/mousePressEvent/sizeHint override、update()机制、QStyle了解） |
| 2026-06-26 | Python/C++互操作完成（pybind11 CRC demo、ctypes原理、Shiboken了解、Plugin系统、Designer集成三种方式对比） |

---

## 后续计划：每日一练（基本功强化）

**启动时机**：Qt6 C++ 核心知识体系全部完成后

**目标**：将核心能力内化为肌肉记忆，不查手册能手写完整可编译代码

**必须信手拈来的核心点**：

- 类的声明和实现分离（.h/.cpp）
- 成员初始化列表
- 指针 vs 引用 vs 值传递的选择
- new + 指针 + parent（Qt 控件创建）
- connect 四参数语法
- 信号和槽的声明模式（signals / private slots / emit）
- 布局基本用法（VBox/HBox + addWidget）
- QThread + Worker + moveToThread 模式
- 析构清理（quit + wait / deleteLater）
- const & 传参
- override
- Q_OBJECT 宏

**练习形式**：

| 形式 | 说明 |
|------|------|
| 骨架练习 | 给需求描述，空项目手写全部代码（15~30分钟） |
| 补洞练习 | 给有 bug/缺失的代码，补全或修复 |
| 默写练习 | 给题目，闭眼写出完整类声明/实现 |
| 限时重构 | 给有问题的实现，限时改成正确模式 |