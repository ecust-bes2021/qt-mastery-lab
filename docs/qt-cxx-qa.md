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

### 4.5 成员函数名不会自动退化为指针

**普通函数**：函数名自动退化为函数指针（C 延续下来的规则）

```cpp
void freeFunc() { ... }

void (*p)() = freeFunc;    // ✅ 不加 & 也行，自动退化
void (*p)() = &freeFunc;   // ✅ 加 & 也行，等价
```

**成员函数**：必须显式用 `&` 取地址，不会自动退化

```cpp
class Widget {
    void onStart();
};

void (Widget::*p)() = &Widget::onStart;   // ✅ 必须写 &类名::函数名
void (Widget::*p)() = Widget::onStart;    // ❌ 编译错误
void (Widget::*p)() = onStart;            // ❌ 编译错误
```

**原因**：成员函数需要对象（隐含 this）才能调用，它的地址类型是 `void (Widget::*)()`，比普通函数指针复杂。C++ 标准规定不允许隐式转换，强制开发者明确写出归属。

**Qt connect 中的体现**：

```cpp
connect(_btnStart, &QPushButton::clicked, this, &Widget::onStart);
//                 ↑ 必须 & + 类名::信号            ↑ 必须 & + 类名::槽
```

| 函数类型 | 取地址方式 | 原因 |
|----------|-----------|------|
| 普通函数 | `funcName` 或 `&funcName` | 自动退化 |
| 成员函数 | 必须 `&ClassName::funcName` | C++ 语法强制 |

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

**使用规则**：在 .h 中只用了指针或引用时，前向声明够了；在 .cpp 中需要调用方法时才 #include。

| .h 中的使用方式 | 需要 #include？ | 前向声明够？ |
|----------------|:-:|:-:|
| `Worker *_worker;`（指针成员） | | ✅ |
| `void func(Worker &w);`（引用参数） | | ✅ |
| `Worker _worker;`（值成员） | ✅ | |
| `_worker->doWork();`（调用方法） | ✅ | |
| `class X : public Worker`（继承） | ✅ | |

**好处**：减少头文件间的依赖链，加快编译速度。A.h 改了不会导致所有 include A.h 的文件都重新编译。

**典型模式**：

