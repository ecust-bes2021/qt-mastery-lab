#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include "sensor.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    // TODO(5): 声明成员变量
    //   QWidget *_centralWidget;
    //   QLabel *_labelTemp;          — 显示当前温度
    //   QLabel *_labelWarning;       — 显示警告信息
    //   QPushButton *_btnRead;       — "读取温度" 按钮
    //   QPushButton *_btnReset;      — "重置警告" 按钮
    //   Sensor *_sensor;             — 传感器对象
    QWidget *_centralWidget;
    QLabel *_labelTemp;
    QLabel *_labelWarning;
    QPushButton *_btnRead;
    QPushButton *_btnReset;
    Sensor *_sensor;

private slots:
    // TODO(6): 声明槽函数
    //   void onTemperatureChanged(double temp);   — 收到温度更新
    //   void onOverheated(double temp);           — 收到超温警告
    //   void onReset();                           — 重置警告标签
    void onTemperatureChanged(double temp);
    void onOverheated(double temp);
    void onReset();
                               
};

#endif // MAINWINDOW_H