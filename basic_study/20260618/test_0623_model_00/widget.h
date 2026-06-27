#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QTableView>
#include <QStandardItemModel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>

// ============================================================
// Model/View 练习
//
// 目标：理解 Qt 的 Model/View 架构
//   - Model（数据层）：存储数据，不关心怎么显示
//   - View（视图层）：显示数据，不关心数据从哪来
//   - 两者通过 setModel() 连接
//
// 核心优势：
//   - 同一份数据可以有多个视图（表格/列表/树）
//   - 改数据 → 所有视图自动更新
//   - 数据量大时，View 只渲染可见区域（高性能）
//
// 本练习内容：
//   Part 1（必做）：用 QStandardItemModel + QTableView 展示数据
//   Part 2（选做）：自定义 Model（继承 QAbstractTableModel）
//
// 预期界面：
//   ┌────────────────────────────────────┐
//   │  姓名      │  年龄  │  职位        │
//   │────────────┼────────┼──────────────│
//   │  张三      │  28    │  工程师      │
//   │  李四      │  32    │  设计师      │
//   │  王五      │  25    │  测试工程师  │
//   │────────────────────────────────────│
//   │  [添加行]  [删除行]  [修改数据]    │
//   └────────────────────────────────────┘
// ============================================================

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = nullptr);
    ~Widget();

private slots:
    // TODO(1): 声明槽函数
    //   void onAddRow();         — 添加一行数据
    //   void onRemoveRow();      — 删除选中行
    //   void onModifyData();     — 修改某个单元格的数据
    void onAddRow();
    void onRemoveRow();
    void onModifyData();

private:
    // TODO(2): 声明成员变量
    //   QTableView *_tableView;           — 表格视图
    //   QStandardItemModel *_model;       — 数据模型
    //   QPushButton *_btnAdd;             — 添加按钮
    //   QPushButton *_btnRemove;          — 删除按钮
    //   QPushButton *_btnModify;          — 修改按钮
    QTableView *_tableView;
    QStandardItemModel *_model;
    QPushButton *_btnAdd;
    QPushButton *_btnRemove;
    QPushButton *_btnModify;
};

#endif // WIDGET_H