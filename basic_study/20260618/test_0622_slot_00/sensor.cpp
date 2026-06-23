#include "sensor.h"

Sensor::Sensor(QObject *parent)
    : QObject(parent)
{}

// TODO(4): 实现 readTemperature()
//
//   实现步骤：
//   (a) 用 QRandomGenerator 生成随机温度（15.0 ~ 45.0）
//       _currentTemp = 15.0 + QRandomGenerator::global()->generateDouble() * 30.0;
//       （generateDouble() 返回 [0.0, 1.0) 范围的随机 double，乘以30加15得到 [15.0, 45.0)）
//
//   (b) 保存到 _currentTemp
//
//   (c) 发射 temperatureChanged 信号：
//       emit temperatureChanged(_currentTemp);
//
//       emit 的作用：调用 MOC 生成的信号函数，通知所有连接的槽
//       实际上 emit 是空宏（#define emit），写不写都行，但写上表达意图
//
//   (d) 判断是否超温，如果 _currentTemp > _threshold：
//       emit overheated(_currentTemp);

void Sensor::readTemperature(){
    _currentTemp =15.0 + QRandomGenerator::global()->generateDouble() * 30.0;
    emit temperatureChanged(_currentTemp);
    if(_currentTemp > _threshold){
        emit overheated(_currentTemp);
    }
}