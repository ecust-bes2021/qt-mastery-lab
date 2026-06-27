#include "mymodel.h"

MyModel::MyModel(QObject *parent)
    : QAbstractTableModel(parent)
{
    _data.append({"张三", 28, "工程师"});
    _data.append({"李四", 32, "设计师"});
    _data.append({"王五", 25, "测试工程师"});
}

// TODO(M1): 实现三个必须的纯虚函数
//
//   int MyModel::rowCount(const QModelIndex &parent) const {
//       Q_UNUSED(parent);
//       return _data.size();    // 有几条数据就有几行
//   }
//
//   int MyModel::columnCount(const QModelIndex &parent) const {
//       Q_UNUSED(parent);
//       return 3;               // 固定3列：姓名、年龄、职位
//   }
//
//   QVariant MyModel::data(const QModelIndex &index, int role) const {
//       if (!index.isValid()) return QVariant();   // 防御性检查
//
//       const Employee &emp = _data[index.row()];  // 取出这一行对应的数据
//
//       if (role == Qt::DisplayRole || role == Qt::EditRole) {
//           // View 问"显示什么文字？"
//           switch (index.column()) {
//               case 0: return emp.name;
//               case 1: return emp.age;
//               case 2: return emp.position;
//           }
//       }
//       // 其他 role（背景色、对齐等）不处理，返回空 QVariant
//       return QVariant();
//   }
int MyModel::rowCount(const QModelIndex &parent)const{
    Q_UNUSED(parent);
    return _data.size();
}
int MyModel::columnCount(const QModelIndex &parent)const{
    Q_UNUSED(parent);
    return MYMODEL_COLUMN_COUNT;
}

QVariant MyModel::data(const QModelIndex &index, int role)const{
    if(!index.isValid())return QVariant();
    const Employee &emp = _data[index.row()];
    if(role == Qt::DisplayRole || role == Qt::EditRole){
        switch (index.column())
        {
        case 0: return emp.name;
        case 1: return emp.age;
        case 2: return emp.position;
        }
    }
    return QVariant();
}


// TODO(M2): 实现表头
//
//   QVariant MyModel::headerData(int section, Qt::Orientation orientation, int role) const {
//       if (role != Qt::DisplayRole) return QVariant();
//
//       if (orientation == Qt::Horizontal) {
//           // 列头
//           switch (section) {
//               case 0: return "姓名";
//               case 1: return "年龄";
//               case 2: return "职位";
//           }
//       } else {
//           // 行号（Vertical），默认显示行号即可
//           return section + 1;   // 从1开始编号
//       }
//       return QVariant();
//   }
QVariant MyModel::headerData(int section, Qt:: Orientation orientation, int role) const{
    if(role != Qt::DisplayRole) return QVariant();
    if(orientation == Qt::Horizontal){
        switch(section){
            case 0: return "姓名";
            case 1: return "年龄";
            case 2: return "职位";
        }

    }else{
        return section + 1;
    }
    return QVariant();
}


// TODO(M3): 实现编辑支持
//
//   bool MyModel::setData(const QModelIndex &index, const QVariant &value, int role) {
//       if (!index.isValid() || role != Qt::EditRole) return false;
//
//       Employee &emp = _data[index.row()];   // 注意这里是引用 &，要修改原数据
//
//       switch (index.column()) {
//           case 0: emp.name = value.toString(); break;
//           case 1: emp.age = value.toInt(); break;
//           case 2: emp.position = value.toString(); break;
//           default: return false;
//       }
//
//       emit dataChanged(index, index);   // 通知 View："这个位置的数据变了"
//       return true;
//   }
//
//   Qt::ItemFlags MyModel::flags(const QModelIndex &index) const {
//       if (!index.isValid()) return Qt::NoItemFlags;
//       return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable;
//       // 告诉 View：这个单元格可以选中、可以编辑
//   }

bool MyModel::setData(const QModelIndex &index, const QVariant &value ,int role){
    if(!index.isValid() || role!= Qt::EditRole)return false;
    Employee &emp = _data[index.row()];
    switch (index.column())
    {
    case 0: emp.name = value.toString();break;
    case 1: emp.age = value.toInt();break;
    case 2: emp.position = value.toString();break;
    default: return false;
    }
    emit dataChanged(index,index);
    return true;
}

Qt::ItemFlags MyModel::flags(const QModelIndex &index)const{
    if(!index.isValid())return Qt::NoItemFlags;
    return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable;
}
// TODO(M4): 添加和删除行
//
//   void MyModel::addEmployee(const Employee &emp) {
//       beginInsertRows(QModelIndex(), _data.size(), _data.size());
//       // ↑ 通知 View："我要在第 _data.size() 行插入1行"
//       //   参数：parent, 起始行, 结束行
//       //   必须在修改数据之前调用！
//
//       _data.append(emp);
//
//       endInsertRows();
//       // ↑ 通知 View："插入完毕，你可以刷新了"
//   }
//
//   void MyModel::removeEmployee(int row) {
//       if (row < 0 || row >= _data.size()) return;
//
//       beginRemoveRows(QModelIndex(), row, row);
//       // ↑ 通知 View："我要删除第 row 行"
//
//       _data.removeAt(row);
//
//       endRemoveRows();
//       // ↑ 通知 View："删除完毕"
//   }
//
//   为什么要 begin/end 配对调用？
//   因为 View 需要知道"什么时候开始变、什么时候变完"
//   才能正确地更新显示（动画、滚动条、选中状态等）
//   如果你直接改 _data 不通知 → View 不知道数据变了 → 显示错乱

void MyModel::addEmployee(const Employee &emp){
    beginInsertRows(QModelIndex(),_data.size(),_data.size());
    _data.append(emp);
    endInsertRows();
}


void MyModel::removeEmployee(int row){
    if(row < 0 || row >=_data.size())return;

    beginRemoveRows(QModelIndex(), row , row);
    _data.removeAt(row);
    endRemoveRows();

}