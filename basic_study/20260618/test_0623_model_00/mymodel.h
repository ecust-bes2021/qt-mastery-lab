#ifndef MYMODEL_H
#define MYMODEL_H

#include <QAbstractTableModel>
#include <QString>
#include <QVector>
#define MYMODEL_COLUMN_COUNT 3

// ============================================================
// 自定义 Model（选做）
//
// 目标：理解 Model 的底层机制
//   - 继承 QAbstractTableModel
//   - 数据存在自己的结构体中
//   - 实现"问答接口"供 View 查询
//
// 数据结构：
//   struct Employee {
//       QString name;
//       int age;
//       QString position;
//   };
//   QVector<Employee> _data;   ← 数据存这里，不是 QStandardItem
// ============================================================

struct Employee {
    QString name;
    int age;
    QString position;
};

class MyModel : public QAbstractTableModel
{
    Q_OBJECT

public:
    explicit MyModel(QObject *parent = nullptr);

    // TODO(M1): 重写必须的纯虚函数（View 的"问答接口"）
    //
    //   int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    //   // View 问："有几行？" → 返回 _data.size()
    //
    //   int columnCount(const QModelIndex &parent = QModelIndex()) const override;
    //   // View 问："有几列？" → 返回 3（姓名、年龄、职位）
    //
    //   QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    //   // View 问："第 index.row() 行第 index.column() 列显示什么？"
    //   // role 参数表示"问的是什么"：
    //   //   Qt::DisplayRole = 显示的文字
    //   //   Qt::TextAlignmentRole = 对齐方式
    //   //   Qt::BackgroundRole = 背景色
    //   //   ... View 会用不同 role 多次问同一个单元格
    int rowCount(const QModelIndex &parent = QModelIndex())const override;

    int columnCount(const QModelIndex &parent = QModelIndex())const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // TODO(M2): 重写表头（可选但推荐）
    //
    //   QVariant headerData(int section, Qt::Orientation orientation,
    //                       int role = Qt::DisplayRole) const override;
    //   // View 问："第 section 列的表头叫什么？"
    //   // orientation: Horizontal = 列头, Vertical = 行号
    QVariant headerData(int section, Qt::Orientation orientation,int role = Qt::DisplayRole) const override;
    

    // TODO(M3): 支持编辑（可选）
    //
    //   bool setData(const QModelIndex &index, const QVariant &value,
    //                int role = Qt::EditRole) override;
    //   // View 说："用户把第 index 个单元格改成了 value"
    //   // 你需要：1. 更新 _data  2. 发射 dataChanged 信号
    //
    //   Qt::ItemFlags flags(const QModelIndex &index) const override;
    //   // View 问："这个单元格能不能编辑？"
    //   // 返回 Qt::ItemIsEditable | Qt::ItemIsEnabled | Qt::ItemIsSelectable
    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override;
    Qt::ItemFlags flags(const QModelIndex &index) const override;

    // TODO(M4): 添加/删除行的公共方法
    //
    //   void addEmployee(const Employee &emp);
    //   void removeEmployee(int row);

    void addEmployee(const Employee &emp);
    void removeEmployee(int row);

private:
    QVector<Employee> _data;
};

#endif // MYMODEL_H