```cpp
// widget.h
class Worker;              // 前向声明（.h 中只用指针）

class Widget : public QWidget {
    Worker *_worker;       // ✅ 指针，前向声明够了
};

// widget.cpp
#include "worker.h"        // .cpp 中要调用方法，必须 include
_worker->doWork();         // ✅ 编译器需要知道 Worker 的完整定义
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

### 34. `Qt::` 命名空间与枚举

**`Qt::` 是什么**：

Qt 框架将大量枚举常量集中放在 `Qt` 命名空间中，用有意义的名字代替魔法数字。

**常见分类**：

| 类别 | 举例 | 用途 |
|------|------|------|
| 数据角色 | `Qt::DisplayRole`, `Qt::EditRole`, `Qt::BackgroundRole` | Model/View 中区分"问什么" |
| Item 标志 | `Qt::ItemIsEnabled`, `Qt::ItemIsEditable` | 单元格能力 |
| 方向 | `Qt::Horizontal`, `Qt::Vertical` | 表头方向 |
| 对齐 | `Qt::AlignCenter`, `Qt::AlignLeft` | 文本对齐 |
| 颜色 | `Qt::red`, `Qt::blue` | 预定义颜色 |
| 画笔样式 | `Qt::SolidLine`, `Qt::DashLine` | QPainter 线型 |
| 键盘键 | `Qt::Key_Escape`, `Qt::Key_Return` | 事件系统按键识别 |

**为什么是 `Qt::ItemIsEnabled` 而不是 `Qt::ItemFlag::ItemIsEnabled`？**

Qt 使用的是传统**无作用域枚举**（`enum`），不是 C++11 的 `enum class`：

```cpp
// Qt 内部（简化）
namespace Qt {
    enum ItemFlag {          // 传统 enum，不是 enum class
        ItemIsEnabled = 1,
        ItemIsSelectable = 2,
        ItemIsEditable = 4,
    };
}
```

传统 `enum` 的枚举值**直接暴露到外层命名空间**，所以只需要 `Qt::ItemIsEnabled`，不需要再经过枚举类型名那一层。

**对比**：

| 枚举类型 | 语法 | 访问方式 |
|----------|------|----------|
| `enum ItemFlag { ... }` | 传统（Qt 用这种） | `Qt::ItemIsEnabled` |
| `enum class ItemFlag { ... }` | C++11 强类型 | `Qt::ItemFlag::ItemIsEnabled` |

Qt 诞生于 C++11 之前，一直沿用传统 enum，改了会破坏所有现有代码的兼容性。

### 35. QAtomicInteger 与内存顺序

**为什么需要原子操作**：

当两个线程读写同一个变量时（比如 UI 线程写停止标志，Worker 线程读标志），普通 `bool` 是数据竞争（未定义行为）。`QAtomicInteger<bool>` 保证读写是原子的（不会读到"写了一半"的值）。

**两组 API**：

| 写 | 读 | 额外保证 |
|----|----|---------| 
| `storeRelaxed(value)` | `loadRelaxed()` | 无（只保证原子性） |
| `storeRelease(value)` | `loadAcquire()` | 对周围普通变量的可见性有保证 |

**Relaxed（只保证原子性）**：

```cpp
_stopFlag.storeRelaxed(true);   // 原子写：其他线程能读到 true
_stopFlag.loadRelaxed();         // 原子读：不会读到"写了一半"的值
```

适用场景：只有一个共享标志位，没有其他需要同步的数据。

**Release/Acquire（保证周围普通变量的可见性）**：

```cpp
// 线程A（生产者）
_result = 42;                       // 普通写
_ready.storeRelease(true);          // 原子写 + 保证 _result=42 对其他线程可见

// 线程B（消费者）
if (_ready.loadAcquire()) {         // 原子读
    use(_result);                   // 保证能看到 42（不会看到旧值）
}
```

**关键理解**：Release/Acquire 操作的还是同一个原子变量（`_ready`），它本身不"存储其他数据"。它的作用是**充当内存屏障**，保证"Release 之前的所有普通写入"对"Acquire 之后的所有普通读取"可见。

**为什么需要这个保证？**：CPU 为了性能会重排指令。没有屏障时，线程B 可能先读到 `_ready==true`，但 `_result` 还没从线程A 同步过来（看到旧值）。

**选择指南**：

| 场景 | 推荐 |
|------|------|
| 单纯的开关标志（如停止标志） | `Relaxed` |
| 通过标志同步其他数据（如"数据准备好了"） | `Release` + `Acquire` |

### 36. moveToThread 与 parent 的关系

**规则**：`moveToThread` 要求对象**不能有 parent**。

**原因**：Qt 对象树要求 parent 和 child 必须在同一线程。如果 child 有 parent（在主线程），你把 child 移到子线程 → parent-child 跨线程 → parent 析构时跨线程 delete child = 崩溃。

```cpp
_worker = new Worker(this);      // ❌ 有 parent
_worker->moveToThread(_thread);  // Qt 报 warning，不生效

_worker = new Worker();          // ✅ 无 parent
_worker->moveToThread(_thread);  // 正常
```

**那内存谁管？**：没有 parent 就不在对象树里，不会被自动 delete。用 `deleteLater` 安排清理：

```cpp
connect(_worker, &Worker::finished, _worker, &Worker::deleteLater);
```

**为什么构造函数还保留 `parent = nullptr` 参数？**

```cpp
explicit Worker(QObject *parent = nullptr);
```

这是 Qt 类的惯例格式，传 `nullptr` 等于没有 parent。保留参数的目的：
- Qt 代码风格统一（所有 QObject 子类都这么写）
- 灵活性（万一某些场景不需要 moveToThread，可以直接挂树）
- Qt Creator 模板自动生成

完全可以写成 `explicit Worker();`，功能一样。

### 37. deleteLater 的执行时机

**是什么**：QObject 提供的函数，作用是"把 delete 操作延迟到事件循环的下一轮执行"。

**为什么不直接 delete**：

```cpp
emit finished();
// ← 此刻 Worker 还在执行代码（刚 emit 完，还没从函数返回）
// 如果这时候 delete Worker → 正在执行的对象被删了 → 崩溃
```

**deleteLater 的执行流程**：

```
Worker::doWork() 执行中
  → emit finished()
  → 触发 deleteLater()（注册"待删除"事件到事件队列）
  → doWork() 正常 return
  → 事件循环取下一个事件："删除 Worker"
  → 此时 Worker 没有代码在跑，安全 delete ✅
