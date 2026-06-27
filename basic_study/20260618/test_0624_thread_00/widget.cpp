#include "widget.h"
#include "worker.h"
#include <QDebug>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , _thread(nullptr)
    , _worker(nullptr)
{
    // TODO(4): 创建 UI 控件
    //   _labelStatus = new QLabel("状态：就绪", this);
    //   _labelThread = new QLabel("主线程ID: " + QString::number((quint64)QThread::currentThreadId()), this);
    //   _btnStart = new QPushButton("开始", this);
    //   _btnStop = new QPushButton("停止", this);
    //   _btnStop->setEnabled(false);   // 初始时停止按钮不可用

    _labelStatus = new QLabel("状态: 就绪",this);
    _labelThread = new QLabel("主线程ID: "+ QString::number((quint64)QThread::currentThreadId()),this);
    _btnStart = new QPushButton("开始", this);
    _btnStop = new QPushButton("停止", this);
    _btnStop->setEnabled(false);


    // TODO(5): 布局
    //   QVBoxLayout *layout = new QVBoxLayout(this);
    //   layout->addWidget(_labelThread);
    //   layout->addWidget(_labelStatus);
    //   layout->addWidget(_btnStart);
    //   layout->addWidget(_btnStop);
    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->addWidget(_labelThread);
    layout->addWidget(_labelStatus);
    layout->addWidget(_btnStart);
    layout->addWidget(_btnStop);


    // TODO(6): 连接按钮信号
    //   connect(_btnStart, &QPushButton::clicked, this, &Widget::onStart);
    //   connect(_btnStop, &QPushButton::clicked, this, &Widget::onStop);
    connect(_btnStart, &QPushButton::clicked, this, &Widget::onStart);
    connect(_btnStop, &QPushButton::clicked, this, &Widget::onStop);


    setWindowTitle("多线程练习 - QThread + Worker");
    resize(350, 200);
}

Widget::~Widget()
{
    // TODO(7): 析构时安全清理线程
    //
    //   if (_thread && _thread->isRunning()) {
    //       _worker->requestStop();   // 通知 Worker 停止
    //       _thread->quit();          // 请求线程事件循环退出
    //       _thread->wait();          // 阻塞等待线程真正结束
    //   }
    //
    //   为什么需要 wait()？
    //   quit() 只是"请求"退出，线程可能还在执行最后一次循环
    //   wait() 确保线程完全停止后，才继续析构（避免悬空指针）
    //
    //   如果不 wait() 就析构 → Worker 还在跑 → 访问已销毁的对象 → 崩溃
    if(_thread && _thread->isRunning()){
        _worker->requestStop();
        _thread->quit();
        _thread->wait();
    }

}

// TODO(8): 实现 onStart — 创建线程 + Worker + 建立连接 + 启动
//
//   void Widget::onStart() {
//       // 第一步：创建线程和 Worker
//       _thread = new QThread(this);       // 有 parent，挂到对象树
//       _worker = new Worker();            // 无 parent！重要！
//
//       // 第二步：把 Worker 移入子线程
//       _worker->moveToThread(_thread);
//       // 从此刻起，Worker 的槽函数都会在 _thread 中执行
//
//       // 第三步：建立信号连接链
//       //   线程启动 → Worker 开始工作
//       connect(_thread, &QThread::started, _worker, &Worker::doWork);
//
//       //   Worker 报告进度 → UI 更新
//       connect(_worker, &Worker::progressChanged, this, &Widget::onProgressChanged);
//
//       //   Worker 完成 → 清理流程
//       connect(_worker, &Worker::finished, this, &Widget::onWorkerFinished);
//
//       //   Worker 完成 → Worker 自我销毁（deleteLater 安全删除）
//       connect(_worker, &Worker::finished, _worker, &Worker::deleteLater);
//
//       //   线程结束 → 线程对象自我销毁
//       connect(_thread, &QThread::finished, _thread, &QThread::deleteLater);
//
//       // 第四步：启动线程
//       _thread->start();
//
//       // 第五步：更新 UI 状态
//       _btnStart->setEnabled(false);
//       _btnStop->setEnabled(true);
//       _labelStatus->setText("状态：运行中...");
//
//       qDebug() << "主线程ID:" << QThread::currentThreadId();
//   }
//
//   信号连接链总结（这是固定模式，要记住）：
//   ┌─────────────────────────────────────────────────────┐
//   │  thread.started  →  worker.doWork()                 │
//   │  worker.progressChanged  →  widget.onProgress()     │
//   │  worker.finished  →  widget.onWorkerFinished()      │
//   │  worker.finished  →  worker.deleteLater()           │
//   │  thread.finished  →  thread.deleteLater()           │
//   └─────────────────────────────────────────────────────┘


// TODO(9): 实现 onStop — 请求停止
//
//   void Widget::onStop() {
//       if (_worker) {
//           _worker->requestStop();
//       }
//       _labelStatus->setText("状态：正在停止...");
//       _btnStop->setEnabled(false);
//   }

void Widget::onStop(){
    if(_worker){
        _worker->requestStop();
    }
    _labelStatus->setText("状态: 正在停止....");
    _btnStop->setEnabled(false);
}

// TODO(10): 实现 onProgressChanged — 更新 UI 显示
//
//   void Widget::onProgressChanged(int value) {
//       _labelStatus->setText(QString("状态：进度 %1/10").arg(value));
//   }

void Widget::onProgressChanged(int value){
    _labelStatus->setText(QString("状态：进度%1/10").arg(value));
}


// TODO(11): 实现 onWorkerFinished — 工作完成后的清理
//
//   void Widget::onWorkerFinished() {
//       _thread->quit();     // 请求线程事件循环退出
//       // 不需要 wait()，因为 deleteLater 会在事件循环退出后自动清理
//
//       _thread = nullptr;   // 指针置空（对象会被 deleteLater 删除）
//       _worker = nullptr;   // 同上
//
//       _btnStart->setEnabled(true);
//       _btnStop->setEnabled(false);
//       _labelStatus->setText("状态：已完成");
//
//       qDebug() << "清理完成";
//   }

void Widget::onWorkerFinished(){
    _thread->quit();

    _thread = nullptr;
    _worker = nullptr;

    _btnStart->setEnabled(true);
    _btnStop->setEnabled(false);
    _labelStatus->setText("状态: 已完成");

    qDebug() << "清理完成";
}

void Widget::onStart(){
    _thread = new QThread(this);
    _worker = new Worker();

    _worker->moveToThread(_thread);

    connect(_thread, &QThread::started,_worker,&Worker::doWork);

    connect(_worker, &Worker::progressChanged, this, &Widget::onProgressChanged);

    connect(_worker,&Worker::finished, this, &Widget::onWorkerFinished);

    connect(_worker, &Worker::finished, _worker,&Worker::deleteLater);

    connect(_thread, &QThread::finished, _thread, &QThread::deleteLater);

    _thread->start();

    _btnStart->setEnabled(false);
    _btnStop->setEnabled(true);
    _labelStatus->setText("状态：运行中...");

    qDebug() << "主线程ID: " << QThread::currentThreadId() ;


}
