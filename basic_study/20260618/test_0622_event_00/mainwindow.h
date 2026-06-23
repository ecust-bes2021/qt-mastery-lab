#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QMouseEvent>
#include <QKeyEvent>

// ============================================================
// 事件系统练习
//
// 目标：理解 Qt 事件机制
//   - 事件 vs 信号的区别
//   - 虚函数重写（override）
//   - 事件过滤器（eventFilter）
//
// 背景知识：
//   Qt 中有两套通知机制：
//   1. 信号槽 —— 对象间通信（高层、业务逻辑）
//   2. 事件   —— 系统底层输入（鼠标、键盘、窗口、定时器等）
//
//   事件的处理流程：
//   OS 产生事件 → QApplication::exec() 事件循环取出
//   → QObject::event() 分发 → 具体的 xxxEvent() 虚函数
//
//   你要做的就是"重写"这些虚函数，插入你的处理逻辑。
// ============================================================

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    // TODO(1): 重写鼠标按下事件
    //   void mousePressEvent(QMouseEvent *event) override;
    //
    //   当用户在窗口内点击鼠标时，Qt 会调用这个函数。
    //   参数 event 包含：点击位置、哪个按键、修饰键等信息。
    //
    //   关键字解释：
    //   - protected: 这个函数不需要外部调用，只被 Qt 框架内部调用
    //   - override: 告诉编译器"我在重写父类的虚函数"，拼错名字会报错（安全网）
    //   - QMouseEvent *event: 事件对象指针，包含事件详情
    void mousePressEvent(QMouseEvent *event) override;

    // TODO(2): 重写鼠标移动事件
    //   void mouseMoveEvent(QMouseEvent *event) override;
    //
    //   默认只在按住鼠标时触发。
    //   如果想不按也触发，需要 setMouseTracking(true);
    void mouseMoveEvent(QMouseEvent *event) override;

    // TODO(3): 重写键盘按下事件
    //   void keyPressEvent(QKeyEvent *event) override;
    //
    //   当窗口有焦点时，按键会触发这个函数。
    //   event->key() 返回按键码（如 Qt::Key_A）
    //   event->text() 返回按键对应的字符
    void keyPressEvent(QKeyEvent *event) override;

    // TODO(4): 重写事件过滤器
    //   bool eventFilter(QObject *watched, QEvent *event) override;
    //
    //   事件过滤器可以拦截其他对象的事件（不需要子类化那个对象）。
    //   返回 true = 事件被你吃掉了，不再传递
    //   返回 false = 正常传递，你只是"偷看"了一下
    //
    //   使用方式：
    //   在构造函数中调用 someWidget->installEventFilter(this);
    //   然后这个函数就会收到 someWidget 的所有事件。
    bool eventFilter(QObject *watched, QEvent *event) override;

private:
    // TODO(5): 声明成员变量
    //   QLabel *_labelMouse;       — 显示鼠标事件信息
    //   QLabel *_labelKey;         — 显示键盘事件信息
    //   QLabel *_labelFilter;      — 显示事件过滤器拦截的信息
    //   QPushButton *_btn;         — 用于演示事件过滤器（拦截它的事件）
    QLabel *_labelMouse;
    QLabel *_labelKey;
    QLabel *_labelFilter;
    QPushButton *_btn;
};

#endif // MAINWINDOW_H