```

**使用场景**：任何"对象正在参与信号槽执行时需要被删除"的情况都用 `deleteLater`，不要直接 `delete`。

---

### 38. Qt Plugin 系统

**是什么**：Qt 提供的动态库加载机制，让主程序在运行时加载 `.dll`（或 `.so`），获得新功能，而不需要重新编译主程序。

**核心设计思想**：接口与实现分离。

```
主程序（Host）
  │ 只知道接口（纯虚类），不知道具体实现
  │ 运行时通过 QPluginLoader 加载 .dll
  ▼
Plugin（.dll）
  实现了接口的所有纯虚函数
  通过 Q_INTERFACES + Q_PLUGIN_METADATA 注册
```

**三个关键角色**：

| 角色 | 职责 | 代码所在 |
|------|------|---------|
| 接口（Interface） | 纯虚类，定义"能做什么" | 独立头文件，主程序和 Plugin 都 include |
| Plugin 实现 | 继承 QObject + 接口，真正做事 | 编译为 .dll |
| 主程序加载 | QPluginLoader 加载 .dll，qobject_cast 转为接口指针 | 主程序 |

**代码骨架**：

```cpp
// ① 接口定义（纯虚类）
class MyPluginInterface
{
public:
    virtual ~MyPluginInterface() {}
    virtual QString name() const = 0;
    virtual QWidget* createWidget(QWidget *parent) = 0;
};
Q_DECLARE_INTERFACE(MyPluginInterface, "com.example.MyPluginInterface/1.0")

// ② Plugin 实现（编译为 .dll）
class LedPlugin : public QObject, public MyPluginInterface
{
    Q_OBJECT
    Q_INTERFACES(MyPluginInterface)
    Q_PLUGIN_METADATA(IID "com.example.MyPluginInterface/1.0" FILE "ledplugin.json")
public:
    QString name() const override { return "LedIndicator"; }
    QWidget* createWidget(QWidget *parent) override {
        return new LedIndicator(parent);
    }
};

// ③ 主程序加载
QPluginLoader loader("plugins/ledplugin.dll");
QObject *obj = loader.instance();
MyPluginInterface *plugin = qobject_cast<MyPluginInterface*>(obj);
if (plugin) {
    QWidget *led = plugin->createWidget(this);
}
```

**关键要点**：
- `Q_PLUGIN_METADATA` 必须带一个 `.json` 文件（哪怕是空的 `{}`），Qt 用它做元数据
- IID 字符串带版本号（如 `/1.0`），接口变了改版本号，旧 Plugin 不会误加载
- 主程序不需要 `#include` Plugin 的头文件，只需要接口头文件

**适用场景**：
- 多芯片系列的烧录协议（每个芯片一个 Plugin）
- 多种测试项（每个测试类型一个 Plugin）
- 主程序框架固定，功能通过 Plugin 热插拔扩展

---

### 39. Qt Designer 集成与自定义控件使用方式

#### 39.1 背景：Qt Designer 是什么

Qt Designer 是一个**独立的 GUI 设计工具**（`designer.exe`），提供可视化拖拽界面设计：
- 左侧面板：控件列表（QPushButton、QLabel 等）
- 中间画布：拖拽控件、调整位置
- 右侧面板：属性编辑器
- 保存结果：`.ui` 文件（XML 格式），编译时由 UIC 工具转成 C++ 代码

#### 39.2 方式一：Plugin 方式（完整集成）

