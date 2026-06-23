# C++ Qt6 知识点笔记

> 整理自 Qt6 C++ 学习过程中的问答，涵盖 C++ 基础语法、编译流程、Qt 框架机制三大块。

---

## 一、C++ 基础语法

### 1. 成员初始化列表

**语法格式**：

```cpp
类名::类名(参数列表)
    : 父类(参数)              // 用冒号开头
    , 成员1(初始值)            // 后续用逗号分隔
    , 成员2(初始值)
{
    // 构造函数体
}
```

**示例**：

```cpp
class Engine {
public:
    int horsepower;
    Engine(int hp) : horsepower(hp) {}
};

class Car : public Engine {
public:
    string brand;
    const int seats;       // const 成员
    int *price;            // 指针成员

    Car(string b, int hp, int s, int p)
        : Engine(hp)              // ① 构造父类
        , brand(b)                // ② 初始化普通成员
        , seats(s)                // ③ 初始化 const 成员（只能在这里）
        , price(new int(p))       // ④ 初始化指针成员
    {}

    ~Car() { delete price; }
};
```

**关键点**：
- `: 父类(参数)` — 唯一指定父类构造方式的地方，**不能**在函数体里调用父类构造
- `, 成员(值)` — 初始化成员变量，对于 `const`、引用、没有无参构造的类型**必须**用初始化列表
- 执行顺序：父类构造 → 成员初始化 → 函数体

**构造与析构的顺序关系**：

构造和析构是**严格镜像**的，像栈一样先进后出：

```
构造：父类 → 成员（按声明顺序） → 函数体
析构：函数体 → 成员（按声明逆序） → 父类
```

原因：后构造的对象可能依赖先构造的对象，所以销毁时必须先销毁后构造的，保证"被依赖者"最后才走。

```cpp
class Example {
    Database *db;      // 先构造
    Logger *logger;    // 后构造，依赖 db

    Example() {
        db = new Database();
        logger = new Logger(db);   // logger 内部使用 db
    }
    ~Example() {
        delete logger;   // 后构造的先销毁
        delete db;       // 先构造的后销毁
    }
};
```

Qt 对象树也遵循此规则：父对象析构时自动 delete 所有子对象，子对象先于父对象被销毁。

---

### 2. `new` 与堆内存

```cpp
int *a = new int;              // 堆上创建 int（未初始化）
int *b = new int(42);          // 堆上创建 int，初始值 42
int *c = new int[100];         // 堆上创建 100 个 int 的数组
string *s = new string("hi");  // 堆上创建 string
```

**配对规则**：
- `new` → `delete`
- `new[]` → `delete[]`
- 忘了 `delete` → 内存泄漏

---

### 3. 栈 vs 堆

```cpp
void foo() {
    int x = 10;                    // 栈上，函数结束自动销毁
    int *p = new int(42);          // 堆上，必须手动 delete
}
```

| | 栈 | 堆 |
|--|--|--|
| 生命周期 | 函数结束自动销毁 | 手动管理或交给对象树 |
| 大小 | 编译时确定 | 运行时确定 |
| 速度 | 快 | 相对慢 |

---

### 4. 指针

```cpp
int *p = new int(42);   // 指针 p 在栈上，指向堆上的 42
//  ↑ 声明时：* 表示指针类型
int value = *p;         // 使用时：* 表示解引用（取值）
//         ↑ 表达式里：* 表示解引用
```

---

### 4.1 指针 ≠ 堆对象

指针只是一个**存地址的变量**，它可以指向任何地方，不一定要 `new`：

```cpp
// 情况1：指针指向堆对象（最常见）
int *p1 = new int(42);      // p1 在栈上，指向堆上的 42

// 情况2：指针指向栈对象
int x = 42;
int *p2 = &x;              // p2 在栈上，指向栈上的 x

// 情况3：指针指向另一个对象的成员
struct Foo { int val; };
Foo foo{10};
int *p3 = &foo.val;        // p3 指向栈上 foo 的成员

// 情况4：指针为空
int *p4 = nullptr;          // 不指向任何东西
```

