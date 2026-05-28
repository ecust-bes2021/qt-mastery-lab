# qt-mastery-lab

PySide6 / Qt6 daily mastery lab for Phase 1 of the 2026-2027 growth plan.

This repository is for Qt mechanism learning demos. The goal is not to collect snippets, but to build a durable mental model of Qt by studying small, observable programs, then rewriting them by hand and explaining the design trade-offs.

## Learning Rules

- AI may provide a minimal teaching reference demo first, especially when rebuilding hand-coding fluency.
- The final learning result should be rewritten by hand after understanding the reference, then reviewed with AI.
- Every week owns one Qt module theme.
- Every runnable demo should have a short README explaining the requirement, core Qt concept, verification method, and known pitfalls.
- Cross-project notes belong in `D:\JH\growth-plan-2026-2027\notes\`; project-specific demo notes stay here.
- AI assistants should read `docs/ai-context.md` before helping in this repository.

## Structure

```text
qt-mastery-lab/
├── week01-objects-signals/
│   └── day01-qobject-tree/
│       ├── src/           # user-rewritten demo code
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
| W1 | QObject + signals/slots | custom signal widget + ownership notes |
| W2 | Event system | event filter / custom event demo |
| W3 | Paint + layout | custom painted widget + layout constraints |
| W4 | Model/View | large-data model demo |
| W5 | Threading | worker thread + queued signal demo |
| W6 | QML / Qt Quick | Python backend + QML frontend demo |
| W7 | OpenGL / high-performance rendering | high-volume plotting prototype |
| W8 | Packaging | Windows packaging checklist and installer demo |

