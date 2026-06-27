#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QThread>
// #include <QString>

class Worker;

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

    // TODO(1): 声明槽函数
    //   void onStart();    // 点击"开始"按钮
    //   void onStop();     // 点击"停止"按钮
    //   void onProgressChanged(int value);  // 收到 Worker 的进度信号
    //   void onWorkerFinished();            // Worker 完成后的清理

private slots:
    void onStart();
    void onStop();
    void onProgressChanged(int value);
    void onWorkerFinished();

private:
    // TODO(2): 声明 UI 控件
    //   QPushButton *_btnStart;
    //   QPushButton *_btnStop;
    //   QLabel *_labelStatus;
    //   QLabel *_labelThread;

    QPushButton *_btnStart;
    QPushButton *_btnStop;
    QLabel *_labelStatus;
    QLabel *_labelThread;

    // TODO(3): 声明线程相关成员
    //   QThread *_thread;    // 子线程对象
    //   Worker *_worker;     // 工作对象（会被移入子线程）
    //
    //   注意：
    //   - _thread 可以挂到 this（有 parent，会被对象树管理）
    //   - _worker 不能有 parent（moveToThread 的要求）
    //   - _worker 的生命周期通过 deleteLater 管理

    QThread *_thread;
    Worker *_worker;
};
#endif // WIDGET_H