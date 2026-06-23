#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>

// ============================================================
// 布局系统练习 — 轻量版
//
// 目标：用最少控件覆盖所有布局知识点
//   - QVBoxLayout / QHBoxLayout / QGridLayout
//   - 布局嵌套（addLayout）
//   - 间距（spacing）和边距（contentsMargins）
//   - 伸缩因子（stretch / addStretch）
//   - 尺寸策略（QSizePolicy）
//
// 预期界面：
//   ┌──────────────────────────────┐
//   │  [标题 Label]                │  ← 顶部标题（Fixed 高度）
//   │                              │
//   │  [A]  [B]                    │  ← QGridLayout 2x2
//   │  [C]  [D]                    │
//   │                              │
//   │  [确定]  ←弹簧→  [取消]     │  ← 底部栏（HBox + stretch）
//   └──────────────────────────────┘
// ============================================================

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    // TODO(1): 声明成员变量
    //   QLabel *_labelTitle;           — 顶部标题
    //   QPushButton *_btnA;            — 按钮 A
    //   QPushButton *_btnB;            — 按钮 B
    //   QPushButton *_btnC;            — 按钮 C
    //   QPushButton *_btnD;            — 按钮 D
    //   QPushButton *_btnOK;           — 确定按钮
    //   QPushButton *_btnCancel;       — 取消按钮
    QLabel *_labelTitle;
    QPushButton *_btnA;
    QPushButton *_btnB;
    QPushButton *_btnC;
    QPushButton *_btnD;
    QPushButton *_btnOK;
    QPushButton *_btnCancel;
};

#endif // MAINWINDOW_H