| 情况 | 需要 `delete`？ | 生命周期谁管？ |
|------|----------------|----------------|
| `new` 出来的 | 是 | 你自己（或 Qt 对象树） |
| `&` 取地址得到的 | 不需要 | 原对象自己管 |
| 函数参数传指针 | 不需要 | 调用者管 |

**Qt 中的体现**：

```cpp
// parent 参数就是"指向别人的指针"，不是 new 出来的
MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    // 这个 parent 可能是栈上的，可能是堆上的
    // 你不 new 它，也不 delete 它
}

// main.cpp 中：
int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MainWindow w;           // 栈上！
    w.show();               // &w 就是个指向栈对象的指针
    return app.exec();
}
```

**一句话**：指针只是"遥控器"，`new` 才是"创建堆对象"的动作。可以有遥控器但不创建新对象。

---

### 4.2 空指针与野指针

**空指针（Null Pointer）**：指针没有指向有效对象

```cpp
int *p = nullptr;    // 明确标记"我还没指向任何东西"

*p = 42;             // ❌ 崩溃！段错误（Segmentation Fault）
p->doSomething();    // ❌ 崩溃！
```

防御方式——使用前先判空：

```cpp
if (p != nullptr) {
    *p = 42;         // ✅ 安全
}
if (p) {             // 等价于 p != nullptr
    p->doSomething();
}
```

**野指针（Dangling Pointer）**：指针指向的对象已经被销毁，但指针还保留着旧地址

```cpp
int *p = new int(42);
delete p;            // 对象已释放
// 此时 p 仍然保存着那个地址，但内存已经还给系统了

*p = 100;            // ❌ 野指针！未定义行为（可能崩溃，可能不崩但数据错乱）
```

**野指针比空指针更危险**：空指针解引用 → 立刻崩溃，容易定位；野指针解引用 → 可能不崩，偷偷改了别人的内存，bug 在很远的地方才暴露。

**野指针的常见来源**：

```cpp
// 来源1：delete 后没置空
int *p = new int(10);
delete p;
// p 现在是野指针！
p = nullptr;         // ✅ 养成习惯：delete 后立刻置空

// 来源2：返回局部变量的地址
int* badFunc() {
    int x = 42;
    return &x;       // ❌ 函数结束后 x 销毁，返回的地址变野
}

// 来源3：对象树中，子对象被提前手动 delete
QLabel *label = new QLabel("hi", parent);
delete label;        // 手动删了
// parent 析构时还会再 delete 一次 → double free
```

**三种状态的危险等级**：

```cpp
int *p1;                // ❌ 未初始化指针（最危险，指向垃圾地址）
int *p2 = nullptr;      // ✅ 空指针（安全，解引用前可以判断）
int *p3 = new int(42);  // ✅ 有效指针

delete p3;              // 释放后：
// p3 现在是野指针（危险）
p3 = nullptr;           // ✅ 变成空指针（安全状态）
```

**最佳实践**：

| 原则 | 做法 |
|------|------|
| 初始化 | 声明指针时就赋值（`= nullptr` 或 `= new ...`） |
| delete 后置空 | `delete p; p = nullptr;` |
| 使用前判空 | `if (p) { ... }` |
| Qt 场景 | 不要手动 delete 对象树中的对象，交给 parent 管理 |
| 现代 C++ | 尽量用智能指针（`std::unique_ptr`、`std::shared_ptr`）替代裸指针 |

---

### 4.3 .h 中指针 vs 值类型的选择

```cpp
// mainwindow.h
class MainWindow : public QMainWindow {
private:
    QLabel *_label;         // 指针 → 堆上创建，对象树管理
    Sensor *_sensor;        // 指针 → 堆上创建，对象树管理
    double _threshold;      // 值类型 → 简单数据，直接存
    QString _name;          // 值类型 → Qt 值类型自己管理内存
};
```

