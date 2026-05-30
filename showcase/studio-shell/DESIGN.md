# Studio Shell Design

## 1. Project Positioning

`studio-shell` is a Phase 1 integration project for `qt-mastery-lab`.

It should become a small open-source Qt desktop framework demo that shows how to build an extensible engineering-tool style application. It is not meant to be a generic AI product shell, and it should not contain company-specific code, protocols, logs, register maps, or private workflow details.

The intended public-facing message is:

> A Qt/PySide6 engineering tool shell that demonstrates plugin-style tool panels, disciplined shared state, worker-thread execution, and maintainable desktop application boundaries.

## 2. Relationship to qt-mastery-lab

The weekly folders are for fundamentals. `studio-shell` is for composition.

| Weekly Track | Mechanism | How It Enters Studio Shell |
|---|---|---|
| W1 QObject + signals/slots | ownership, signal-slot delivery | `AppContext`, tool lifecycle, cross-tool notifications |
| W2 Event system | event loop, filters, custom events | navigation behavior, UI event boundaries, diagnostics hooks |
| W3 Paint + layout | custom widgets, layout constraints | polished shell layout, status panels, log views |
| W4 Model/View | scalable data presentation | log table, data inspector, task list, project tree |
| W5 Threading | worker objects, queued signals | slow file/API/mock-device tasks without blocking UI |
| W6 QML / Qt Quick | optional modern UI frontend | optional experiment, not required for V0 |
| W7 OpenGL / performance | high-volume rendering | optional waveform/data visualization panel |
| W8 Packaging | deployable desktop app | Windows packaging, resources, runtime notes |

This project should not replace the weekly exercises. It should start after enough weekly mechanisms are understood to explain the design choices.

## 3. PySide6 and Qt6 C++ Boundary

The architecture is Qt-first, not PySide6-only.

| Concept | PySide6 Shape | Qt6 C++ Shape |
|---|---|---|
| Tool panel | `QWidget` subclass | `QWidget` subclass |
| Tool contract | abstract base class / protocol | pure virtual interface |
| Shared context | `QObject` singleton or owned service | `QObject` service owned by application root |
| State payload | `dict`, dataclass, JSON-like objects | `QJsonObject`, `QVariantMap`, typed structs |
| Signals | `Signal(...)` | `signals:` section |
| Dynamic loading | registry / `importlib` later | static registration first, `QPluginLoader` later |
| Persistence | `QSettings`, SQLite | `QSettings`, `QSqlDatabase` |
| Slow work | `QObject + moveToThread` | `QObject + moveToThread` |

Important rule: PySide6 can be the first implementation, but design explanations should identify which parts are Qt concepts and which parts are Python binding conveniences.

## 4. V0 Scope

V0 should be small enough to finish and explain.

Required:

- `QMainWindow` shell with left navigation and stacked tool area
- static tool registration, no runtime plugin loading yet
- `ToolPlugin` contract with name, icon/key, widget, activate, deactivate, state export
- disciplined `AppContext` with only truly shared application state
- one log/diagnostics panel
- one mock long-running task routed through worker-thread signals
- one simple settings flow using `QSettings`
- README screenshots after W8 packaging polish

Suggested demo tools:

| Tool | Purpose |
|---|---|
| Log Viewer | Model/View, filtering, engineering diagnostics |
| Task Runner | worker thread, progress, cancellation boundary |
| Data Inspector | table/tree model, data roles, selection behavior |
| Settings Panel | shared config, theme/font options, persistence |

## 5. Non-Goals for V0

Do not add these in the first version:

- real AI API integration
- real serial/I2C/SPI/JTAG hardware access
- company-specific protocols or data formats
- dynamic binary plugin loading
- remote update system
- complex theme engine
- QML rewrite
- compatibility or fallback layers not required by the demo contract

These are not bad features. They are postponed because V0's goal is to prove architecture and Qt fundamentals, not product breadth.

## 6. Architecture Sketch

```text
studio-shell/
├── app shell
│   ├── main window
│   ├── navigation
│   └── stacked tool area
├── core services
│   ├── app context
│   ├── tool registry
│   ├── settings service
│   └── logging service
├── tools
│   ├── log viewer
│   ├── task runner
│   ├── data inspector
│   └── settings panel
└── infrastructure
    ├── worker-thread helper
    ├── model/view helpers
    └── resource packaging
```

The shell owns tool lifetime. Tools should not own each other. Cross-tool communication must go through a small, explicit service or signal contract.

## 7. AppContext Constraint

`AppContext` is useful, but it is also the highest-risk part of the design.

Allowed in `AppContext`:

- current project identity
- selected demo data source
- global settings snapshot
- theme/font selection
- shared logging/event signal
- service accessors that are stable application-level concepts

Avoid in `AppContext`:

- every widget's local state
- every tool's private fields
- temporary UI selections that matter only inside one panel
- business logic that belongs to a tool or service
- arbitrary signal growth without naming discipline

The principle is: shared state must be shared for a reason, not because it is convenient.

## 8. Milestones

| Milestone | Timing | Output |
|---|---|---|
| M0 Design Seed | Now | this document and empty project skeleton |
| M1 Shell Prototype | after W1-W3 | main window, navigation, static tool panels |
| M2 Data UI | after W4 | log/data inspector using Model/View |
| M3 Long Task Flow | after W5 | worker-thread task runner with progress/error/finish |
| M4 Polish + Packaging | after W8 | screenshots, README, packaged Windows demo |

## 9. GitHub Display Standard

Before this becomes a portfolio item, it should have:

- clear README with problem statement and screenshots
- architecture diagram or concise architecture section
- small runnable demo data, no private data
- setup and run commands
- explanation of PySide6 versus Qt6 C++ design transfer
- notes on threading and UI-thread safety
- known limitations and explicit non-goals

## 10. Minimal Next Step

Do not implement the shell immediately.

During each weekly exercise, add only short notes about how that mechanism will later map into `studio-shell`. Start implementation when the shell design can be explained from practiced Qt mechanisms rather than copied architecture labels.
