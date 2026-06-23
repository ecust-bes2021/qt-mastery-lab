#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
{
    // TODO(2): 创建控件
    //   _labelTitle = new QLabel("布局练习", this);
    //   _labelTitle->setAlignment(Qt::AlignCenter);  // 居中
    //   _labelTitle->setStyleSheet("font-size: 20px; font-weight: bold;");
    //
    //   设置尺寸策略（SizePolicy）：
    //   _labelTitle->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    //   ↑ 水平：尽量填满宽度     ↑ 垂直：固定高度，不随窗口变大而变高
    //
    //   QSizePolicy 常用值：
    //   - Fixed:     固定大小，不能缩放
    //   - Expanding: 尽量占满剩余空间
    //   - Preferred: 默认大小（sizeHint），可以缩放
    //   - Minimum:   可以变大，不能比 sizeHint 小

    // TODO(3): 创建4个按钮（用于 Grid 布局演示）
    //   _btnA = new QPushButton("A", this);
    //   _btnB = new QPushButton("B", this);
    //   _btnC = new QPushButton("C", this);
    //   _btnD = new QPushButton("D", this);
    //
    //   给按钮设置 Expanding 策略，让它们随窗口等比缩放：
    //   _btnA->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    //   _btnB->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    //   _btnC->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    //   _btnD->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);

    // TODO(4): 创建底部按钮
    //   _btnOK = new QPushButton("确定", this);
    //   _btnCancel = new QPushButton("取消", this);

    // TODO(5): 创建 QGridLayout（网格布局）
    //   QGridLayout *gridLayout = new QGridLayout();
    //   gridLayout->addWidget(_btnA, 0, 0);    // 第0行, 第0列
    //   gridLayout->addWidget(_btnB, 0, 1);    // 第0行, 第1列
    //   gridLayout->addWidget(_btnC, 1, 0);    // 第1行, 第0列
    //   gridLayout->addWidget(_btnD, 1, 1);    // 第1行, 第1列
    //
    //   设置间距（spacing）— 按钮之间的距离：
    //   gridLayout->setSpacing(10);
    //   ↑ 所有按钮之间留10像素

    // TODO(6): 创建 QHBoxLayout（水平布局）用于底部栏
    //   QHBoxLayout *bottomLayout = new QHBoxLayout();
    //   bottomLayout->addWidget(_btnOK);
    //   bottomLayout->addStretch(1);           // ← 弹簧！
    //   bottomLayout->addWidget(_btnCancel);
    //
    //   addStretch(1) 效果：
    //   [确定] ←────弹性空白────→ [取消]
    //   窗口越宽，中间空白越大，两个按钮分居两端

    // TODO(7): 创建主布局 QVBoxLayout（垂直布局），嵌套组合
    //   QVBoxLayout *mainLayout = new QVBoxLayout(this);
    //   ↑ 传 this = 设置为本窗口的布局
    //
    //   mainLayout->addWidget(_labelTitle);        // 标题（stretch默认0，不抢空间）
    //   mainLayout->addLayout(gridLayout, 1);      // 网格区域，stretch=1（占满剩余）
    //   mainLayout->addLayout(bottomLayout);       // 底部栏（stretch默认0）
    //
    //   伸缩因子（stretch factor）解释：
    //   - stretch=0：不抢额外空间，保持自身最小尺寸
    //   - stretch=1：窗口变大时，多余空间全给这一块
    //   - 如果多个 stretch=1：按比例瓜分（1:1:1...）
    //
    //   设置外边距（contentsMargins）— 布局到窗口边缘的距离：
    //   mainLayout->setContentsMargins(15, 15, 15, 15);
    //   ↑ 左、上、右、下各留15像素
    //
    //   设置控件间距（spacing）— 标题/网格/底部栏之间的距离：
    //   mainLayout->setSpacing(12);

    setWindowTitle("布局练习");
    resize(300, 250);
}

MainWindow::~MainWindow() {}