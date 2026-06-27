#ifndef LEDINDICATOR_H
#define LEDINDICATOR_H

#include <QWidget>

class LedIndicator : public QWidget
{
    Q_OBJECT

public:
    // TODO(1): 定义枚举 State，包含三种状态：Off(灰), On(绿), Error(红)
    //  提示：enum State { Off, On, Error };
    enum State {
        Off,
        On,
        Error
    };


    // TODO(2): 构造函数，接收 parent 指针，默认 nullptr
    //  提示：explicit LedIndicator(QWidget *parent = nullptr);
    explicit LedIndicator(QWidget *parent = nullptr);


    // TODO(3): setState 方法 —— 设置 LED 状态
    //  参数：State s
    //  返回：void
    //  提示：内部保存状态后调用 update() 请求重绘
    void setState(State s);


    // TODO(4): setLabel 方法 —— 设置下方文字标签
    //  参数：const QString &text
    //  返回：void
    //  提示：内部保存文字后调用 update() 请求重绘
    void setLabel(const QString &text);


    // TODO(5): 重写 sizeHint —— 返回控件的理想尺寸
    //  提示：QSize sizeHint() const override;
    //  建议返回 QSize(60, 80)，60宽 = LED圆直径留余量，80高 = 圆 + 文字
    QSize sizeHint() const override;


signals:
    // TODO(6): clicked 信号 —— 用户点击时发射
    //  提示：void clicked();
    void clicked();


protected:
    // TODO(7): 重写 paintEvent —— 自绘 LED 圆形 + 文字
    //  提示：void paintEvent(QPaintEvent *event) override;
    void paintEvent(QPaintEvent *event) override;


    // TODO(8): 重写 mousePressEvent —— 捕获鼠标点击，发射 clicked 信号
    //  提示：void mousePressEvent(QMouseEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;


private:
    // TODO(9): 声明两个私有成员变量
    //  _state：类型 State，保存当前 LED 状态，默认 Off
    //  _label：类型 QString，保存文字标签，默认空
    //  提示：
    //    State _state = Off;
    //    QString _label;
    State _state = Off;
    QString _label;

};

#endif // LEDINDICATOR_H