#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

// TODO(1): 前向声明 LedIndicator 和 QPushButton
//  提示：不需要 include 头文件，这里只用指针，前向声明即可
//    class LedIndicator;
//    class QPushButton;

class LedIndicator;
class QPushButton;


class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

// TODO(2): 声明三个 private slots 槽函数
//  - onToggle()    —— 切换 LED 开/关状态
//  - onSetError()  —— 将 LED 设为错误状态
//  - onLedClicked() —— LED 被点击时的响应
//
//  提示：
//    private slots:
//        void onToggle();
//        void onSetError();
//        void onLedClicked();
private slots:
    void onToggle();
    void onSetError();
    void onLedClicked();



// TODO(3): 声明私有成员变量
//  - LedIndicator *_led;
//  - QPushButton  *_btnToggle;
//  - QPushButton  *_btnError;
//  - bool          _isOn;    // 记录当前 LED 是否为 On 状态
//
//  提示：
//    private:
//        LedIndicator *_led;
//        QPushButton  *_btnToggle;
//        QPushButton  *_btnError;
//        bool          _isOn = false;
private:
    LedIndicator *_led;
    QPushButton *_btnToggle;
    QPushButton *_btnError;
    bool _isOn = false;

};
#endif // WIDGET_H