**目标**：让自定义控件出现在 Designer 左侧面板中，可以拖拽使用，且画布上能**实时预览真实外观**。

**完整流程**：

```
第 1 步：准备自定义控件源码
    已有 ledindicator.h / ledindicator.cpp（正常的自定义控件）

第 2 步：创建 Designer Plugin 项目（独立项目）
    新建项目，包含：
    ├── 控件源码（ledindicator.h/.cpp，拷贝或引用）
    ├── Plugin 适配类（ledindicatorplugin.h/.cpp）
    └── 元数据文件（ledindicatorplugin.json，可以是空的 {}）

第 3 步：编写 Plugin 适配类
    继承 QObject + QDesignerCustomWidgetInterface
    实现以下方法告诉 Designer 关于控件的信息：
      name()         → 控件类名（"LedIndicator"）
      group()        → 面板分组名（"Custom Widgets"）
      toolTip()      → 鼠标悬停提示
      whatsThis()    → 详细说明
      icon()         → 面板图标
      isContainer()  → 是否是容器控件（能否往里拖子控件）
      createWidget() → 创建真实控件实例（Designer 拖到画布时调用）
      domXml()       → .ui 文件中该控件的默认 XML 描述
      includeFile()  → UIC 生成代码时需要 include 的头文件路径

第 4 步：CMakeLists.txt 配置
    编译目标为共享库（add_library SHARED），不是可执行文件
    链接 Qt6::Widgets + Qt6::Designer

第 5 步：编译
    得到 ledindicatorplugin.dll

第 6 步：部署
    将 dll 放到 Qt 安装目录/plugins/designer/ 下
    或设置环境变量 QT_PLUGIN_PATH 指向自定义目录

第 7 步：验证
    启动 designer.exe → 左侧面板出现 "Custom Widgets" 分组
    拖拽 LedIndicator 到画布 → 能看到真实的 LED 灯外观
    保存 → 生成 .ui 文件

第 8 步：在项目中使用 .ui 文件
    UIC 工具读取 .ui → 生成 ui_xxx.h
    生成的代码会 #include "ledindicator.h" 并 new LedIndicator(parent)
    你的项目 CMakeLists.txt 中需要包含 ledindicator.h/.cpp 源码
    注意：最终 exe 运行时不需要 plugin dll（控件代码已编译进 exe）
```

**关键理解**：Designer 是已编译好的 exe，它不能编译你的源码。所以需要 Plugin dll 让它在运行时能创建你的控件实例来预览。但你自己的项目编译时是直接编译源码的，不需要这个 dll。

---

#### 39.3 方式二：提升控件（Promoted Widget，轻量级）

**目标**：在 Designer 的 `.ui` 文件中使用自定义控件，但**不需要编写 Plugin、不需要编译 dll**。

**代价**：Designer 画布上只能看到一个占位方块，无法预览真实外观。编译运行后外观正确。

**完整流程**：

```
第 1 步：在 Designer 中拖一个基类控件到画布
    例如拖一个 QWidget（因为 LedIndicator 继承自 QWidget）

第 2 步：右键该控件 → "提升为..."（Promote to...）

第 3 步：在弹出对话框中填写
    提升的类名：LedIndicator
    头文件：    ledindicator.h
    基类：      QWidget（自动识别）

第 4 步：点击"添加" → "提升" → 确认

第 5 步：保存 .ui 文件
    .ui 中会记录：
      <widget class="LedIndicator" ...>
      <customwidgets>
        <customwidget>
          <class>LedIndicator</class>
          <extends>QWidget</extends>
          <header>ledindicator.h</header>
        </customwidget>
      </customwidgets>

第 6 步：编译你的项目
    UIC 读取 .ui → 生成代码 #include "ledindicator.h" + new LedIndicator(parent)
    你的 CMakeLists.txt 中包含 ledindicator.h/.cpp 源码即可
    运行后外观完全正确
```

**优势**：零额外工作量，只需要在 Designer 中右键操作两下。
**劣势**：设计时看不到真实外观，只能看到基类（QWidget）的空白方块。

