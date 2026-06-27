#ifndef WORKER_H
#define WORKER_H

#include <QObject>
#include <QThread>
#include <QAtomicInteger>

// ============================================================
// Worker 类（在子线程中执行耗时任务）
//
// 核心规则：
//   1. Worker 继承 QObject，但创建时 parent = nullptr
//      （因为 moveToThread 要求对象不能有 parent）
//   2. Worker 本身不创建线程，它只是"被移入"线程的工作对象
//   3. 通过信号与 UI 线程通信（跨线程信号自动走队列连接）
//
// 设计模式对比（PySide6 vs C++）：
//   PySide6:  worker = Worker()
//             worker.moveToThread(thread)
//   C++:      Worker *worker = new Worker();    // 无 parent！
//             worker->moveToThread(thread);
//
//   关键区别：C++ 中 worker 没有 parent，不会被对象树自动 delete
//             必须手动安排 deleteLater 清理
// ============================================================

class Worker : public QObject
{
    Q_OBJECT

public:
    explicit Worker(QObject *parent = nullptr);//moveToThread要求对象不能有parent

    // TODO(W1): 声明停止标志
    //   用于线程安全地通知 Worker 停止工作
    //
    //   void requestStop();
    //   bool isStopRequested() const;
    //
    //   为什么用 QAtomicInteger<bool> 而不是普通 bool？
    //   因为 requestStop() 在 UI 线程调用，doWork() 在子线程运行
    //   普通 bool 跨线程读写 = 数据竞争 = 未定义行为
    //   QAtomicInteger 保证原子操作，无需加锁

    void requestStop();
    bool isStopRequested() const;

public slots:
    // TODO(W2): 声明工作槽函数
    //   这个函数会在子线程中执行（因为 Worker 被 moveToThread 了）
    //
    //   void doWork();
    //   内部逻辑：
    //     循环 10 次（模拟耗时任务）
    //     每次循环：
    //       1. 检查 isStopRequested()，如果是就提前退出
    //       2. QThread::sleep(1) 模拟耗时操作
    //       3. emit progressChanged(i) 报告进度
    //     循环结束后 emit finished()

    void doWork();

signals:
    // TODO(W3): 声明信号
    //   void progressChanged(int value);   // 进度更新（0~10）
    //   void finished();                    // 工作完成

    void progressChanged(int value);
    void finished();

private:
    QAtomicInteger<bool> _stopFlag;
};

#endif // WORKER_H