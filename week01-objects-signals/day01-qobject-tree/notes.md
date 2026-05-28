# Day 01 Notes - QObject Tree and Ownership

## Observed Behavior

- Command:
- Output summary:
- What surprised me:

## Evidence vs Inference

Evidence from my demo:

- 

Inference / mental model:

- 

## Failure Modes This Helps Prevent

- Widget or dialog leaks because parent is missing.
- Object accessed after Qt has deleted the underlying C++ instance.
- Hardware/session object accidentally owned by a short-lived UI widget.

## Transfer to Real Tools

Where this matters in chip/debug tools:

- Long-running serial/I2C/SPI sessions should not be blindly parented to transient widgets.
- Worker objects moved to threads need explicit lifetime design.
- Dialog-owned widgets can rely on QObject tree cleanup, but backend state should have clearer ownership.

## Follow-Up Questions

- 
