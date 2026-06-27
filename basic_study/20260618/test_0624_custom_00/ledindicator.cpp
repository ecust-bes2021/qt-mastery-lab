#include "ledindicator.h"
#include <QPainter>
#include <QMouseEvent>

// TODO(1): 构造函数实现
//  - 初始化列表：调用父类 QWidget(parent)，_state 初始化为 Off
//  - 函数体可以为空（布局和外观由 paintEvent 决定）
//
//  提示：
//    LedIndicator::LedIndicator(QWidget *parent)
//        : QWidget(parent), _state(Off)
//    {}
LedIndicator::LedIndicator(QWidget *parent)
    : QWidget(parent), _state(Off)
{}


// TODO(2): setState 实现
//  - 保存参数到 _state
//  - 调用 update() 请求重绘（不要直接调 paintEvent！）
//
//  提示：
//    void LedIndicator::setState(State s)
//    {
//        _state = s;
//        update();
//    }
void LedIndicator::setState(State s)
{
    _state = s;
    update();
}


// TODO(3): setLabel 实现
//  - 保存参数到 _label
//  - 调用 update() 请求重绘
//
//  提示：和 setState 结构一样
void LedIndicator::setLabel(const QString &text)
{
    _label = text;
    update();
}


// TODO(4): sizeHint 实现
//  - 返回 QSize(60, 80)
//  - 这个尺寸是建议值，布局系统会参考它来分配空间
//
//  提示：
//    QSize LedIndicator::sizeHint() const
//    {
//        return QSize(60, 80);
//    }
QSize LedIndicator::sizeHint() const
{
    return QSize(60, 80);
}


// TODO(5): paintEvent 实现 —— 核心绘制逻辑
//  这是自定义控件最重要的部分！
//
//  步骤：
//  5a. 创建 QPainter，绑定到 this
//       QPainter painter(this);
//       painter.setRenderHint(QPainter::Antialiasing);  // 开启抗锯齿
//
//  5b. 根据 _state 选择颜色
//       QColor color;
//       用 switch(_state) 选择：
//         Off   → QColor(160, 160, 160)   // 灰色
//         On    → QColor(0, 200, 0)       // 绿色
//         Error → QColor(220, 0, 0)       // 红色
//
//  5c. 计算 LED 圆的位置和大小
//       int diameter = qMin(width(), height() - 20);  // 留20像素给文字
//       int x = (width() - diameter) / 2;             // 水平居中
//       int y = 0;                                    // 顶部对齐
//       QRect ledRect(x, y, diameter, diameter);
//
//  5d. 绘制圆形 LED
//       painter.setBrush(color);                      // 填充色
//       painter.setPen(Qt::black);                    // 边框色
//       painter.drawEllipse(ledRect);                 // 画圆
//
//  5e. 绘制文字标签（在圆下方）
//       QRect textRect(0, diameter + 2, width(), 18); // 文字区域
//       painter.setPen(Qt::black);
//       painter.drawText(textRect, Qt::AlignCenter, _label);
void LedIndicator::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    QColor color;
    switch (_state) {
    case Off:
        color = QColor(160, 160, 160);
        break;
    case On:
        color = QColor(0, 200, 0);
        break;
    case Error:
        color = QColor(220, 0, 0);
        break;
    }

    int diameter = qMin(width(), height() - 20);
    int x = (width() - diameter) / 2;
    int y = 0;
    QRect ledRect(x, y, diameter, diameter);

    painter.setBrush(color);
    painter.setPen(Qt::black);
    painter.drawEllipse(ledRect);

    QRect textRect(0, diameter + 2, width(), 18);
    painter.setPen(Qt::black);
    painter.drawText(textRect, Qt::AlignCenter, _label);
}


// TODO(6): mousePressEvent 实现
//  - 发射 clicked() 信号
//  - 调用父类的 mousePressEvent（保持事件链）
//
//  提示：
//    void LedIndicator::mousePressEvent(QMouseEvent *event)
//    {
//        emit clicked();
//        QWidget::mousePressEvent(event);
//    }
void LedIndicator::mousePressEvent(QMouseEvent *event)
{
    emit clicked();
    qDebug() << "测试clicekd信号";
    QWidget::mousePressEvent(event);
}