---
title: Avoid Side Effects
impact: HIGH
impactDescription: prevents hidden temporal couplings
tags: func, side-effects, purity, predictability
---

## Avoid Side Effects

Avoid effects that the function's name and contract do not reveal. Mutation and I/O are normal C++ operations; the problem is surprising callers who think they are only asking a question.

**Before (validation silently records the reading):**

```cpp
#include <vector>

struct Reading {
    int value;
};

bool isValid(const Reading& reading, std::vector<Reading>& accepted) {
    if (reading.value < 0) {
        return false;
    }
    accepted.push_back(reading);
    return true;
}
```

**After (query and recording have explicit names):**

```cpp
#include <vector>

struct Reading {
    int value;
};

bool isValid(const Reading& reading) noexcept {
    return reading.value >= 0;
}

bool recordReading(Reading reading, std::vector<Reading>& accepted) {
    if (!isValid(reading)) {
        return false;
    }
    accepted.push_back(reading);
    return true;
}
```

Repeated calls to `isValid` now leave the collection unchanged. `recordReading` clearly mutates it, and its result reports whether the reading was accepted.

**Make contracts visible:**
- Names such as `save`, `erase`, and `record` signal expected effects.
- Document non-obvious invalidation, ownership transfer, and external effects.
- Passing a mutable reference should be justified by the operation's contract.
- `const` helps communicate intent but does not prove purity: a method can still mutate external state or `mutable` members.

Do not separate a required atomic operation into a query followed by a mutation; see command/query separation for operations whose result belongs to the mutation.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