| 类型 | 用什么 | 原因 |
|------|--------|------|
| QObject 子类（控件、自定义对象） | 指针 + `new` | 对象树要求堆分配 |
| 简单值类型（int、double、bool） | 直接值 | 没必要上堆 |
| Qt 值类型（QString、QList、QVector） | 直接值 | 内部自己管理堆，支持隐式共享 |

---

### 4.4 指针函数与函数指针

**指针函数**：返回指针的普通函数

```cpp
int* createArray(int size) {
    int *arr = new int[size];
    return arr;                   // 返回堆对象地址，调用者负责释放
}

int *data = createArray(10);
delete[] data;
```

Qt 中常见：

```cpp
QLabel* MainWindow::createLabel(const QString &text) {
    return new QLabel(text, this);   // 返回指针，parent 管理生命周期
}
```

**函数指针**：指向函数的指针变量

```cpp
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

// 声明：指向"接收两个 int，返回 int"的函数
int (*funcPtr)(int, int);

funcPtr = add;              // 函数名本身就是地址
int result = funcPtr(3, 4); // 通过指针调用 → 7
funcPtr = sub;
result = funcPtr(3, 4);     // → -1
```

**声明语法区别（关键！）**：

```cpp
int* func(int x);        // 指针函数：func 是函数，返回 int*
int (*ptr)(int x);       // 函数指针：ptr 是指针，指向函数
//   ↑ 括号是关键！
```

记忆：`*` 跟谁结合——
- `int *func(...)` → `*` 修饰返回值 → 返回指针的函数
- `int (*ptr)(...)` → `*` 修饰变量名（被括号框住） → 指向函数的指针

**实际用途**：

```cpp
// 用途1：回调（嵌入式常见）
typedef void (*Callback)(int);
void onDataReady(int value) { printf("received: %d\n", value); }
Callback cb = onDataReady;
cb(42);

// 用途2：Qt connect 中的成员函数指针
connect(btn, &QPushButton::clicked, this, &MainWindow::onClicked);
//           ↑ 成员函数指针             ↑ 成员函数指针
```

**成员函数指针 vs 普通函数指针**：

```cpp
// 普通函数指针：直接调用
void (*fp)() = &freeFunction;
fp();

// 成员函数指针：需要绑定对象才能调用
void (MyClass::*mfp)() = &MyClass::doSomething;
MyClass obj;
(obj.*mfp)();              // 必须通过对象调用（成员函数需要 this）
```

**现代 C++ 替代**：

```cpp
#include <functional>
std::function<int(int, int)> op = add;
op = [](int a, int b) { return a * b; };   // 也能存 lambda
```

| | 指针函数 | 函数指针 |
|--|---------|---------|
| 本质 | 函数 | 指针变量 |
| 声明 | `int* func(int)` | `int (*ptr)(int)` |
| 含义 | 返回一个地址 | 存一个函数的地址 |
| 用途 | 创建堆对象、工厂模式 | 回调、策略模式、Qt connect |

---

### 5. `const`

```cpp
const int x = 10;           // const 变量：值不能改
const int *p1 = &x;         // 指向的内容不能改
int *const p2 = &x;         // 指针本身不能改
const int *const p3 = &x;   // 都不能改

class Sensor {
    int _value;
public:
    int getValue() const { return _value; }   // const 成员函数：不修改对象
};

void print(const string &s) { cout << s; }    // const 引用参数：只读 + 零拷贝
```

---

### 6. `#define` vs `const`

```cpp
#define MAX 100           // 预处理文本替换，无类型、无作用域
const int MAX = 100;       // 真正的变量，有类型、有作用域、可调试
```

**原则**：能用 `const` 就不用 `#define`。`#define` 只用于头文件保护、条件编译。

---

### 7. 引用 `&`

```cpp
int x = 42;
int &ref = x;      // ref 是 x 的别名，同一个东西
int copy = x;      // copy 是新变量，值从 x 复制

ref = 100;         // x 也变成 100（同一个东西）
copy = 100;        // x 还是 42（独立变量）
```

