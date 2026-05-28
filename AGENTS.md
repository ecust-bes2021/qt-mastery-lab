# AGENTS.md

This is a learning lab, not a production codebase.

## Assistant Rules

- Do not write final demo code unless the user explicitly says `write the final code` or `apply this change`.
- Prefer explanation, code shape, review, debugging guidance, and verification plans.
- Keep examples minimal and tied to the current day/week objective.
- Do not add compatibility layers, fallback behavior, or extra business logic unless requested.
- Keep Qt/PySide6 reasoning grounded in event loop safety, QObject ownership, signal-slot semantics, and observability.

## Repository Intent

Each demo should answer four questions:

1. What Qt mechanism is being learned?
2. What behavior proves the mechanism works?
3. What failure mode can happen in a real tool?
4. How would this knowledge transfer to chip/debug/embedded tooling?
