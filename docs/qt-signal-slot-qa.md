# Qt / PySide6 Q&A

---

## 信号与槽

### Q1: 一个信号连接多个槽时，槽函数的执行顺序是怎样的？

**答：在同线程下，按 connect 的调用顺序依次同步执行。**

### 关键机制：ConnectionType

`connect` 有一个隐藏的参数决定调用行为：

```python
signal.connect(slot, type=Qt.ConnectionType.AutoConnection)  # 默认值
```

| ConnectionType | 行为 | 适用场景 |
|---------------|------|---------|
| `DirectConnection` | emit 时立即同步调用槽，等同普通函数调用 | 信号和槽在同一线程 |
| `QueuedConnection` | emit 时把调用投递到接收者线程的事件队列，等事件循环处理 | 信号和槽在不同线程 |
| `AutoConnection`（默认） | Qt 自动判断：同线程 → Direct，跨线程 → Queued | 绝大多数情况 |

### 同线程下的执行流程（DirectConnection）

```python
self.action_signal.connect(self._on_action_slot1)  # 先连
self.action_signal.connect(self._on_action_slot2)  # 后连
```

```
self.action_signal.emit("Action!")
│
├── 同步调用 _on_action_slot1("Action!")   ← 必须执行完
├── 同步调用 _on_action_slot2("Action!")   ← 才轮到这个
│
└── emit 返回  ← 所有槽都执行完了才返回
```

### 工程原则

- emit 在 DirectConnection 下是**阻塞的**，等所有槽执行完才返回
- 不要在设计上依赖 connect 顺序——把多个槽视为独立观察者
- 如果两个动作有先后依赖，应该放在同一个槽里按顺序写，而非拆成两个槽

---

### Q2: Signal(int) 为什么必须定义在 class body 而不能写在 __init__ 里？

**答：PySide6 的元类机制需要在类创建时注册信号。**

Qt 的信号是元对象系统（Meta-Object System）的一部分。PySide6 在类定义阶段（metaclass 处理时）扫描 class body 中的 Signal 描述符并注册。如果写在 `__init__` 里，类已经创建完成，注册时机已过，信号无法正常工作。

```python
# ✅ 正确：class body
class MyWidget(QWidget):
    my_signal = Signal(int)

# ❌ 错误：__init__ 里
class MyWidget(QWidget):
    def __init__(self):
        self.my_signal = Signal(int)  # 不会被注册为信号
```

---

### Q3: 槽函数的参数和信号参数的关系是什么？

**答：emit 的参数 = 实参，槽函数的参数 = 形参。本质就是一次函数调用。**

规则：
- 槽的参数数量 ≤ 信号的参数数量（多余的参数被丢弃）
- 槽的参数数量不能 > 信号的参数数量（给不够会崩溃）
- 类型要匹配

```python
Signal(str, int)  →  def slot(self, text: str, count: int):  # ✅ 完全匹配
Signal(str, int)  →  def slot(self, text: str):              # ✅ 丢弃 int
Signal(str, int)  →  def slot(self):                         # ✅ 全部丢弃
Signal()          →  def slot(self, value: int):             # ❌ 信号给不出 int
```

---

### Q4: 三个不同签名的信号能连接到同一个槽函数吗？

**答：不能直接连，但可以通过适配层解决。**

### 方式 A：lambda 适配

```python
self.no_arg_signal.connect(lambda: self._display("收到无参信号"))
self.int_signal.connect(lambda v: self._display(f"收到int: {v}"))
self.multi_signal.connect(lambda t, c: self._display(f"{t}: {c}"))

def _display(self, msg: str):
    self._label.setText(msg)
```

### 方式 B：独立槽函数（推荐）

```python
def _on_no_arg(self):
    self._label.setText("收到无参信号")

def _on_int(self, value: int):
    self._label.setText(str(value))

def _on_multi(self, text: str, count: int):
    self._label.setText(f"{text}: {count}")
```

### 选择建议

| | lambda 适配 | 独立槽函数 |
|---|---|---|
| 优点 | 代码紧凑 | 可读性好、可调试、可单独 disconnect |
| 缺点 | traceback 不清晰、无法精确 disconnect | 代码量稍多 |
| 适合 | 简单格式转发 | 有业务逻辑、需要动态断连 |

---

### Q5: 在多信号连一槽的场景中，如何区分是哪个信号（或哪个对象）触发的？

**答：两种方式。**

### 方式 1：self.sender()

```python
def _on_any_button_clicked(self):
    btn = self.sender()  # 返回发射信号的对象
```

注意事项：

| 场景 | `self.sender()` 行为 |
|------|---------------------|
| 同线程 DirectConnection | ✅ 正确返回发射者 |
| 跨线程 QueuedConnection | ⚠️ 可能返回 `None`（发射者可能已被销毁） |
| 不在槽函数执行期间调用 | 返回 `None` |

