#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
{
    setWindowTitle("QPainter 绘制练习");
    resize(600, 450);
}

MainWindow::~MainWindow() {}

// TODO(2): 实现 paintEvent
//
//   void MainWindow::paintEvent(QPaintEvent *event) {
//       Q_UNUSED(event);   // 暂时不用 event 参数，避免编译警告
//
//       QPainter painter(this);  // 在当前 widget 上画图
//       //       ↑ 构造时传 this，表示"在我这个窗口上画"
//       //       painter 析构时自动结束绑制
//
//       // ────────────────────────────────────────
//       // TODO(3): 画线
//       //   painter.setPen(QPen(Qt::black, 2));   // 黑色，2像素宽
//       //   painter.drawLine(20, 20, 200, 20);    // 从(20,20)到(200,20)的水平线
//       //
//       //   QPen 控制线条外观：
//       //   QPen(颜色, 宽度, 线型)
//       //   线型：Qt::SolidLine(实线)、Qt::DashLine(虚线)、Qt::DotLine(点线)
//       //
//       //   画一条虚线：
//       //   painter.setPen(QPen(Qt::red, 2, Qt::DashLine));
//       //   painter.drawLine(20, 40, 200, 40);
//
//       // ────────────────────────────────────────
//       // TODO(4): 画矩形
//       //   painter.setPen(QPen(Qt::blue, 2));
//       //   painter.setBrush(QBrush(Qt::cyan));   // 填充颜色
//       //   painter.drawRect(20, 60, 150, 80);    // x, y, 宽, 高
//       //
//       //   QPen = 边框，QBrush = 填充
//       //   如果不想要边框：painter.setPen(Qt::NoPen);
//       //   如果不想要填充：painter.setBrush(Qt::NoBrush);
//
//       // ────────────────────────────────────────
//       // TODO(5): 画圆 / 椭圆
//       //   painter.setPen(QPen(Qt::darkGreen, 2));
//       //   painter.setBrush(QBrush(Qt::green));
//       //   painter.drawEllipse(220, 60, 100, 100);  // 正圆（宽==高）
//       //   //                  x, y, 宽, 高  → 外接矩形
//       //
//       //   画椭圆（宽 ≠ 高）：
//       //   painter.drawEllipse(350, 60, 150, 80);
//
//       // ────────────────────────────────────────
//       // TODO(6): 画圆角矩形
//       //   painter.setPen(QPen(Qt::darkMagenta, 2));
//       //   painter.setBrush(QBrush(Qt::magenta));
//       //   painter.drawRoundedRect(20, 180, 150, 80, 15, 15);
//       //   //                      x, y, 宽, 高, x圆角半径, y圆角半径
//
//       // ────────────────────────────────────────
//       // TODO(7): 画文字
//       //   painter.setPen(Qt::black);
//       //   painter.setFont(QFont("Arial", 16, QFont::Bold));
//       //   painter.drawText(220, 200, "Hello QPainter!");
//       //   //              x, y, 文字内容
//       //   // 注意：y 是文字基线位置，不是左上角
//       //
//       //   也可以在矩形内画文字（自动对齐）：
//       //   painter.drawText(QRect(220, 220, 200, 40), Qt::AlignCenter, "居中文字");
//
//       // ────────────────────────────────────────
//       // TODO(8): 线性渐变填充
//       //   QLinearGradient gradient(20, 300, 170, 380);
//       //   //                      起点x,y    终点x,y
//       //   gradient.setColorAt(0, Qt::red);      // 起点颜色
//       //   gradient.setColorAt(1, Qt::yellow);   // 终点颜色
//       //
//       //   painter.setPen(Qt::NoPen);
//       //   painter.setBrush(gradient);            // 用渐变作为刷子
//       //   painter.drawRect(20, 300, 150, 80);
//
//       // ────────────────────────────────────────
//       // TODO(9): 径向渐变填充
//       //   QRadialGradient radGrad(300, 340, 60);
//       //   //                     圆心x, 圆心y, 半径
//       //   radGrad.setColorAt(0, Qt::white);    // 中心颜色
//       //   radGrad.setColorAt(1, Qt::blue);     // 边缘颜色
//       //
//       //   painter.setBrush(radGrad);
//       //   painter.drawEllipse(240, 280, 120, 120);
//
//       // ────────────────────────────────────────
//       // TODO(10): 抗锯齿（可选，让图形边缘更平滑）
//       //   painter.setRenderHint(QPainter::Antialiasing, true);
//       //   ↑ 建议在 paintEvent 开头就加上
//       //   开启后圆和斜线会更平滑，但性能略微下降
//   }
void MainWindow::paintEvent(QPaintEvent *event){
    Q_UNUSED(event);

    QPainter painter(this);

    painter.setPen(QPen(Qt::black,2));
    painter.drawLine(20,20,200,20);

    painter.setPen(QPen(Qt::red ,2,Qt::DashLine));
    painter.drawLine(20,40,200,40);

    painter.setPen(QPen(Qt::blue,2));
    painter.setPen(Qt::NoPen);
    painter.setBrush(QBrush(Qt::cyan));
    // painter.setBrush(Qt::NoBrush);
    painter.drawRect(20,40,200,40);

    painter.setPen(QPen(Qt::darkBlue ,2));
    painter.setBrush(QBrush(Qt::green));
    painter.drawEllipse(220,60,150,80);

    painter.setPen(QPen(Qt::darkMagenta,2));
    painter.setBrush(QBrush(Qt::magenta));
    painter.drawRoundedRect(20,180,150,80,15,15);

    painter.setPen(Qt::black);
    painter.setFont(QFont("Arial",16,QFont::Bold));
    painter.drawText(220,200,"Hello QPainter!");
    painter.drawText(QRect(220,220,200,40),Qt::AlignCenter,"文字居中");
   
    QLinearGradient gradient(20,300,170,380);
    gradient.setColorAt(0,Qt::red);
    gradient.setColorAt(1,Qt::yellow);
    painter.setPen(Qt::NoPen);
    painter.setBrush(gradient);
    painter.drawRect(20,300,150,80);

    QRadialGradient radGrad(300,340,60);
    radGrad.setColorAt(0,Qt::white);
    radGrad.setColorAt(1, Qt::blue);

    painter.setBrush(radGrad);
    painter.drawEllipse(240,280,120,120);

    // TODO(11): 在 paintEvent 末尾调用仪表盘绘制
    //   drawGauge(painter);
    //   传引用，让 drawGauge 用同一个 painter 继续画
    drawGauge(painter);
}

