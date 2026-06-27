#include "widget.h"
#include "ledindicator.h"
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QDebug>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    // TODO(1): 创建 LedIndicator 控件
    //  - new LedIndicator(this)
    //  - 调用 setLabel("电源") 设置初始标签
    //
    //  提示：
    //    _led = new LedIndicator(this);
    //    _led->setLabel("电源");
    _led = new LedIndicator(this);
    _led->setLabel("电源");


    // TODO(2): 创建两个 QPushButton
    //  - _btnToggle：文字 "开关切换"
    //  - _btnError：文字 "模拟故障"
    //
    //  提示：
    //    _btnToggle = new QPushButton("开关切换", this);
    //    _btnError  = new QPushButton("模拟故障", this);
    _btnToggle = new QPushButton("开关切换", this);
    _btnError  = new QPushButton("模拟故障", this);


    // TODO(3): 布局 —— 垂直布局包含 LED + 水平按钮行
    //  步骤：
    //  3a. 创建水平布局 btnLayout，添加两个按钮
    //       auto *btnLayout = new QHBoxLayout;
    //       btnLayout->addWidget(_btnToggle);
    //       btnLayout->addWidget(_btnError);
    //
    //  3b. 创建垂直主布局，添加 LED 控件 + 按钮布局
    //       auto *mainLayout = new QVBoxLayout(this);
    //       mainLayout->addWidget(_led, 0, Qt::AlignCenter);  // LED 居中
    //       mainLayout->addLayout(btnLayout);
    auto *btnLayout = new QHBoxLayout;
    btnLayout->addWidget(_btnToggle);
    btnLayout->addWidget(_btnError);

    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->addWidget(_led, 0, Qt::AlignCenter);
    mainLayout->addLayout(btnLayout);


    // TODO(4): 连接信号与槽 —— 3 条 connect
    //  4a. _btnToggle 的 clicked → this 的 onToggle
    //  4b. _btnError  的 clicked → this 的 onSetError
    //  4c. _led       的 clicked → this 的 onLedClicked
    //
    //  提示：
    //    connect(_btnToggle, &QPushButton::clicked, this, &Widget::onToggle);
    //    connect(_btnError,  &QPushButton::clicked, this, &Widget::onSetError);
    //    connect(_led, &LedIndicator::clicked, this, &Widget::onLedClicked);
    connect(_btnToggle, &QPushButton::clicked, this, &Widget::onToggle);
    connect(_btnError,  &QPushButton::clicked, this, &Widget::onSetError);
    connect(_led, &LedIndicator::clicked, this, &Widget::onLedClicked);


    // TODO(5): 设置窗口标题和初始大小
    //  提示：
    //    setWindowTitle("LED 指示灯 - 自定义控件练习");
    //    resize(300, 250);
    setWindowTitle("LED 指示灯 - 自定义控件练习");
    resize(300, 250);

    _isOn = false;
}

Widget::~Widget() {}

// TODO(6): onToggle 实现
//  - 每次调用切换 _isOn 状态（true↔false）
//  - 根据 _isOn 调用 _led->setState()：
//      true  → LedIndicator::On
//      false → LedIndicator::Off
//
//  提示：
//    void Widget::onToggle()
//    {
//        _isOn = !_isOn;
//        _led->setState(_isOn ? LedIndicator::On : LedIndicator::Off);
//    }
void Widget::onToggle()
{
    _isOn = !_isOn;
    _led->setState(_isOn ? LedIndicator::On : LedIndicator::Off);
}


// TODO(7): onSetError 实现
//  - 调用 _led->setState(LedIndicator::Error)
//  - 同时将 _isOn 设为 false（错误状态不算"开"）
//
//  提示：
//    void Widget::onSetError()
//    {
//        _led->setState(LedIndicator::Error);
//        _isOn = false;
//    }
void Widget::onSetError()
{
    _led->setState(LedIndicator::Error);
    _isOn = false;
}


// TODO(8): onLedClicked 实现
//  - 使用 qDebug() 输出一条消息："LED 被点击了！"
//  - 这里主要演示自定义控件的信号能被外部 connect
//
//  提示：
//    void Widget::onLedClicked()
//    {
//        qDebug() << "LED 被点击了！";
//    }
void Widget::onLedClicked()
{
    qDebug() << "LED 被点击了！";
}