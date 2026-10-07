---
title: Maximize Expressiveness
impact: MEDIUM-HIGH
impactDescription: makes intent easier to understand during maintenance
tags: emerge, expressiveness, readability, maintenance
---

## Maximize Expressiveness

Choose names, types, and operations that tell readers what the code means. Prefer familiar standard-library idioms to clever encodings. Express the domain directly without inventing abstractions that require their own explanation.

**Incorrect (numeric convention is hidden in an encoding):**

```cpp
bool off(int d) {
    return d >= 0 && d < 7 && (0x60u & (1u << d)) != 0;
    // Callers must know that Monday is zero.
}

int main() { return off(6) ? 0 : 1; }
```

**Correct (names and a domain type explain the policy):**

```cpp
#include <stdexcept>

enum class Weekday {
    monday, tuesday, wednesday, thursday, friday, saturday, sunday
};

bool is_weekend(Weekday day) {
    return day == Weekday::saturday || day == Weekday::sunday;
}

int main() {
    if (!is_weekend(Weekday::saturday) ||
        !is_weekend(Weekday::sunday) || is_weekend(Weekday::monday)) {
        throw std::runtime_error("weekend policy changed");
    }
}
```

Use the project's naming conventions consistently. Name operations for their behavior and types for their domain role; avoid appending design-pattern names unless they help explain a real choice. Comments can capture reasons, units, or external constraints that code cannot express well.

Tests should describe meaningful behavior with representative cases. Preserve behavior during a readability refactor and run existing checks; clearer names do not establish correctness by themselves. Validate external numeric input before converting it to a domain enum.

Reference: [Clean Code, Chapter 12: Emergence](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
