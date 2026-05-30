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

This repository is specifically for strengthening Qt fundamentals from both sides: Qt6 C++ as the native framework model, and PySide6 as the Python binding used in the user's daily engineering tools. It prepares later work on engineering systems, representative portfolio work, and job search preparation.

## 2. What This Repository Is For

This repository is for synchronized PySide6 + Qt6 C++ mechanism learning demos.

The goal is not to collect generated snippets. The goal is to build a durable mental model of Qt mechanisms through small, observable programs in both Qt6 C++ and PySide6, then rebuild the idea by hand.

Every useful demo should answer four questions:

1. What Qt mechanism is being learned?
2. What behavior proves the mechanism works?
3. What real tool failure mode can happen if this mechanism is misunderstood?
4. How does the lesson transfer to chip/debug/embedded tooling?

Every topic should also include a comparison note:

```text
Qt6 C++ native mechanism:
PySide6 binding behavior:
Same rule:
Different behavior or risk:
Real-tool consequence:
```

## 3. Current Learning Map

Phase 1 uses an 8-week synchronized Qt6 C++ + PySide6 structure:

| Week | Topic | Expected Output |
|---|---|---|
| W1 | QObject + signals/slots | C++ ownership/signal probe + PySide6 binding probe + comparison notes |
| W2 | Event system | C++ event dispatch/filter probe + PySide6 event filter demo |
| W3 | Paint + layout | C++/PySide6 custom widget painting and layout constraints |
| W4 | Model/View | C++ model contract notes + PySide6 large-data model demo |
| W5 | Threading | C++ thread-affinity model + PySide6 worker/queued signal demo |
| W6 | QML / Qt Quick | C++ registration/property model + PySide6/Python backend QML demo |
| W7 | OpenGL / high-performance rendering | C++ Qt OpenGL lifecycle + PySide6 high-volume plotting prototype |
| W8 | Packaging | PySide6 packaging plus Qt/C++ runtime, plugin, DLL, ABI notes |

`showcase/` is a separate integration and portfolio area. It is for composing already-practiced Qt mechanisms into public-facing projects. The current seed is `showcase/studio-shell/`, an extensible Qt engineering-tool shell. It should remain design-only until enough W1-W5 fundamentals have been practiced to explain the architecture from first principles.

`basic_study/` is a separate warmup and ad-hoc practice area. It is for 2026-05-28 to 2026-05-31 pre-study practice and for later foundation drills when the user wants to rebuild hand-coding fluency. It does not count as official Phase 1 weekly output unless the user rewrites/promotes the work into a matching `weekXX-*` directory.

Day 01 starts at:

```text
D:\gitdir\qt-mastery-lab\week01-objects-signals\day01-qobject-tree\
```

Its first principle is QObject ownership: Qt6 C++ parent-child lifetime, `destroyed` observation, QObject non-copyability, and the difference between Qt ownership and Python references/wrappers in PySide6.

## 4. How AI Should Help Here

Default behavior:

- Explain the mechanism before suggesting code.
- Explain the Qt6 C++ native mechanism and the PySide6 binding behavior together.
- Provide a minimal teaching reference demo when the user needs a concrete starting point.
- Keep reference demos small enough to study, run, compare, modify, and rewrite by hand.
- Prefer code shape, review comments, debugging plans, and verification methods for follow-up work.
- Keep examples minimal and tied to the current day/week objective.
- Ask for observed behavior, logs, trace output, or screenshots before debugging runtime issues.
- Ground Qt/PySide6/C++ advice in event loop safety, QObject ownership, signal-slot semantics, memory/lifetime rules, and observability.

For learning tasks, use this response shape by default:

1. Problem understanding
2. Qt6 C++ native mechanism
3. PySide6 binding behavior
4. Same rules and changed risks
5. Minimal teaching reference demo, if needed
6. How to run and observe it
7. What the user should change and explain
8. How the user should rewrite it by hand
9. Real tool failure mode
10. Minimal next step

## 5. Hard Boundaries

AI is allowed to provide a minimal teaching reference demo. This is a study scaffold, not the final learning artifact.

The intended loop is:

1. AI gives the smallest runnable reference that proves the current Qt mechanism.
2. The reference should make the Qt6 C++ mechanism and PySide6 behavior comparable.
3. The user runs it, changes small parts, and explains the observed behavior.
4. The user closes the reference and rewrites the demo by hand.
5. AI reviews the user's rewritten version for correctness, Qt semantics, PySide6 binding risks, and real-tool failure modes.

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
| Pre-2026-06-01 warmup and ad-hoc basics | `D:\gitdir\qt-mastery-lab\basic_study\` |
| Learning demo code for both tracks | `D:\gitdir\qt-mastery-lab\weekXX-...\` |
| Integration / portfolio projects | `D:\gitdir\qt-mastery-lab\showcase\` |
| Project-specific demo notes | this repository, near the demo |
| Cross-project Qt/C++/engineering notes | `D:\JH\growth-plan-2026-2027\notes\` |
| Weekly/monthly progress records | `D:\JH\growth-plan-2026-2027\progress\` |
| Annual plan changes | `D:\JH\growth-plan-2026-2027\` |

Do not put private plan/progress files under this repository.
Do not put code files under `D:\JH\growth-plan-2026-2027\`.

## 7. Teaching Focus

The user's work context is chip/debug/embedded-adjacent engineering tools. When explaining Qt6 C++ and PySide6, connect the mechanism to real tool problems such as:

- UI thread blocking during hardware I/O
- unsafe cross-thread QObject or QWidget access
- QObject ownership mismatch between C++ Qt objects and Python wrappers
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
You are learning QObject ownership today. First compare the Qt6 C++ rule and the
PySide6 wrapper behavior. Use the smallest reference probe: one parent, two children,
and destroyed logging. Run it, change one parent relationship, paste the output,
and we will analyze evidence vs inference. Then close the reference and rewrite it.
```

Good:

```text
For this week, do not jump to QThread yet. The bug you are asking about is still
about QObject lifetime and signal receiver validity. Verify the Qt6 C++ ownership
rule first, then check what PySide6 wrapper lifetime changes.
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
6. `D:\gitdir\qt-mastery-lab\basic_study\README.md` if the user is warming up or doing foundation drills
7. The current week/day README under `D:\gitdir\qt-mastery-lab\weekXX-...\`

## Revision History

| Date | Change |
|---|---|
| 2026-05-28 | Initial AI orientation for qt-mastery-lab |
| 2026-05-28 | Allow minimal AI teaching reference demos while preserving hand rewrite and review as the final learning loop |
| 2026-05-28 | Reframe Phase 1 as synchronized Qt6 C++ native mechanism plus PySide6 binding behavior learning |
| 2026-05-28 | Add basic_study as pre-start warmup and later ad-hoc foundation practice area |
