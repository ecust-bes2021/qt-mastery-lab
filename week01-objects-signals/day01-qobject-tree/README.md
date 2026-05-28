# Day 01 - QObject Tree and Ownership

## Problem Understanding

Before writing signal-heavy PySide6 tools, you need to understand what owns what. In Qt, object lifetime is not only Python reference counting. QObject has its own parent-child tree, and many UI bugs come from confusing Python references with Qt ownership.

## Today's Target

By the end of today, you should be able to explain and demonstrate:

- A parent QObject destroys its children.
- Removing or changing a parent changes the lifetime responsibility.
- `destroyed` signals can be used to observe lifetime, but should not become business logic.
- Python variables are references to wrappers; they are not the same thing as Qt object ownership.

## Minimal Exercise Shape

Create your own small PySide6 console or widget demo in `src/`.

Recommended shape:

```text
src/
└── qobject_tree_probe.py
```

The demo should create one parent object and at least two child objects, print their parent relationship, connect to `destroyed`, then delete the parent and observe the destruction order.

Do not optimize the UI. The point is ownership and observability.

## Verification

Run the script and prove these points from output:

- children report the expected parent before deletion
- deleting the parent emits destruction observations for children
- a child without parent is not destroyed by deleting the original parent

## Engineering Trade-Offs

Qt parent-child ownership is convenient for UI composition, but it can hide lifetime decisions. For production tools, parent ownership is good for visual widgets and short-lived dialogs; explicit ownership and clear cleanup are safer for hardware sessions, worker objects, and protocol state.

## Minimal Next Step

Write only the ownership probe first. Do not add signals/slots beyond `destroyed` until the lifetime behavior is clear.
