#include "worker.h"
#include <QDebug>

Worker::Worker(QObject *parent)
    : QObject(parent)
    , _stopFlag(false)
{
}

// TODO(W1): 实现停止控制
//
//   void Worker::requestStop() {
//       _stopFlag.storeRelaxed(true);
//       // storeRelaxed = 原子写入，保证其他线程能看到新值
//       // "Relaxed" 表示不需要额外的内存屏障（对简单 bool 够用）
//   }
//
//   bool Worker::isStopRequested() const {
//       return _stopFlag.loadRelaxed();
//       // loadRelaxed = 原子读取
//   }
void Worker::requestStop(){
    _stopFlag.storeRelaxed(true);
}

bool Worker::isStopRequested()const{
    return _stopFlag.loadRelaxed();
}

// TODO(W2): 实现工作函数
//
//   void Worker::doWork() {
//       qDebug() << "Worker: 开始工作, 线程ID:" << QThread::currentThreadId();
//
//       for (int i = 1; i <= 10; ++i) {
//           if (isStopRequested()) {
//               qDebug() << "Worker: 收到停止请求，提前退出";
//               break;
//           }
//
//           QThread::sleep(1);   // 模拟耗时 1 秒
//           emit progressChanged(i);
//           qDebug() << "Worker: 进度" << i << "/10";
//       }
//
//       emit finished();
//       qDebug() << "Worker: 工作结束";
//   }
//
//   注意：
//   - QThread::sleep(1) 是让当前线程休眠，不是主线程！
//     因为 doWork 是在子线程中执行的（Worker 被 moveToThread 了）
//   - emit progressChanged(i) 会跨线程传到 UI，Qt 自动用队列连接
void Worker::doWork(){
    qDebug()<<"Worker: 开始工作，线程ID：" << QThread::currentThreadId();
    for (int i =1; i<= 10;++i){
        if(isStopRequested())
        {
            qDebug() << "Worker: 收到停止请求，提前退出";
            break;
        }
        QThread::sleep(1);
        emit progressChanged(i);
        qDebug() << "Worker: 进度"<< i<<"/10";
    }
    emit finished();
    qDebug() << "Worker: 工作结束";
}