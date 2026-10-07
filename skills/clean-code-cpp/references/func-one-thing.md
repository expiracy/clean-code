---
title: Functions Should Do One Thing
impact: CRITICAL
impactDescription: enables understanding functions at a glance
tags: func, single-responsibility, cohesion, focus
---

## Functions Should Do One Thing

Give a function one cohesive responsibility and a name that covers its observable behavior. A sequence of steps can be one operation; unrelated responsibilities deserve separate entry points.

**Before (a counting query also emits a report):**

```cpp
#include <cstddef>
#include <ostream>
#include <vector>

std::size_t countValidReadings(const std::vector<int>& readings,
                              std::ostream& output) {
    std::size_t count = 0;
    for (int reading : readings) {
        if (reading >= 0) {
            ++count;
        } else {
            output << "Invalid reading: " << reading << '\n';
        }
    }
    return count;
}
```

**After (counting and reporting can be used independently):**

```cpp
#include <algorithm>
#include <cstddef>
#include <ostream>
#include <vector>

std::size_t countValidReadings(const std::vector<int>& readings) {
    return static_cast<std::size_t>(std::count_if(
        readings.begin(), readings.end(), [](int value) { return value >= 0; }));
}

void writeInvalidReadings(const std::vector<int>& readings,
                          std::ostream& output) {
    for (int reading : readings) {
        if (reading < 0) {
            output << "Invalid reading: " << reading << '\n';
        }
    }
}
```

Here the callers can choose counting, reporting, or both. An orchestration function named `auditReadings` could legitimately perform both steps when that combined behavior is required.

**Do not split mechanically:**
- Validation and transformation can belong to the same operation.
- An algorithm may need several loops or branches to satisfy one contract.
- Extract when responsibilities evolve independently or the new name improves understanding.
- A tiny arithmetic expression does not need a helper merely to claim it does one thing.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
