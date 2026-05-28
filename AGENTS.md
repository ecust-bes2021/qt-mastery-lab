# AGENTS.md

This is a learning lab, not a production codebase.

## Assistant Rules

- Read `docs/ai-context.md` before helping in this repository.
- AI may provide a minimal teaching reference demo when the user needs a starting point to study.
- Do not treat AI-provided reference code as the final learning result; the user should understand it, close it, rewrite it by hand, then ask for review.
- Do not write or modify the final demo files unless the user explicitly says `write the final code` or `apply this change`.
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
