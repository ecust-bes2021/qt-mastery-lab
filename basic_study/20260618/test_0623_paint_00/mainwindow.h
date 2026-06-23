#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>
#include <QPainter>
#include <QPen>
#include <QBrush>
#include <QLinearGradient>
#include <QRadialGradient>

// ============================================================
// QPainter 绘制练习 — 基本图形集合
//
// 目标：掌握 QPainter 核心 API
//   - paintEvent 重写（绘制的入口）
//   - QPen（笔）— 控制线条颜色、宽度、样式
//   - QBrush（刷子）— 控制填充颜色、渐变、图案
//   - 基本图形：线、矩形、圆/椭圆、圆弧、文字
//   - 坐标系：原点在左上角，x 向右，y 向下
//   - 渐变填充：线性渐变、径向渐变
//
// 关键规则：
//   QPainter 只能在 paintEvent() 内部创建和使用！
//   不能在构造函数或其他地方画图。
//   窗口每次需要重绘时，Qt 会自动调用 paintEvent。
// ============================================================

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    // TODO(1): 重写 paintEvent
    //   void paintEvent(QPaintEvent *event) override;
    //
    //   这是 QPainter 绑定的事件。Qt 在以下时机调用它：
    //   - 窗口首次显示
    //   - 窗口被遮挡后重新露出
    //   - 窗口大小改变
    //   - 手动调用 update()
    //
    //   所有绑制代码必须写在这个函数里。
    void paintEvent(QPaintEvent *event) override;

private:
    // TODO(11): 声明仪表盘绘制函数
    //   void drawGauge(QPainter &painter);
    //
    //   把仪表盘的绘制逻辑封装成单独函数，保持 paintEvent 整洁
    //   参数用引用传递 QPainter（不能拷贝）
    void drawGauge(QPainter &painter);

    double _gaugeValue = 60.0;   // 仪表盘当前值（0~100），控制指针角度
};

#endif // MAINWINDOW_H