// ============================================================
// 仪表盘绘制练习
//
// 目标：综合运用 QPainter 绘制一个简易仪表盘
//   - 圆弧（drawArc）
//   - 坐标变换（translate + rotate）
//   - 三角函数定位刻度和指针
//   - 文字绘制
//
// 预期效果：
//   ┌─────────────────────┐
//   │       ╭───╮         │
//   │     ╱   |   ╲       │  ← 圆弧（刻度盘）
//   │    │    |    │       │  ← 指针（从圆心出发的线）
//   │    │  ╱    │       │
//   │     ╲________╱       │
//   │        60            │  ← 数值文字
//   └─────────────────────┘
// ============================================================

// TODO(12): 实现 drawGauge
//
//   void MainWindow::drawGauge(QPainter &painter) {
//
//       // ── 步骤1：确定仪表盘的位置和大小 ──
//       //   int cx = 450;          // 圆心 x（放在窗口右侧）
//       //   int cy = 200;          // 圆心 y
//       //   int radius = 100;      // 半径
//
//       // ── 步骤2：画外圆弧（刻度盘背景）──
//       //   painter.setPen(QPen(Qt::darkGray, 8));
//       //   painter.setBrush(Qt::NoBrush);
//       //
//       //   QRect arcRect(cx - radius, cy - radius, radius * 2, radius * 2);
//       //   // drawArc 参数：矩形, 起始角度, 跨越角度
//       //   // 角度单位是 1/16 度！（Qt 的奇葩设计）
//       //   // 0度 = 3点钟方向，逆时针为正
//       //   //
//       //   // 仪表盘通常是从左下到右下的弧（约225° → -45°）
//       //   // 起始角 = 225° × 16 = 3600
//       //   // 跨越角 = -270° × 16 = -4320（顺时针270度）
//       //   painter.drawArc(arcRect, 225 * 16, -270 * 16);
//
//       // ── 步骤3：画刻度线 ──
//       //   painter.setPen(QPen(Qt::black, 2));
//       //   // 画11条刻度线（0, 10, 20, ... 100）
//       //   for (int i = 0; i <= 10; i++) {
//       //       // 角度：从225°到-45°，共270°范围
//       //       double angle = (225.0 - i * 27.0) * M_PI / 180.0;  // 转弧度
//       //       // M_PI 需要 #include <QtMath> 或 #include <cmath>
//       //
//       //       // 刻度线的起点（圆弧内侧）和终点（圆弧外侧）
//       //       int x1 = cx + (radius - 15) * cos(angle);
//       //       int y1 = cy - (radius - 15) * sin(angle);
//       //       int x2 = cx + (radius - 5) * cos(angle);
//       //       int y2 = cy - (radius - 5) * sin(angle);
//       //
//       //       painter.drawLine(x1, y1, x2, y2);
//       //   }
//
//       // ── 步骤4：画指针 ──
//       //   painter.setPen(QPen(Qt::red, 3));
//       //   // _gaugeValue 范围 0~100 → 角度范围 225° → -45°
//       //   double needleAngle = (225.0 - _gaugeValue * 2.7) * M_PI / 180.0;
//       //   int nx = cx + (radius - 25) * cos(needleAngle);
//       //   int ny = cy - (radius - 25) * sin(needleAngle);
//       //   painter.drawLine(cx, cy, nx, ny);   // 从圆心到指针端点
//
//       // ── 步骤5：画圆心小圆点 ──
//       //   painter.setPen(Qt::NoPen);
//       //   painter.setBrush(Qt::red);
//       //   painter.drawEllipse(cx - 5, cy - 5, 10, 10);
//
//       // ── 步骤6：画数值文字 ──
//       //   painter.setPen(Qt::black);
//       //   painter.setFont(QFont("Arial", 14, QFont::Bold));
//       //   painter.drawText(QRect(cx - 30, cy + 20, 60, 30),
//       //                    Qt::AlignCenter,
//       //                    QString::number(_gaugeValue, 'f', 1));
//       //   // 'f' = 浮点格式，1 = 小数点后1位
//   }