**`&` 的两种含义**：
- 声明时（类型和变量名之间）：引用类型
- 表达式里：取地址

---

### 8. `const &`（只读引用）

```cpp
const QObjectList &children = widget->children();
// 零拷贝 + 只读，接收大对象返回值的标准写法
```

| 我要做什么 | 用什么 |
|-----------|--------|
| 只想看看数据 | `const &` |
| 想修改但不影响原始的 | 拷贝（不加 `&`） |
| 想直接修改原始数据 | `&`（非 const 引用） |

**函数参数传递方式的完整选择指南**：

```cpp
// 1. const & — 只读，不修改，不拷贝（最常用）
void print(const QString &text);        // 只读取 text

// 2. & — 会修改原对象（或对象禁止拷贝）
void drawGauge(QPainter &painter);      // 会 setPen/drawLine，修改 painter
void fill(QVector<int> &data);          // 往 data 里塞数据

// 3. 值传递 — 需要一份副本（小对象或确实需要拷贝）
void setAge(int age);                   // int 很小，直接拷贝
void process(QString text);             // 函数内部要改 text 但不影响外面

// 4. 指针 — 参数可能为空（可选参数）
void setParent(QObject *parent);        // parent 可以是 nullptr（表示无父对象）
void init(Config *cfg = nullptr);       // cfg 可选，不传就用默认配置
```

**决策流程**：

```
这个参数可能是 nullptr 吗？
├── 是 → 用指针 *
└── 不是 → 继续判断
    │
    函数内部会修改这个参数吗？
    ├── 会修改 → 用 &（非 const 引用）
    └── 不修改 → 继续判断
        │
        对象大吗？（大于 8~16 字节）
        ├── 大（QString、QVector、自定义类）→ 用 const &
        └── 小（int、double、bool、指针）→ 直接值传递
```

---

### 9. 深拷贝 vs 浅拷贝

```cpp
int *p = new int(42);

int *&ref = p;            // 引用：就是 p 本身
int *copy = p;            // 浅拷贝：新指针，指向同一块内存
int *deep = new int(*p);  // 深拷贝：新指针 + 新内存
```

| | 新变量？ | 新内存？ | 改一个另一个变？ |
|--|--|--|--|
| 引用 | 没有 | 没有 | 一定变 |
| 浅拷贝 | 有 | 没有 | 改指针不影响；改内容会影响 |
| 深拷贝 | 有 | 有 | 完全不影响 |

---

### 10. 拷贝构造函数

```cpp
class Buffer {
    int *data;
    int size;
public:
    Buffer(int s) : size(s), data(new int[s]) {}

    // 深拷贝构造函数
    Buffer(const Buffer &other)
        : size(other.size)
        , data(new int[other.size])
    {
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }
    }

    ~Buffer() { delete[] data; }
};
```

**Rule of Three**：如果类需要手动写析构函数（有 `delete`），几乎一定也要写拷贝构造函数和拷贝赋值运算符。

---

### 11. `this` 指针

```cpp
class Sensor {
    int value;
public:
    void setValue(int value) {
        this->value = value;   // this->value 是成员，value 是参数
    }
    int getValue() {
        return value;          // 省略 this->，编译器自动理解
    }
};
```

---

### 12. 访问控制

```cpp
class MyClass {
public:       // 任何人都能访问
    void foo();
protected:    // 本类 + 子类
    void bar();
private:      // 只有本类
    void baz();
    int _data;
};
```

**原则**：默认放 `private`，除非有明确理由让外部访问才放 `public`。

---

### 13. `explicit` 关键字

```cpp
class Sensor : public QObject {
public:
    explicit Sensor(QObject *parent = nullptr);   // 禁止隐式转换
};

// 没有 explicit 时：
void doSomething(Sensor s) {}
doSomething(nullptr);   // ✅ 编译通过！nullptr 被偷偷转换成 Sensor 对象

// 有 explicit 时：
doSomething(nullptr);          // ❌ 编译错误
doSomething(Sensor(nullptr));  // ✅ 必须显式写出来
```

