# AI Context for qt-mastery-lab

> This document is for any AI assistant that helps with this repository.
> Read this before giving advice, reviewing code, or changing files.

## 1. Repository Role

`D:\gitdir\qt-mastery-lab` is not a production project. It is the Phase 1 learning lab for the user's 2026-2027 growth plan.

The annual plan lives here:

```text
D:\JH\growth-plan-2026-2027\
```

The plan's current objective is:

```text
2026-06 to 2027-05:
Grow from a PySide6-based upper-computer/tooling engineer into a senior engineer
who can design, debug, and deliver maintainable engineering tools.

Target job-change window:
2027 H1.
```

This repository is specifically for strengthening Qt/PySide6 fundamentals before expanding into engineering systems, representative portfolio work, and job search preparation.

## 2. What This Repository Is For

This repository is for PySide6 / Qt6 mechanism learning demos.

The goal is not to collect generated snippets. The goal is to build a durable mental model of Qt mechanisms through small, observable programs, then rebuild the idea by hand.

Every useful demo should answer four questions:

1. What Qt mechanism is being learned?
2. What behavior proves the mechanism works?
3. What real tool failure mode can happen if this mechanism is misunderstood?
4. How does the lesson transfer to chip/debug/embedded tooling?

## 3. Current Learning Map

Phase 1 uses an 8-week Qt/PySide6 structure:

| Week | Topic | Expected Output |
|---|---|---|
| W1 | QObject + signals/slots | QObject ownership notes and a custom signal demo |
| W2 | Event system | event filter / custom event demo |
| W3 | Paint + layout | custom painted widget and layout constraints |
| W4 | Model/View | large-data model demo |
| W5 | Threading | worker thread and queued signal demo |
| W6 | QML / Qt Quick | Python backend plus QML frontend demo |
| W7 | OpenGL / high-performance rendering | high-volume plotting prototype |
| W8 | Packaging | Windows packaging checklist and installer demo |

Day 01 starts at:

```text
D:\gitdir\qt-mastery-lab\week01-objects-signals\day01-qobject-tree\
```

Its first principle is QObject ownership: parent-child lifetime, `destroyed` observation, and the difference between Qt ownership and Python references.

## 4. How AI Should Help Here

Default behavior:

- Explain the mechanism before suggesting code.
- Provide a minimal teaching reference demo when the user needs a concrete starting point.
- Keep reference demos small enough to study, run, modify, and rewrite by hand.
- Prefer code shape, review comments, debugging plans, and verification methods for follow-up work.
- Keep examples minimal and tied to the current day/week objective.
- Ask for observed behavior, logs, trace output, or screenshots before debugging runtime issues.
- Ground Qt/PySide6 advice in event loop safety, QObject ownership, signal-slot semantics, and observability.

For learning tasks, use this response shape by default:

1. Problem understanding
2. Core Qt mechanism
3. Minimal teaching reference demo, if needed
4. How to run and observe it
5. What the user should change and explain
6. How the user should rewrite it by hand
7. Real tool failure mode
8. Minimal next step

## 5. Hard Boundaries

AI is allowed to provide a minimal teaching reference demo. This is a study scaffold, not the final learning artifact.

The intended loop is:

1. AI gives the smallest runnable reference that proves the current Qt mechanism.
2. The user runs it, changes small parts, and explains the observed behavior.
3. The user closes the reference and rewrites the demo by hand.
4. AI reviews the user's rewritten version for correctness, Qt semantics, and real-tool failure modes.

Do not write or modify final demo files unless the user explicitly says:

- `write the final code`
- `apply this change`

Without that permission:

- Do not create polished, feature-complete demo implementations.
- Do not replace the user's final rewritten learning work.
- Do not add compatibility layers, fallback behavior, or extra business logic.
- Do not broaden the exercise beyond the current day/week target.
- Do not delete files, code, comments, configuration, tests, or docs unless the user explicitly asks for deletion.

This is important because the user is rebuilding hand-coding fluency. AI reference code is allowed as a teaching aid, but the repository's value comes from understanding, rewriting, and reviewing the mechanism.

## 6. File Placement Rules

Use the annual plan's workspace layout as the source of truth:

```text
D:\JH\growth-plan-2026-2027\workspace-layout.md
```

Short version:

| Content | Location |
|---|---|
| Learning demo code | `D:\gitdir\qt-mastery-lab\weekXX-...\` |
| Project-specific demo notes | this repository, near the demo |
| Cross-project Qt/C++/engineering notes | `D:\JH\growth-plan-2026-2027\notes\` |
| Weekly/monthly progress records | `D:\JH\growth-plan-2026-2027\progress\` |
| Annual plan changes | `D:\JH\growth-plan-2026-2027\` |

Do not put private plan/progress files under this repository.
Do not put code files under `D:\JH\growth-plan-2026-2027\`.

## 7. Teaching Focus

The user's work context is chip/debug/embedded-adjacent engineering tools. When explaining Qt, connect the mechanism to real tool problems such as:

- UI thread blocking during hardware I/O
- unsafe cross-thread QObject or QWidget access
- serial/I2C/SPI/JTAG transaction observability
- large table or register-map performance
- binary parsing and model/view separation
- protocol state, retry, timeout, and cancellation
- field diagnostics and reproducible logs
- packaging reliability on Windows

The emphasis should be senior-engineering growth: correctness, root cause, trade-offs, maintainability, and observable behavior.

## 8. Good AI Behavior Examples

Good:

```text
You are learning QObject ownership today. First prove parent-child destruction
with this smallest reference probe. It has one parent, two children, and destroyed
logging. Run it, change one parent relationship, paste the output, and we will
analyze evidence vs inference. Then close the reference and rewrite it yourself.
```

Good:

```text
For this week, do not jump to QThread yet. The bug you are asking about is still
about QObject lifetime and signal receiver validity. Verify destruction order first.
```

Bad:

```text
Here is a complete polished PySide6 app with all features implemented.
```

Bad:

```text
Here is the finished demo file. Commit this directly as your learning output.
```

Bad:

```text
Let's add a fallback path and compatibility layer even though today's exercise is
only about QObject ownership.
```

## 9. First Files To Read

When entering this repository, read these in order:

1. `D:\gitdir\qt-mastery-lab\README.md`
2. `D:\gitdir\qt-mastery-lab\AGENTS.md`
3. `D:\gitdir\qt-mastery-lab\docs\ai-context.md`
4. `D:\JH\growth-plan-2026-2027\README.md`
5. `D:\JH\growth-plan-2026-2027\workspace-layout.md`
6. The current week/day README under `D:\gitdir\qt-mastery-lab\weekXX-...\`

## Revision History

| Date | Change |
|---|---|
| 2026-05-28 | Initial AI orientation for qt-mastery-lab |
| 2026-05-28 | Allow minimal AI teaching reference demos while preserving hand rewrite and review as the final learning loop |
