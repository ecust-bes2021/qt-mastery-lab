# Week 01 - QObject and Signals/Slots

## Goal

Understand QObject ownership, the Qt meta-object system, and signal-slot delivery well enough to explain and debug real PySide6 application behavior.

## Required Understanding

- QObject parent-child ownership and destruction order
- Signal/slot connection types: Auto, Direct, Queued, BlockingQueued, UniqueConnection
- Automatic disconnect behavior when sender or receiver is destroyed
- Python reference lifetime versus Qt object lifetime
- Why QObject is non-copyable

## Weekly Output

- A custom signal demo, such as a threshold data receiver that emits `thresholdExceeded(value)`.
- A failure demo showing one lifetime or disconnect problem, plus a written fix explanation.
- At least one project-local README explaining the demo design.
- One cross-project note in `D:\JH\growth-plan-2026-2027\notes\qt\` if the lesson is reusable beyond this repository.

## Suggested Day Split

| Day | Focus |
|---|---|
| Day 01 | QObject tree and ownership |
| Day 02 | Custom Signal and Slot basics |
| Day 03 | ConnectionType behavior |
| Day 04 | Lifetime traps: lambda, bound methods, deleteLater |
| Day 05 | Read Qt source around QObject/connect |
| Day 06 | No-AI exercise: connection monitor |
| Day 07 | Review, notes, cleanup |