**规则**：只要构造函数可以用一个参数调用（包括有默认值的情况），都应该加 `explicit`。Qt 的所有 QObject 子类都遵循这个惯例。

---

### 14. 头文件与实现分离

```cpp
// widget.h
#ifndef WIDGET_H
#define WIDGET_H
class Widget {
public:
    Widget();
    void doSomething();
private:
    int _data;
};
#endif

// widget.cpp
#include "widget.h"
Widget::Widget() : _data(0) {}
void Widget::doSomething() { _data = 42; }
```

---

### 14. 前向声明

```cpp
// mainwindow.h
namespace Ui { class MainWindow; }   // 前向声明，不需要 include ui_mainwindow.h

class MainWindow : public QMainWindow {
private:
    Ui::MainWindow *ui;   // 只用指针，不需要知道类的大小
};
```

---

### 15-16. `*` 和 `&` 的双重含义

```cpp
int x = 42;
int *p = &x;        // 声明：* 是指针类型；& 是取地址
int &ref = x;       // 声明：& 是引用类型
int value = *p;     // 表达式：* 是解引用
```

---

### 17. 函数定义格式

```cpp
返回值类型 类名::函数名(参数列表) {
    // 函数体
}

// 示例
void MainWindow::onPrintTree() {
    qDebug() << "clicked";
}
```

---

### 18. 堆上数组

```cpp
void foo(int s) {
    int stackArr[s];            // ❌ 栈上数组大小必须是编译时常量
    int *heapArr = new int[s];  // ✅ 堆上数组大小可以是变量
    delete[] heapArr;
}
```

---

## 二、C++ 编译相关

### 19. 编译五阶段

```
源代码 (.cpp/.h)
    │ ① 预处理    → 展开 #include、#define、条件编译
    ▼
预处理后代码 (.i)
    │ ② 编译      → 语法检查、类型检查、优化，生成汇编
    ▼
汇编代码 (.s)
    │ ③ 汇编      → 翻译成机器码
    ▼
目标文件 (.obj)
    │ ④ 链接      → 合并多个 .obj + 库，解析符号引用
    ▼
可执行文件 (.exe)
    │ ⑤ 加载运行   → OS 加载到内存，跳转到 main()
    ▼
程序执行
```

---

