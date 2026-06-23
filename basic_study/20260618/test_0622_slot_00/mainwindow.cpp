#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // TODO(7): 创建 UI
    //   创建 _centralWidget（parent = this），setCentralWidget
    //   创建 _labelTemp（初始文本 "温度: --"）
    //   创建 _labelWarning（初始文本 ""，空的）
    //   创建 _btnRead（文本 "读取温度"）
    //   创建 _btnReset（文本 "重置警告"）
    //   所有控件的 parent 传 _centralWidget

    _centralWidget = new QWidget(this);
    setCentralWidget(_centralWidget);
    _labelTemp = new QLabel("温度：--",_centralWidget);
    _labelWarning = new QLabel("",_centralWidget);
    _btnRead = new QPushButton("读取温度",_centralWidget);
    _btnReset = new QPushButton("重置警告",_centralWidget);

    // TODO(8): 创建 Sensor
    //   _sensor = new Sensor(this);
    //   parent 传 this（MainWindow），让对象树管理它
    //   注意：Sensor 不是 widget，不需要加入布局，它只是逻辑对象
    _sensor = new Sensor(this);

    // TODO(9): 布局
    //   QVBoxLayout，把4个控件加进去
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(_labelTemp);
    layout->addWidget(_labelWarning);
    layout->addWidget(_btnRead);
    layout->addWidget(_btnReset);
    _centralWidget->setLayout(layout);

    // TODO(10): 连接信号槽
    //
    //   连接1：按钮 clicked → 传感器 readTemperature
    //   connect(_btnRead, &QPushButton::clicked, _sensor, &Sensor::readTemperature);
    //   含义：点击按钮 → 直接触发传感器读取（按钮信号连到另一个对象的槽）
    //
    //   连接2：传感器 temperatureChanged → 主窗口 onTemperatureChanged
    //   connect(_sensor, &Sensor::temperatureChanged, this, &MainWindow::onTemperatureChanged);
    //
    //   连接3：传感器 overheated → 主窗口 onOverheated
    //   connect(_sensor, &Sensor::overheated, this, &MainWindow::onOverheated);
    //
    //   连接4：重置按钮 → 主窗口 onReset
    //   connect(_btnReset, &QPushButton::clicked, this, &MainWindow::onReset);
    //
    //   思考：连接1 中，按钮的 clicked() 没有参数，但 readTemperature() 也没有参数
    //         如果信号参数比槽多怎么办？如果信号参数比槽少呢？
    //         答：信号参数 >= 槽参数 可以（多余的被忽略）
    //             信号参数 < 槽参数 不行（编译报错）
    connect(_btnRead, &QPushButton::clicked, _sensor, &Sensor::readTemperature);
    connect(_sensor,&Sensor::temperatureChanged, this , &MainWindow::onTemperatureChanged);
    connect(_sensor, &Sensor::overheated, this , &MainWindow::onOverheated);
    connect(_btnReset, &QPushButton::clicked, this, &MainWindow::onReset);

    setWindowTitle("信号与槽练习 - 温度传感器");
    resize(400, 250);
}

MainWindow::~MainWindow() {}

// TODO(11): 实现 onTemperatureChanged(double temp)
//   更新 _labelTemp 的文本为 "温度: xx.x °C"
//   提示：QString::number(temp, 'f', 1) 可以格式化为1位小数
void MainWindow::onTemperatureChanged(double temp){
    _labelTemp->setText("温度：" + QString::number(temp,'f',1)+"℃");


}

// TODO(12): 实现 onOverheated(double temp)
//   设置 _labelWarning 的文本为 "⚠ 警告：温度过高！xx.x °C"
//   设置 _labelWarning 的样式为红色：
//   _labelWarning->setStyleSheet("color: red; font-weight: bold;");
void MainWindow::onOverheated(double temp){
    _labelWarning->setText("⚠ 警告：温度过高！"+ QString::number(temp,'f',1)+"°C");
    _labelWarning->setStyleSheet("color: red; font-weight: bold;");

}

// TODO(13): 实现 onReset()
//   清空 _labelWarning 的文本
//   恢复样式：_labelWarning->setStyleSheet("");
void MainWindow::onReset(){
    _labelWarning->clear();
    _labelWarning->setStyleSheet("");

}