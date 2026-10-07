---
title: Avoid Redundant Comments
impact: HIGH
impactDescription: eliminates noise that obscures important information
tags: cmt, redundant, noise, clutter
---

## Avoid Redundant Comments

Remove comments that only repeat the adjacent code. Keep contract documentation and rationale that a reader cannot reliably infer from names or types.

**Before (the comment restates the calculation):**

```cpp
struct SensorReading {
    int rawTemperature;
};

// Return the temperature in Celsius.
double temperatureCelsius(const SensorReading& reading) noexcept {
    // Divide the raw temperature by ten.
    return reading.rawTemperature / 10.0;
}
```

**After (the comment identifies the protocol rule):**

```cpp
struct SensorReading {
    int rawTemperature;
};

double temperatureCelsius(const SensorReading& reading) noexcept {
    // The sensor protocol encodes temperature in tenths of a degree Celsius.
    return reading.rawTemperature / 10.0;
}
```

A useful comment explains why ten is the divisor. Its accuracy depends on the sensor's protocol, so it must change if the representation changes.

**Common noise to remove:**
- Comments saying a constructor constructs an object.
- Accessor documentation that repeats only its name.
- Comments such as “increment count” beside `++count`.
- Section labels that duplicate an already clear function name.

**Keep meaningful documentation:**

Public API documentation may need to state units, ownership, valid ranges, exceptions, or thread-safety guarantees even for a short implementation. Follow the project's Doxygen or other documentation convention, and retain required notices.

Reference: [Clean Code, Chapter 4: Comments](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