### 20. CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16)
project(myapp VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

set(PROJECT_SOURCES main.cpp mainwindow.cpp mainwindow.h)

qt_add_executable(myapp MANUAL_FINALIZATION ${PROJECT_SOURCES})
target_link_libraries(myapp PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

set_target_properties(myapp PROPERTIES WIN32_EXECUTABLE TRUE)

qt_finalize_executable(myapp)
```

**关键配置**：
- `find_package` — 找到系统上的 Qt 库
- `target_link_libraries` — 链接 Qt 模块
- `WIN32_EXECUTABLE TRUE` — Windows 上以 GUI 程序运行（不弹控制台）

---

### 21. AUTOMOC / AUTOUIC / AUTORCC

```cmake
set(CMAKE_AUTOUIC ON)   # 自动处理 .ui → ui_xxx.h
set(CMAKE_AUTOMOC ON)   # 自动处理 Q_OBJECT → moc_xxx.cpp
set(CMAKE_AUTORCC ON)   # 自动处理 .qrc → qrc_xxx.cpp
```

---

## 三、Qt / C++ Qt6 特有

### 22. Q_OBJECT 宏

```cpp
class MainWindow : public QMainWindow {
    Q_OBJECT    // 任何使用信号槽的类必须加
public:
    MainWindow(QWidget *parent = nullptr);
};
```

---

### 23. MOC（元对象编译器）

```
mainwindow.h (含 Q_OBJECT)
    │ MOC 扫描
    ▼
moc_mainwindow.cpp (自动生成)
    │ 包含：信号实现、元对象信息、qobject_cast 支持
    ▼
和你的代码一起编译
```

---

### 24. 对象树（parent-child）

```cpp
// 建立父子关系
QLabel *label = new QLabel("hello", parentWidget);
//                                ↑ 传 parent
// parentWidget 销毁时自动 delete label
```

```
MainWindow
└── centralWidget
    ├── label1      ← 自动被 centralWidget 管理
    ├── label2
    ├── button
    └── layout      ← setLayout 后也进入对象树
```

---

### 25. Qt 控件必须用 `new` + 指针

```cpp
// ✅ 正确：堆上 + parent 管理
QLabel *_label = new QLabel("text", this);

// ❌ 错误：栈上对象会和对象树冲突 → double free
QLabel _label;   // MainWindow 析构时销毁一次，对象树又 delete 一次
```

---

### 26. setCentralWidget

```cpp
MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    QWidget *central = new QWidget(this);
    setCentralWidget(central);    // QMainWindow 必须设置中心 widget
    QVBoxLayout *layout = new QVBoxLayout();
    central->setLayout(layout);
}
```

**QMainWindow 的结构**：菜单栏、工具栏、中心区域、状态栏。内容只能放在中心区域。

---

### 27. connect 四参数

```cpp
connect(_btn, &QPushButton::clicked, this, &MainWindow::onPrintTree);
//      ①          ②                 ③          ④
//      发送者      信号              接收者      槽
//      (对象指针)  (成员函数指针)     (对象指针)  (成员函数指针)
```

---

### 28. private slots

```cpp
class MainWindow : public QMainWindow {
private slots:
    void onPrintTree();   // 只被信号触发，外部不需要手动调用
};
```

---

### 29. qDebug()

```cpp
qDebug() << "对象名:" << obj->objectName()
         << "类型:" << obj->metaObject()->className();
```

在 Qt Creator 的 Application Output 面板查看输出。

---

### 30. children() / metaObject()

```cpp
const QObjectList &children = widget->children();   // const & 零拷贝
for (QObject *child : children) {
    qDebug() << child->objectName()
             << child->metaObject()->className();
}
```

---

### 31. layout 的 parent 自动管理

```cpp
QVBoxLayout *layout = new QVBoxLayout();   // 局部变量，不需要存为成员
layout->addWidget(_label);
_centralWidget->setLayout(layout);
// setLayout 内部把 layout 的 parent 设为 _centralWidget
// _centralWidget 销毁时自动 delete layout
```

---

### 32. 事件系统三层处理机制

Qt 中事件（鼠标、键盘、窗口等系统输入）的处理分为三层，按优先级从高到低：

```
事件到达目标对象
    │
    ▼
┌─ 第0层（外部）：eventFilter ──────── 别人拦截，不改目标代码
│      return true → 事件被吃掉，结束
│      return false ↓
│
├─ 第1层（内部-总入口）：event() ───── 所有事件的统一入口
│      return true → 结束
│      否则内部 switch 分发 ↓
│
└─ 第2层（内部-具体）：xxxEvent() ─── 处理某一类事件
       mousePressEvent / keyPressEvent / paintEvent / ...
```

**日常使用频率**：

| 层级 | 使用频率 | 典型场景 |
|------|---------|---------|
| 第2层 xxxEvent() | 90% | 处理自己的鼠标/键盘事件 |
| 第0层 eventFilter | 少量 | 监控/拦截别人的事件 |
| 第1层 event() | 极少 | 拦截 Tab 等在 event() 层被消费的特殊事件 |

---

### 32.1 第2层：重写 xxxEvent()（最常用）

重写父类的虚函数，处理自己的某一类事件：

```cpp
// mainwindow.h
class MainWindow : public QWidget {
protected:
    void mousePressEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;
};

// mainwindow.cpp
void MainWindow::mousePressEvent(QMouseEvent *event) {
    QPoint pos = event->pos();            // 点击坐标（相对于窗口）
    Qt::MouseButton btn = event->button(); // 哪个按键

    QString btnName;
    if (btn == Qt::LeftButton) btnName = "Left";
    else if (btn == Qt::RightButton) btnName = "Right";
    else btnName = "Middle";

    _labelMouse->setText(QString("鼠标：点击 (%1, %2)，按键：%3")
        .arg(pos.x()).arg(pos.y()).arg(btnName));
}

void MainWindow::keyPressEvent(QKeyEvent *event) {
    _labelKey->setText(QString("键盘：按下 [%1]，键码：%2")
        .arg(event->text()).arg(event->key()));
}
```

**关键字说明**：
- `protected`：虚函数重写放这里，不需要外部调用，只被 Qt 框架内部调用
- `override`：告诉编译器"我在重写父类虚函数"，拼错名字会编译报错（安全网）

---

### 32.2 第0层：eventFilter（拦截别人的事件）

**不修改目标对象的代码**，在外部监控/拦截它的事件：

```cpp
// 注册：让 MainWindow 监控 _btn 的事件
_btn->installEventFilter(this);
//  ↑ 目标（被监控者）       ↑ 过滤器（监控者）

// 实现过滤器
bool MainWindow::eventFilter(QObject *watched, QEvent *event) {
    if (watched == _btn) {
        if (event->type() == QEvent::MouseButtonPress) {
            _labelFilter->setText("过滤器：拦截到按钮的鼠标点击！");
            return true;    // 吃掉事件，_btn 收不到，clicked 不会发射
        }
        if (event->type() == QEvent::Enter) {
            _labelFilter->setText("过滤器：鼠标进入按钮区域");
            // 不 return true，让按钮正常高亮
        }
    }
    return QWidget::eventFilter(watched, event);  // 其他事件正常传递
}
```

**installEventFilter 的注册机制**：

```
目标->installEventFilter(监控者);

_btn 内部维护一个列表："谁在监控我的事件？"
调用后：_btn 的监控列表 = [MainWindow]
以后 _btn 收到事件时，Qt 先调用 MainWindow::eventFilter()
```

- 一个过滤器可以监控多个对象（用 `watched` 参数判断是谁）
- 一个对象可以被多个过滤器监控（后注册的先调用）
- 取消注册：`_btn->removeEventFilter(this);`

---

### 32.3 第1层：重写 event()（极少用）

所有事件的统一入口，在分发到 xxxEvent() 之前拦截：

```cpp
bool MainWindow::event(QEvent *event) {
    if (event->type() == QEvent::KeyPress) {
        QKeyEvent *ke = static_cast<QKeyEvent*>(event);
        if (ke->key() == Qt::Key_Tab) {
            qDebug() << "Tab 被拦截，不切焦点！";
            return true;   // 吃掉，不分发给 keyPressEvent
        }
    }
    return QWidget::event(event);  // 其他照常分发
}
```

**什么时候用**：Tab 键默认在 `event()` 层就被处理掉了（切焦点），根本到不了 `keyPressEvent`。如果你想拦截 Tab，只能在这里做。

---

### 32.4 完整流程示例

**用户点击 _btn 按钮时的事件流**：

```
用户点击 _btn
    │
    ▼
第0层：MainWindow::eventFilter(_btn, event)
    │   watched == _btn ✅
    │   event->type() == MouseButtonPress ✅
    │   return true → 事件被吃掉！
    │
    ├── 如果 return true：
    │   _btn 完全不知道被点了，clicked 不会发射
    │
    └── 如果 return false：
        │
        ▼
    第1层：_btn->event() → 内部 switch 分发
        │
        ▼
    第2层：QPushButton::mousePressEvent()
        → 按钮变按下状态 → 松开时发射 clicked()
```

**用户在窗口空白区域点击时**：

```
用户点击窗口空白
    │
    ▼
第0层：没人对 MainWindow 装过 eventFilter → 跳过
    │
    ▼
第1层：MainWindow::event() → 没重写，走 QWidget 默认 → switch 分发
    │
    ▼
第2层：MainWindow::mousePressEvent(event) → 你重写了，执行你的代码
```

---

### 32.5 事件 vs 信号的区别

| | 事件 | 信号槽 |
|--|------|--------|
| 来源 | 操作系统（用户输入） | 你的代码（emit） |
| 处理方式 | 重写虚函数 / eventFilter | connect 注册槽函数 |
| 层级 | 底层输入处理 | 高层业务逻辑 |
| 能否拦截 | 可以（return true / 不调父类） | 可以（disconnect） |
| 典型场景 | 鼠标拖拽、快捷键、窗口关闭确认 | 按钮点击、数据更新通知 |

**关系**：信号往往是事件的"上层包装"。例如 QPushButton 的 `clicked()` 信号，底层就是 `mousePressEvent` + `mouseReleaseEvent` 组合触发的。

---

### 33. QSS 样式表

QSS（Qt Style Sheets）语法类似 CSS，用于快速设置控件外观。

**三种使用方式**：

```cpp
// 方式1：给单个控件设样式
btn->setStyleSheet("background: #3498db; color: white; border-radius: 5px;");

// 方式2：给整个窗口设样式（所有子控件生效）
this->setStyleSheet("QPushButton { background: #3498db; color: white; }"
                    "QLabel { font-size: 14px; }");

// 方式3：从文件加载（大项目推荐）
QFile file(":/style.qss");
file.open(QFile::ReadOnly);
qApp->setStyleSheet(file.readAll());
```

**选择器**：

```css
QPushButton { }              /* 所有 QPushButton */
QPushButton#btnOK { }        /* objectName 为 btnOK 的按钮 */
QPushButton:hover { }        /* 鼠标悬停状态 */
QPushButton:pressed { }      /* 按下状态 */
QPushButton:disabled { }     /* 禁用状态 */
```

**常用属性**：

```css
background: #222;            /* 背景色 */
color: #fff;                 /* 文字颜色 */
font-size: 16px;             /* 字体大小 */
font-weight: bold;           /* 加粗 */
border: 2px solid #ccc;      /* 边框 */
border-radius: 8px;          /* 圆角 */
padding: 5px 10px;           /* 内边距 */
min-height: 40px;            /* 最小高度 */
```

**伪状态（交互反馈）**：

```cpp
btn->setStyleSheet(
    "QPushButton {"
    "  background: #3498db; color: white; border-radius: 5px; padding: 8px;"
    "}"
    "QPushButton:hover {"
    "  background: #2980b9;"
    "}"
    "QPushButton:pressed {"
    "  background: #1abc9c;"
    "}"
);
```

**QSS vs C++ API**：

| | QSS | C++ API |
|--|-----|---------|
| 颜色 | `background: red;` | `setPalette(...)` 繁琐 |
| 字体 | `font-size: 16px;` | `setFont(QFont("", 16))` |
| 圆角 | `border-radius: 5px;` | 只能靠 QPainter 自绘 |
| 适用场景 | 快速调外观 | 精确控制每一个像素 |

**原则**：改外观用 QSS 最快，自绘复杂图形用 QPainter。

---

## 四、对比 PySide6 速查

| C++ Qt6 | PySide6 | 说明 |
|---------|---------|------|
| `new QLabel("text", parent)` | `QLabel("text", parent)` | C++ 需要 new + 指针 |
| `label->setText("x")` | `label.setText("x")` | `->` vs `.` |
| `connect(btn, &QPushButton::clicked, this, &MyClass::onSlot)` | `btn.clicked.connect(self.on_slot)` | 四参数 vs 链式 |
| `Q_OBJECT` | 不需要 | Python 运行时处理 |
| `#include <QLabel>` | `from PySide6.QtWidgets import QLabel` | 头文件 vs import |
| `delete ui;` | 不需要 | Python 有 GC |
| `const QObjectList &children = w->children()` | `children = w.children()` | C++ 用 const & 避免拷贝 |