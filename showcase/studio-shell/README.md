# Studio Shell

`studio-shell` is the portfolio-oriented integration project for `qt-mastery-lab`.

It is planned as a small, extensible Qt desktop shell for engineering tools. The first implementation can be PySide6, but the architecture should stay close enough to Qt fundamentals that a Qt6 C++ version can be designed later without changing the core ideas.

## Current Status

Design seed only. No implementation code should be added until the related fundamentals have been practiced in the weekly tracks.

## Why This Exists

The weekly exercises prove individual mechanisms. `studio-shell` proves that those mechanisms can be composed into a maintainable desktop application architecture:

- `QMainWindow` shell and navigation
- `QWidget` tool panels
- signal-slot based communication
- centralized but disciplined application context
- worker-thread execution for slow tasks
- settings, logs, and project state suitable for engineering tools

## First Implementation Bias

Use PySide6 first because it matches daily tool work and allows faster iteration. Keep the design language compatible with Qt6 C++ by avoiding Python-only assumptions in the architecture documents.

## Documents

- [DESIGN.md](DESIGN.md) - project positioning, scope, architecture, and milestones
