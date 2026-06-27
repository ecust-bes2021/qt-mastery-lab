#include <QCoreApplication>
#include <QFile>
#include <QTextStream>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QDataStream>
#include <QProcess>
#include <QDebug>

// ============================================================
// 文件与序列化 + 进程调用 综合练习
//
// 不需要事件循环，所以直接在 main 里写完就 return
// ============================================================

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    qDebug() << "===== #8 文件与序列化 + #9 进程调用 练习 =====\n";

    // ────────────────────────────────────────────────
    // Part 1: QFile + QTextStream（文本文件读写）
    // ────────────────────────────────────────────────

    // TODO(1): 写一个文本文件
    //
    //   QFile file("test_output.txt");
    //   if (file.open(打开模式)) {
    //       QTextStream out(&file);     // 用 QTextStream 包装 QFile
    //       out << "chipModel=STM32F103\n";
    //       out << "baudRate=115200\n";
    //       out << "port=COM3\n";
    //       file.close();
    //   }
    //
    //   打开模式：QIODevice::WriteOnly | QIODevice::Text
    //     - WriteOnly = 只写（如果文件存在会覆盖）
    //     - Text = 文本模式（Windows 下自动处理 \r\n 换行）
    //
    //   QTextStream 的作用：把 QString 转成字节写入文件
    //   类似 C++ 的 ofstream，用 << 运算符写入
     QFile file("test_output.txt");
     if(file.open(QIODevice::WriteOnly | QIODevice::Text)){
        QTextStream out(&file);
        out << "chipModel=STM32f103\n";
        out << "baudRate=115200\n";
        out << "port=COM3\n";
        file.close();

     }
    


    // TODO(2): 读回这个文本文件
    //
    //   if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    //       QTextStream in(&file);
    //       while (!in.atEnd()) {            // atEnd() = 是否读到文件末尾
    //           QString line = in.readLine(); // readLine() = 读一行（不包含换行符）
    //           qDebug() << line;
    //       }
    //       file.close();
    //   }
    //
    //   注意：file 对象可以复用（同一个 QFile 关闭后重新 open）
    //   ReadOnly = 只读模式
    if(file.open(QIODevice::ReadOnly | QIODevice::Text)){
        QTextStream in(&file);
        while(!in.atEnd()){
            QString line = in.readLine();
            qDebug() << line;
        }
        file.close();
    }


    qDebug() << "\n";

    // ────────────────────────────────────────────────
    // Part 2: JSON 读写
    // ────────────────────────────────────────────────

    // TODO(3): 写 JSON 文件
    //
    //   QJsonObject obj;
    //   obj["chipModel"] = "STM32F103";      // 字符串值
    //   obj["baudRate"] = 115200;             // 整数值
    //   obj["port"] = "COM3";
    //
    //   QJsonArray arr;                       // JSON 数组
    //   arr.append(1);
    //   arr.append(3);
    //   arr.append(5);
    //   arr.append(7);
    //   obj["testItems"] = arr;               // 把数组放进对象
    //
    //   QJsonDocument doc(obj);               // 用 QJsonDocument 包装
    //
    //   QFile jsonFile("config.json");
    //   if (jsonFile.open(QIODevice::WriteOnly)) {
    //       jsonFile.write(doc.toJson());     // toJson() 转成 UTF-8 文本
    //       jsonFile.close();
    //   }
    //
    //   QJsonObject 用 [] 设值，类似 Python 的 dict
    //   QJsonArray 用 append 添加元素，类似 Python 的 list
    //   toJson() 默认是格式化输出（带缩进），toJson(QJsonDocument::Compact) 是紧凑输出
    QJsonObject obj;
    obj["chipModel"] = "STM32F103";
    obj["baudeRate"] = 115200;
    obj["port"] = "COM3";

    QJsonArray arr;
    arr.append(1);
    arr.append(3);
    arr.append(5);
    arr.append(7);
    obj["testItems"] = arr;
    QJsonDocument doc(obj);
    QFile jsonFile("config.json");
    if(jsonFile.open(QIODevice::WriteOnly)){
        jsonFile.write(doc.toJson());
        jsonFile.close();
    }

    // TODO(4): 读 JSON 文件
    //
    //   QFile jsonReadFile("config.json");
    //   if (jsonReadFile.open(QIODevice::ReadOnly)) {
    //       QByteArray data = jsonReadFile.readAll();    // 一次性读完整个文件
    //       jsonReadFile.close();
    //
    //       QJsonDocument doc = QJsonDocument::fromJson(data);  // 解析 JSON
    //       QJsonObject root = doc.object();                     // 获取根对象
    //
    //       qDebug() << "chipModel:" << root["chipModel"].toString();
    //       qDebug() << "baudRate:" << root["baudRate"].toInt();
    //       qDebug() << "port:" << root["port"].toString();
    //
    //       QJsonArray items = root["testItems"].toArray();      // 获取数组
    //       for (int i = 0; i < items.size(); ++i) {
    //           qDebug() << "testItem:" << items[i].toInt();
    //       }
    //   }
    //
    //   readAll() 返回 QByteArray（原始字节），不是 QString
    //   fromJson() 把字节解析成 QJsonDocument
    //   取值时需要调 toString()/toInt()/toArray() 等转换函数（跟 QVariant 类似）
    QFile jsonReadFile("config.json");
    if(jsonReadFile.open(QIODevice::ReadOnly)){
        QByteArray data = jsonReadFile.readAll();
        jsonReadFile.close();

        QJsonDocument doc = QJsonDocument::fromJson(data);
        QJsonObject root = doc.object();
        qDebug() << "chipModel" <<root["chipModel"].toString();
        qDebug() << "baudeRate" <<root["baudRate"].toInt();

        QJsonArray items = root["testItems"].toArray();
    }
    


    qDebug() << "\n";

    // ────────────────────────────────────────────────
    // Part 3: QDataStream（二进制序列化）
    // ────────────────────────────────────────────────

    // TODO(5): 二进制写入
    //
    //   QFile binFile("data.dat");
    //   if (binFile.open(QIODevice::WriteOnly)) {
    //       QDataStream out(&binFile);         // 用 QDataStream 包装 QFile
    //       out << QString("张三");             // 写 QString（自动序列化：长度+内容）
    //       out << (qint32)28;                  // 写 int（固定 4 字节）
    //       out << QString("工程师");
    //       binFile.close();
    //   }
    //
    //   QDataStream 用 << 写入，跟 QTextStream 类似
    //   区别：QTextStream 写文本，QDataStream 写二进制
    //   qint32 是 Qt 定义的固定 32 位整数（跨平台大小一致）


    // TODO(6): 二进制读取
    //
    //   if (binFile.open(QIODevice::ReadOnly)) {
    //       QDataStream in(&binFile);
    //       QString name;
    //       qint32 age;
    //       QString position;
    //       in >> name >> age >> position;     // 顺序必须跟写的时候一致！
    //       binFile.close();
    //
    //       qDebug() << "姓名:" << name;
    //       qDebug() << "年龄:" << age;
    //       qDebug() << "职位:" << position;
    //   }
    //
    //   读的顺序必须跟写的完全一致：
    //     写：QString, qint32, QString
    //     读：QString, qint32, QString
    //   如果顺序错了或类型错了 → 数据全部乱掉


    qDebug() << "\n";

    // ────────────────────────────────────────────────
    // Part 4: QProcess（调用外部程序）
    // ────────────────────────────────────────────────

    // TODO(7): 阻塞方式调用外部命令
    //
    //   QProcess process;
    //   process.start("ping", QStringList() << "-n" << "1" << "127.0.0.1");
    //   // start(程序名, 参数列表)
    //   //   "ping" = 要执行的外部程序
    //   //   QStringList() << "-n" << "1" << "127.0.0.1" = 命令行参数
    //   //   等价于命令行：ping -n 1 127.0.0.1
    //
    //   process.waitForFinished();     // 阻塞等待外部程序执行完
    //
    //   QString output = process.readAllStandardOutput();  // 读取 stdout
    //   qDebug() << "ping 输出:" << output;
    //   qDebug() << "退出码:" << process.exitCode();       // 0 = 成功
    //
    //   QProcess 在栈上创建即可（不需要 new）
    //   waitForFinished() 会阻塞当前线程，所以只适合控制台程序或子线程
    //   在 UI 程序的主线程中不要用 waitForFinished（会卡界面）
    //   UI 程序应该用信号 readyReadStandardOutput + finished 异步处理

    QProcess process;
    process.start("ping", QStringList() << "-n" <<"1" << "127.0.0.1");
    process.waitForFinished();
    QString output = process.readAllStandardOutput();
    qDebug() << "ping 输出：" << output;
    qDebug() << "退出码：" << process.exitCode();


    qDebug() << "\n===== 练习完成 =====";

    return 0;
}