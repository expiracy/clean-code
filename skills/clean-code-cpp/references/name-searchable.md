---
title: Use Searchable Names
impact: HIGH
impactDescription: enables effective code navigation
tags: name, searchable, constants, refactoring
---

## Use Searchable Names

Give domain constants names that can be found with code search. A name should explain what a value controls, while its C++ type should express units where practical.

**Before (the timeout policy is buried in a literal):**

```cpp
#include <chrono>

bool sessionExpired(std::chrono::seconds idleDuration) {
    return idleDuration >= std::chrono::seconds{30};
}

bool showIdleWarning(std::chrono::seconds idleDuration) {
    return idleDuration >= std::chrono::seconds{30};
}
```

**After (one searchable policy value):**

```cpp
#include <chrono>

inline constexpr auto sessionIdleTimeout = std::chrono::seconds{30};

bool sessionExpired(std::chrono::seconds idleDuration) {
    return idleDuration >= sessionIdleTimeout;
}

bool showIdleWarning(std::chrono::seconds idleDuration) {
    return idleDuration >= sessionIdleTimeout;
}
```

Searching for `sessionIdleTimeout` now finds the places that implement the same policy. The example's duration is illustrative; choose the actual product requirement rather than copying it.

**Use judgment:**
- Name repeated policy values and non-obvious domain constants.
- Ordinary structural values such as `0` and `1` do not all need named wrappers.
- Keep conventional short variables in small loops and mathematical expressions.
- If operators need to tune a value, use the existing configuration path instead of freezing it as a constant.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
