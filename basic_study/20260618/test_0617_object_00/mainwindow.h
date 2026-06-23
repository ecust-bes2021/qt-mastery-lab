#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QDebug>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    // TODO(1): 声明成员变量
    //   QWidget *_centralWidget;       — 中心 widget（作为对象树的中间节点）
    //   QLabel *_label1;               — 显示 "设备A"
    //   QLabel *_label2;               — 显示 "设备B"
    //   QPushButton *_btn;             — 按钮 "打印对象树"
    //
    //   注意：这些指针不需要在析构函数里 delete
    //         思考：为什么？谁负责释放它们？
    QWidget *_centralWidget;
    QLabel *_label1;
    QLabel *_label2;
    QPushButton *_btn;


private slots:
    // TODO(2): 声明槽函数
    //   void onPrintTree();            — 按钮点击时调用，遍历打印对象树
    void onPrintTree();

};
#endif // MAINWINDOW_H