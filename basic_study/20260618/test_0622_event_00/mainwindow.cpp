#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
{
    // TODO(6): 创建 UI
    //   创建 _labelMouse（初始文本 "鼠标：等待点击..."）
    //   创建 _labelKey（初始文本 "键盘：等待按键..."）
    //   创建 _labelFilter（初始文本 "过滤器：等待事件..."）
    //   创建 _btn（文本 "点我试试"）
    //   所有控件的 parent 传 this（因为没有 centralWidget，直接挂在 MainWindow 上）
    _labelMouse = new QLabel("鼠标：等待点击...",this);
    _labelKey = new QLabel("键盘：等待按键...", this);
    _labelFilter = new QLabel("过滤器：等待事件...",this);
    _btn = new QPushButton("点我试试", this);

    // TODO(7): 布局
    //   QVBoxLayout *layout = new QVBoxLayout(this);
    //   把4个控件加进去
    //
    //   注意：QVBoxLayout(this) 直接传 this 作为 parent
    //   等价于 new QVBoxLayout() + this->setLayout(layout)
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(_labelMouse);
    layout->addWidget(_labelKey);
    layout->addWidget(_labelFilter);
    layout->addWidget(_btn);
    this->setLayout(layout);

    // TODO(8): 启用鼠标追踪（可选）
    //   setMouseTracking(true);
    //   不加这行的话，mouseMoveEvent 只在按住鼠标时触发
    //   加了之后，鼠标在窗口内移动就会触发
    setMouseTracking(true);

    // TODO(9): 安装事件过滤器
    //   _btn->installEventFilter(this);
    //
    //   含义：把 this（MainWindow）注册为 _btn 的事件过滤器
    //   之后 _btn 收到的所有事件，会先经过 MainWindow::eventFilter() 处理
    //
    //   应用场景：你想监控/拦截某个控件的事件，但不想子类化它
    _btn->installEventFilter(this);

    setWindowTitle("事件系统练习");
    resize(500, 300);
}

MainWindow::~MainWindow() {}

// TODO(10): 实现 mousePressEvent
//
//   void MainWindow::mousePressEvent(QMouseEvent *event) {
//       获取点击位置：event->pos()    返回 QPoint（相对于窗口）
//       获取按键类型：event->button()  返回 Qt::LeftButton / Qt::RightButton 等
//
//       更新 _labelMouse 的文本，显示：
//       "鼠标：点击位置 (x, y)，按键：Left/Right/Middle"
//
//       提示：
//       - event->pos().x() 和 event->pos().y() 获取坐标
//       - 判断按键：if (event->button() == Qt::LeftButton)
//       - QString("鼠标：点击 (%1, %2)，按键：%3").arg(x).arg(y).arg(btnName)
//   }
void MainWindow::mousePressEvent(QMouseEvent *event){
    QPoint point = event->pos();
    QString btnName;
    if(Qt::LeftButton == event->button()){
        btnName = "Left";
    }
    else if (Qt::RightButton == event->button())
    {
        btnName ="Right";
    }
    else{
        btnName = "Middle";
    }
    _labelMouse->setText(QString("鼠标：点击(%1,%2),按键：%3").arg(point.x()).arg(point.y()).arg(btnName));

}

// TODO(11): 实现 mouseMoveEvent
//
//   void MainWindow::mouseMoveEvent(QMouseEvent *event) {
//       更新 _labelMouse 显示当前鼠标位置：
//       "鼠标：移动到 (x, y)"
//
//       提示：event->pos() 同样可用
//   }
void MainWindow::mouseMoveEvent(QMouseEvent *event){
    QPoint point = event->pos();
    _labelMouse->setText("鼠标移动到 ("+ QString::number(point.x(),point.y())+")");
}
// TODO(12): 实现 keyPressEvent
//
//   void MainWindow::keyPressEvent(QKeyEvent *event) {
//       获取按键码：event->key()     返回 int（如 Qt::Key_A = 65）
//       获取按键文本：event->text()  返回 QString（如 "a"）
//
//       更新 _labelKey 的文本：
//       "键盘：按下 [A]，键码：65"
//
//       提示：
//       - QKeySequence(event->key()).toString() 可以把键码转为可读字符串
//       - 或者直接用 event->text()（对字母/数字有效）
//
//       思考：如果按下的是 Ctrl+C 这种组合键，event->key() 和
//             event->modifiers() 分别是什么？
//   }
void MainWindow::keyPressEvent(QKeyEvent *event){

}

// TODO(13): 实现 eventFilter
//
//   bool MainWindow::eventFilter(QObject *watched, QEvent *event) {
//       if (watched == _btn) {
//           if (event->type() == QEvent::MouseButtonPress) {
//               更新 _labelFilter："过滤器：拦截到按钮的鼠标点击！"
//               return true;   // 吃掉事件，按钮不会收到 clicked 信号
//           }
//           if (event->type() == QEvent::Enter) {
//               更新 _labelFilter："过滤器：鼠标进入按钮区域"
//               // return false; 不拦截，让按钮正常高亮
//           }
//       }
//       return QWidget::eventFilter(watched, event);  // 其他事件正常传递
//   }
//
//   思考：
//   - 如果 return true，按钮的 clicked 信号还会发射吗？（不会！事件被吃掉了）
//   - eventFilter 和直接重写 mousePressEvent 有什么区别？
//     答：重写需要子类化，eventFilter 可以在外部对象上拦截，不需要改目标类
bool MainWindow::eventFilter(QObject *watched, QEvent *event){
    if(watched == _btn){
        if(event->type()== QEvent::MouseButtonPress){
            _labelFilter->setText("过滤器：拦截到按钮的鼠标点击！");
            return true;
        }
        if(event->type()==QEvent::Enter){
            _labelFilter->setText("过滤器：鼠标进入按钮区域");
        }
    }
    return QWidget::eventFilter(watched,event);
}