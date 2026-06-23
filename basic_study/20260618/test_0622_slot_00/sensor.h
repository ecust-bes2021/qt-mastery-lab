#ifndef SENSOR_H
#define SENSOR_H

#include <QObject>
#include <QRandomGenerator>

// TODO(1): 创建 Sensor 类，继承 QObject
//
//   这个类模拟一个温度传感器：
//   - 每次调用 readTemperature() 时，随机生成一个温度值（15.0 ~ 45.0）
//   - 如果温度超过阈值（默认35.0），发射 overheated 信号
//   - 每次读取都发射 temperatureChanged 信号
//
//   你需要：
//   (a) 加 Q_OBJECT 宏
//   (b) 在 signals: 区域声明两个信号：
//       void temperatureChanged(double temp);   — 每次读取都发射
//       void overheated(double temp);           — 超温时发射
//
//       注意：C++ 中信号只声明，不写实现！MOC 会自动生成实现。
//
//   (c) 在 public slots: 区域声明：
//       void readTemperature();                 — 模拟读取温度
//
//   (d) 在 private: 区域声明：
//       double _threshold = 35.0;              — 报警阈值
//       double _currentTemp = 0.0;             — 当前温度
//
//   思考：为什么信号不需要写函数体？
//         signals: 和 slots: 在编译后到底变成了什么？
//         emit 是一个真正的关键字吗？

class Sensor : public QObject
{
    Q_OBJECT

public:
    explicit Sensor(QObject *parent = nullptr);

signals:
    // TODO(2): 声明信号
    //   void temperatureChanged(double temp);
    //   void overheated(double temp);
    //
    //   信号不需要实现，也不能实现。MOC 自动生成。
    void  temperatureChanged(double temp);
    void overheated(double temp);

public slots:
    // TODO(3): 声明槽函数
    //   void readTemperature();
    void readTemperature();

private:
    double _threshold = 35.0;
    double _currentTemp = 0.0;
};

#endif // SENSOR_H