结论：简单 UI 场景下够用，正式项目推荐方式 2。

### 方式 2：lambda / functools.partial 绑定标识（推荐）

```python
self._btn_a.clicked.connect(lambda: self._on_click("A"))
self._btn_b.clicked.connect(lambda: self._on_click("B"))

def _on_click(self, source: str):
    self._label.setText(f"来自: {source}")
```

显式传参，不依赖运行时状态，更安全。

---

### Q6: 重复 connect 和重复 disconnect 会怎样？

**答：重复 connect 导致槽被多次调用（静默），重复 disconnect 抛 RuntimeError（崩溃）。**

#### 重复 connect

```python
self.notify.connect(self._on_notify)
self.notify.connect(self._on_notify)   # 不报错

self.notify.emit("Hello!")
# _on_notify 被调用 2 次
```

Qt 不会去重，connect 几次就存几条。常见触发场景：用户多次点击"连接"按钮。

#### 重复 disconnect

```python
self.notify.disconnect(self._on_notify)   # 成功
self.notify.disconnect(self._on_notify)   # RuntimeError!
```

第二次找不到连接记录，直接抛异常。

#### 对比

| | 重复 connect | 重复 disconnect |
|---|---|---|
| 行为 | 静默成功，多加一条 | 抛 RuntimeError |
| 危险性 | 隐性 bug，难发现 | 直接崩溃（如果没 catch） |

#### 防御方式

```python
# 方式1：先断再连（保证只有一条）
try:
    self.notify.disconnect(self._on_notify)
except RuntimeError:
    pass
self.notify.connect(self._on_notify)

# 方式2：UniqueConnection（Qt 官方防重复）
self.notify.connect(self._on_notify, Qt.ConnectionType.UniqueConnection)

# 方式3：disconnect 用 try/except 保护
try:
    self.notify.disconnect(self._on_notify)
except RuntimeError:
    pass
```

---

### Q7: emit 之后槽函数在哪个线程执行？取决于什么？

**答：取决于 ConnectionType。**

| ConnectionType | 槽在哪执行 | 何时使用 |
|---------------|-----------|---------|
| `DirectConnection` | 发射者所在线程（同步调用） | 同线程，或你明确要同步 |
| `QueuedConnection` | 接收者所在线程（异步，等事件循环处理） | 跨线程 |
| `AutoConnection`（默认） | Qt 自动判断：同线程→Direct，跨线程→Queued | 绝大多数情况 |

关键规则：**只有主线程能安全操作 UI 控件。** 子线程的信号通过 Queued 回到主线程更新 UI。

---

### Q8: 信号槽能跨进程使用吗？

**答：不能。信号槽只在同一进程内工作。**

原因：
- DirectConnection 依赖共享地址空间（跨进程没有）
- QueuedConnection 依赖同一进程的事件循环（另一个进程有自己的事件循环）

跨进程需使用 IPC 方案（QLocalSocket、multiprocessing.Queue、共享内存等），再在进程内部用信号槽桥接到 UI。

---

## Python 基础

### Q6: 位置参数和关键字参数有什么区别？`/` 和 `*` 在函数签名中是什么意思？

**答：位置参数靠"排第几"对应，关键字参数靠"叫什么名"对应。`/` 和 `*` 是设计者强制调用方式的约束工具。**

#### 两种传参方式

```python
def greet(name, msg):
    print(f"{name}: {msg}")

greet("Alice", "Hello")          # 位置参数：按顺序对应
greet(msg="Hello", name="Alice") # 关键字参数：按名字对应，顺序无所谓
```

#### `/` 和 `*` 的含义

```python
def func(a, b, /, c, d, *, e, f):
#        ^^^^      ^^^^      ^^^^
#      仅位置     普通参数    仅关键字
```

| 标记 | 作用范围 | 含义 |
|------|---------|------|
| `/` | 左边的参数 | 仅位置参数（positional-only），不能用 `name=value` |
| `*` | 右边的参数 | 仅关键字参数（keyword-only），必须用 `name=value` |

#### 设计意图

- **`/` 左边**：参数名不是 API 契约，设计者将来可能改名
- **`*` 右边**：参数多时防止搞混，强制调用者写明含义

#### 实际例子

```python
len([1, 2, 3])        # ✅ positional-only
len(obj=[1, 2, 3])    # ❌

print("a", "b", sep="-", end="\n")   # ✅ sep/end 是 keyword-only
print("a", "b", "-", "\n")           # ❌ "-" 会被当成要打印的内容
```

#### 与 PySide6 的关系

PySide6 的 C++ 绑定函数基本都是 positional-only（`/` 左边），所以直接按位置传参即可：

```python
QSlider(Qt.Orientation.Horizontal)   # ✅ 直接传位置
QSlider(orientation=Qt.Orientation.Horizontal)  # ❌ 大多数情况不支持
```