---

#### 39.4 方式三：纯代码布局（不用 Designer）

**目标**：完全不用 `.ui` 文件，直接在代码中创建控件和布局。

**做法**：就是我们一直在做的方式：

```
在构造函数中：
  _led = new LedIndicator(this);
  _led->setLabel("电源");
  auto *layout = new QVBoxLayout(this);
  layout->addWidget(_led);
```

不需要 Designer，不需要 .ui 文件，不需要 Plugin，不需要 UIC。

---

#### 39.5 三种方式对比总结

| 维度 | Plugin 集成 | 提升控件（Promoted） | 纯代码布局 |
|------|-------------|---------------------|-----------|
| 需要写 Plugin 类 | ✅ 需要 | ❌ 不需要 | ❌ 不需要 |
| 需要编译 dll | ✅ 需要 | ❌ 不需要 | ❌ 不需要 |
| Designer 中能预览真实外观 | ✅ 能 | ❌ 只有占位框 | — 不使用 Designer |
| 使用 .ui 文件 | ✅ | ✅ | ❌ |
| 开发效率 | 低（前期投入大） | 中（右键提升即可） | 高（直接写代码） |
| 适合动态布局 | ❌ | ❌ | ✅ |
| 灵活性 | 低 | 中 | 高 |
| Git 友好度 | — | 差（.ui 是 XML，diff 难看） | 好（纯代码，diff 清晰） |

#### 39.6 使用时机建议

| 你的场景 | 推荐方式 |
|---------|---------|
| 一个人开发工具 | **纯代码布局** |
| 用 Designer 设计界面 + 自定义控件 | **提升控件** |
| 做控件库给团队/客户用 | **Plugin 集成** |
| UI 设计师（不写代码）需要用你的控件 | **Plugin 集成** |
| 控件还在频繁迭代中 | **纯代码布局**或**提升控件** |
| 控件已稳定 + 大量项目复用 | **Plugin 集成** |

---

### 40. pybind11（Python 调用 C++ 的主流方案）

**是什么**：一个 C++ 头文件库（header-only），让你用 C++ 编写 Python 扩展模块。编译后生成 `.pyd`（Windows）或 `.so`（Linux），Python 端直接 `import` 使用。

**核心优势**：
- 能绑定 C++ 类（不仅限于 C 函数）
- 自动类型转换（Python list ↔ std::vector, str ↔ std::string 等）
- 自动生命周期管理（Python GC 回收时自动 delete C++ 对象）
- 语法简洁，绑定代码量少

**完整流程**：

```
开发阶段：
  1. 写纯 C++ 代码（业务逻辑，和 Python 无关）
  2. 写 bindings.cpp（绑定代码，告诉 pybind11 暴露哪些类/方法）
  3. 写 setup.py + pyproject.toml（构建配置）

编译阶段（uv pip install .）：
  1. setuptools 读取 setup.py，找到要编译的 .cpp 文件
  2. 调用 C++ 编译器（MSVC/GCC）编译 .cpp → .obj
  3. 链接 .obj + python3xx.lib → 生成 crc_module.pyd
  4. 安装到虚拟环境的 site-packages 中

运行阶段（import crc_module）：
  1. Python 加载 .pyd 动态库
  2. pybind11 注册的类/函数出现在 Python 命名空间中
  3. Python 调用方法 → pybind11 转换参数类型 → 调用 C++ 方法
  4. C++ 返回值 → pybind11 转换回 Python 类型 → 返回给 Python
  5. Python 对象被 GC 回收时 → pybind11 自动 delete C++ 对象
```

**绑定代码核心语法**：

| 语法 | 作用 |
|------|------|
| `PYBIND11_MODULE(模块名, m)` | 定义 Python 模块入口 |
| `py::class_<C++类>(m, "Python类名")` | 注册 C++ 类 |
| `.def(py::init<参数类型>())` | 绑定构造函数 |
| `.def("方法名", &类::方法)` | 绑定成员方法 |
| `.def_property_readonly("名", &getter)` | 绑定只读属性 |
| `m.def("函数名", &函数)` | 绑定独立函数 |
| `py::arg("参数名") = 默认值` | 指定参数名和默认值 |

