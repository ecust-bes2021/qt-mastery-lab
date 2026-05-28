# qt-mastery-lab

PySide6 + Qt6 C++ daily mastery lab for Phase 1 of the 2026-2027 growth plan.

This repository is for learning Qt mechanisms through two synchronized views: Qt6 C++ as the native framework model, and PySide6 as the Python binding used in daily tool development. The goal is not to collect snippets, but to build a durable mental model by studying small, observable programs, then rewriting them by hand and explaining the design trade-offs.

## Learning Rules

- AI may provide a minimal teaching reference demo first, especially when rebuilding hand-coding fluency.
- The final learning result should be rewritten by hand after understanding the reference, then reviewed with AI.
- Every topic should be learned in pairs: Qt6 C++ native mechanism first, PySide6 binding behavior second, then a short comparison note.
- `basic_study/` is the warmup and ad-hoc practice area; it is useful for rebuilding hand-coding fluency but does not count as formal weekly output.
- Every week owns one Qt module theme.
- Every runnable demo should have a short README explaining the requirement, core Qt concept, verification method, and known pitfalls.
- Cross-project notes belong in `D:\JH\growth-plan-2026-2027\notes\`; project-specific demo notes stay here.
- AI assistants should read `docs/ai-context.md` before helping in this repository.

## Structure

```text
qt-mastery-lab/
├── basic_study/           # pre-Phase-1 warmup and later ad-hoc basics
├── week01-objects-signals/
│   └── day01-qobject-tree/
│       ├── src/           # user-rewritten PySide6 / Qt6 C++ demo code
│       ├── experiments/   # small probes, throwaway checks
│       ├── tests/         # focused tests or smoke checks
│       ├── README.md      # day task card
│       └── notes.md       # day learning notes
├── week02-events/
├── week03-paint-layout/
├── week04-model-view/
├── week05-threading/
├── week06-qml/
├── week07-opengl/
├── week08-packaging/
├── docs/                  # project-local docs, including AI context
└── tools/                 # helper scripts if they become necessary
```

## Phase 1 Weekly Map

| Week | Topic | Output |
|---|---|---|
| W1 | QObject + signals/slots | C++ ownership/signal probe + PySide6 binding probe + comparison notes |
| W2 | Event system | C++ event dispatch/filter probe + PySide6 event filter demo |
| W3 | Paint + layout | C++/PySide6 custom widget painting and layout constraints |
| W4 | Model/View | C++ model contract notes + PySide6 large-data model demo |
| W5 | Threading | C++ thread-affinity model + PySide6 worker/queued signal demo |
| W6 | QML / Qt Quick | C++ registration/property model + PySide6/Python backend QML demo |
| W7 | OpenGL / high-performance rendering | C++ Qt OpenGL lifecycle + PySide6 high-volume plotting prototype |
| W8 | Packaging | PySide6 packaging plus Qt/C++ runtime, plugin, DLL, ABI notes |

