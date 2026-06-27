#include "widget.h"
#include <QHeaderView>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    // TODO(3): 创建 Model
    //   _model = new QStandardItemModel(this);
    //
    //   设置表头（列名）：
    //   _model->setHorizontalHeaderLabels({"姓名", "年龄", "职位"});
    //
    //   QStandardItemModel 是一个"万能模型"：
    //   - 它内部用 QStandardItem 存储每个单元格的数据
    //   - 不需要你自己管数据结构，直接往里塞 item 就行
    //   - 适合快速开发、数据量不大的场景
    _model =  new QStandardItemModel(this);
    _model->setHorizontalHeaderLabels({"姓名","年龄","职位"});


    // TODO(4): 往 Model 中添加初始数据
    //   QList<QStandardItem*> row1;
    //   row1 << new QStandardItem("张三")
    //        << new QStandardItem("28")
    //        << new QStandardItem("工程师");
    //   _model->appendRow(row1);
    //
    //   QList<QStandardItem*> row2;
    //   row2 << new QStandardItem("李四")
    //        << new QStandardItem("32")
    //        << new QStandardItem("设计师");
    //   _model->appendRow(row2);
    //
    //   QList<QStandardItem*> row3;
    //   row3 << new QStandardItem("王五")
    //        << new QStandardItem("25")
    //        << new QStandardItem("测试工程师");
    //   _model->appendRow(row3);
    //
    //   注意：每个 QStandardItem 是 new 出来的，但不需要你 delete
    //         model 会接管它们的内存（类似对象树）
    QList<QStandardItem*>row1;
    row1 << new QStandardItem("张三")
         << new QStandardItem("28")
         << new QStandardItem("工程师");
    _model->appendRow(row1);

    QList<QStandardItem*>row2;
    row2 << new QStandardItem("李四")
         << new QStandardItem("32")
         << new QStandardItem("设计师");
    _model->appendRow(row2);

    QList<QStandardItem*>row3;
    row3 << new QStandardItem("王五")
         << new QStandardItem("25")
         << new QStandardItem("测试工程师");
    _model->appendRow(row3);

    // TODO(5): 创建 TableView 并绑定 Model
    //   _tableView = new QTableView(this);
    //   _tableView->setModel(_model);
    //
    //   就这一行 setModel()，View 就知道该显示什么数据了。
    //   之后你修改 model 的数据 → View 自动刷新显示。
    //
    //   可选设置：
    //   _tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    //   // 点击时选中整行，而不是单个单元格
    //   _tableView->horizontalHeader()->setStretchLastSection(true);
    //   // 最后一列自动拉伸填满宽度
    //   // 需要 #include <QHeaderView>

    _tableView = new QTableView(this);
    _tableView->setModel(_model);
    _tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    _tableView->horizontalHeader()->setStretchLastSection(true);

    // TODO(6): 创建按钮
    //   _btnAdd = new QPushButton("添加行", this);
    //   _btnRemove = new QPushButton("删除行", this);
    //   _btnModify = new QPushButton("修改数据", this);
    _btnAdd = new QPushButton("添加行",this);
    _btnRemove = new QPushButton("删除行",this);
    _btnModify = new QPushButton("修改数据",this);


    // TODO(7): 布局
    //   QVBoxLayout *mainLayout = new QVBoxLayout(this);
    //   mainLayout->addWidget(_tableView);
    //
    //   QHBoxLayout *btnLayout = new QHBoxLayout();
    //   btnLayout->addWidget(_btnAdd);
    //   btnLayout->addWidget(_btnRemove);
    //   btnLayout->addWidget(_btnModify);
    //   mainLayout->addLayout(btnLayout);

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->addWidget(_tableView);
    
    QHBoxLayout *btnLayout = new QHBoxLayout();
    btnLayout->addWidget(_btnAdd);
    btnLayout->addWidget(_btnRemove);
    btnLayout->addWidget(_btnModify);
    mainLayout->addLayout(btnLayout);


    // TODO(8): 连接信号槽
    //   connect(_btnAdd, &QPushButton::clicked, this, &Widget::onAddRow);
    //   connect(_btnRemove, &QPushButton::clicked, this, &Widget::onRemoveRow);
    //   connect(_btnModify, &QPushButton::clicked, this, &Widget::onModifyData);
    connect(_btnAdd, &QPushButton::clicked,this,&Widget::onAddRow);
    connect(_btnRemove, &QPushButton::clicked,this,&Widget::onRemoveRow);
    connect(_btnModify, &QPushButton::clicked,this,&Widget::onModifyData);

    setWindowTitle("Model/View 练习");
    resize(500, 350);
}

Widget::~Widget() {}

// TODO(9): 实现 onAddRow — 添加一行新数据
//
//   void Widget::onAddRow() {
//       QList<QStandardItem*> newRow;
//       newRow << new QStandardItem("新员工")
//              << new QStandardItem("0")
//              << new QStandardItem("未分配");
//       _model->appendRow(newRow);
//       // 添加后 View 自动显示新行，不需要手动刷新
//   }
void Widget::onAddRow(){
    QList<QStandardItem*> newRow;
    newRow << new QStandardItem("新员工")
            << new QStandardItem("0")
            << new QStandardItem("未分配");
    _model->appendRow(newRow);
}

// TODO(10): 实现 onRemoveRow — 删除选中行
//
//   void Widget::onRemoveRow() {
//       QModelIndex index = _tableView->currentIndex();
//       // currentIndex() 返回当前选中的单元格的"坐标"（QModelIndex）
//       //   index.row() = 行号
//       //   index.column() = 列号
//       //   index.isValid() = 是否有选中
//
//       if (index.isValid()) {
//           _model->removeRow(index.row());
//       }
//   }
void Widget::onRemoveRow(){
    QModelIndex index = _tableView->currentIndex();
    if(index.isValid()){
        _model->removeRow(index.row());
    }
}

// TODO(11): 实现 onModifyData — 修改选中单元格的数据
//
//   void Widget::onModifyData() {
//       QModelIndex index = _tableView->currentIndex();
//       if (index.isValid()) {
//           // 方式1：通过 model 修改
//           _model->setData(index, "已修改");
//
//           // 方式2：通过 item 修改
//           // QStandardItem *item = _model->itemFromIndex(index);
//           // item->setText("已修改");
//
//           // 两种方式等价，View 都会自动更新显示
//       }
//   }

void Widget::onModifyData(){
    QModelIndex index = _tableView->currentIndex();
    if(index.isValid()){
        _model->setData(index,"已修改");
    }
}

// ============================================================
// Part 2（选做）：自定义 Model
//
// 如果你想理解 Model 的底层机制，可以创建一个新文件：
//   mymodel.h / mymodel.cpp
//
// 需要继承 QAbstractTableModel 并重写以下纯虚函数：
//   int rowCount(const QModelIndex &parent) const override;
//   int columnCount(const QModelIndex &parent) const override;
//   QVariant data(const QModelIndex &index, int role) const override;
//
// 可选重写（支持编辑）：
//   bool setData(const QModelIndex &index, const QVariant &value, int role) override;
//   Qt::ItemFlags flags(const QModelIndex &index) const override;
//   QVariant headerData(int section, Qt::Orientation, int role) const override;
//
// 自定义 Model 的优势：
//   - 数据存在你自己的结构体/容器中（如 QVector<Employee>）
//   - 不需要为每个单元格创建 QStandardItem 对象
//   - 数据量大时性能更好
//   - 可以对接数据库、文件、网络等数据源
// ============================================================