**自动类型转换表**（需要 `#include <pybind11/stl.h>`）：

| Python | C++ | 方向 |
|--------|-----|------|
| `str` | `std::string` | 双向 |
| `int` | `int / uint8_t / uint16_t / ...` | 双向 |
| `float` | `double / float` | 双向 |
| `bool` | `bool` | 双向 |
| `list` | `std::vector` | 双向 |
| `dict` | `std::map / std::unordered_map` | 双向 |
| `None` | `void`（返回值） | C++ → Python |

**项目结构**：

| 文件 | 职责 |
|------|------|
| `xxx.h / xxx.cpp` | 纯 C++ 业务代码（不依赖 pybind11） |
| `bindings.cpp` | 绑定代码（桥梁/翻译官） |
| `setup.py` | 构建配置（告诉编译器怎么编译） |
| `pyproject.toml` | 项目元信息 + 构建系统声明 |

**适用场景**：
- 你自己写的 C++ 代码，想暴露给 Python 使用
- 需要绑定 C++ 类、复杂数据结构
- 性能热点代码（大文件解析、CRC 计算、协议解析等）

**MSVC 注意事项**：MSVC 默认使用 GBK 代码页，C++ 源文件中的中文字符串会导致编译错误。解决方案：
- 传给 pybind11 的 docstring 使用英文
- 在 setup.py 中添加 `/utf-8` 编译选项

---

### 41. ctypes（Python 调用 C 动态库）

**是什么**：Python 标准库自带的模块，可以直接加载 `.dll`（或 `.so`）并调用里面的 C 函数。不需要安装任何额外库。

**工作原理**：

```
已有的 C 动态库（mylib.dll）
        ↓
Python: ctypes.CDLL("mylib.dll")
        ↓
手动声明参数类型和返回类型
        ↓
调用函数
```

**使用示例**：

```python
import ctypes

lib = ctypes.CDLL("./mylib.dll")

# 必须手动声明参数类型和返回类型
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

result = lib.add(3, 5)  # 调用 C 的 int add(int a, int b)
```

**关键限制**：
- 只能调**纯 C 函数**（C 的 ABI 是稳定的，C++ 的不是）
- C++ 类、模板、重载函数 → 不能直接调，必须先包一层 `extern "C"` 接口
- 所有参数类型、返回类型必须手动声明（Python 不知道 dll 的函数签名）
- 内存管理完全手动（容易泄漏或崩溃）
- 不支持自动类型转换（vector、string 等需要手动处理）

**适用场景**：
- 调用**已有的 C 动态库**（芯片厂商提供的 SDK .dll、系统 API 等）
- 你**没有源码**，只有一个 .dll 文件
- 接口简单、函数少

---

### 42. pybind11 vs ctypes 对比

| 维度 | pybind11 | ctypes |
|------|----------|--------|
| 能调 C 函数 | ✅ | ✅ |
| 能调 C++ 类 | ✅ 直接支持 | ❌ 需要包 C 接口 |
| 类型自动转换 | ✅ | ❌ 全部手动 |
| 内存管理 | ✅ 自动（GC 联动） | ❌ 手动 delete |
| 错误处理 | ✅ C++ 异常 → Python 异常 | ❌ 段错误直接 crash |
| 需要源码 | ✅ 需要 | ❌ 不需要 |
| 需要编译 | ✅ 编译成 .pyd | ❌ 直接加载 .dll |
| 安装依赖 | pip install pybind11 | 无（标准库） |
| Python 端体验 | 像原生 Python 类 | 像调外部函数 |

**选择建议**：

| 场景 | 用什么 |
|------|--------|
| 你能控制 C++ 源码 | **pybind11** |
| 只有 .dll 没有源码 | **ctypes** |
| 绑定 C++ 类 | **pybind11** |
| 调芯片厂商 SDK | **ctypes**（通常只有 .dll） |
| 追求 Python 端使用体验 | **pybind11** |

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