void MainWindow::drawGauge(QPainter &painter){
    int cx = 450;
    int cy = 200;
    int radius = 100;

    painter.setPen(QPen(Qt::darkGray,8));
    painter.setBrush(Qt::NoBrush);
    QRect arcRect(cx-radius,cy-radius,radius*2,radius*2);
    painter.drawArc(arcRect,225*16,-270*16);

    painter.setPen(QPen(Qt::black,2));
    for(int i =0; i<=10;i++){
        double angle = (225.0 - i*27.0)*M_PI/180.0;
        int x1 = cx + (radius -15)*cos(angle);
        int y1 = cy + (radius-15)*sin(angle);
        int x2 = cx + (radius -5)*cos(angle);
        int y2 = cy + (radius - 5)* sin(angle);

        painter.drawLine(x1,y1,x2,y2);
    }

    painter.setPen(QPen(Qt::red, 3));
    double needLeAngle = (225.0 - _gaugeValue*2.7)*M_PI/180.0;
    int nx = cx + (radius -25) *cos(needLeAngle);
    int ny = cy - (radius -25) *sin(needLeAngle);
    painter.drawLine(cx,cy,nx,ny);

    painter.setPen(Qt::NoPen);
    painter.setBrush(Qt::red);
    painter.drawEllipse(cx-5,cy-5,10,10);
    
    painter.setPen(Qt::black);
    painter.setFont(QFont("Arial",14,QFont::Bold));
    painter.drawText(QRect(cx-30,cy+20,60,30),Qt::AlignCenter,QString::number(_gaugeValue,'f',1));
}