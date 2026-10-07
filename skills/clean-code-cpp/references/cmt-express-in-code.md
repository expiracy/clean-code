---
title: Express Yourself in Code, Not Comments
impact: CRITICAL
impactDescription: eliminates stale comment risk
tags: cmt, self-documenting, refactoring, clarity
---

## Express Yourself in Code, Not Comments

Use names, types, and standard operations to expose the meaning of a rule. Extract a named predicate when it expresses a useful concept, but do not add a helper when clearer local names suffice.

**Before (a comment decodes flags and a threshold):**

```cpp
// The configured overtemperature alarm requests a controller shutdown.
bool shutdownRequired(unsigned flags, int temperature) noexcept {
    return (flags & 0x04U) != 0U && temperature >= 90;
}
```

**After (names expose the rule):**

```cpp
inline constexpr unsigned overtemperatureAlarmEnabled = 0x04U;
inline constexpr int shutdownTemperatureCelsius = 90;

bool shutdownRequired(unsigned controllerFlags,
                      int temperatureCelsius) noexcept {
    return (controllerFlags & overtemperatureAlarmEnabled) != 0U &&
           temperatureCelsius >= shutdownTemperatureCelsius;
}
```

The names identify both the flag meaning and temperature units. These values are illustrative controller settings, not a recommended hardware safety threshold; use the project's actual specification and configuration mechanism.

**Prefer clearer code first:**
- Name domain constants and values.
- Use existing strong types when they prevent unit or ownership mistakes.
- Use the standard library instead of narrating a custom reimplementation.
- Avoid moving a single obvious expression into a helper only to remove a comment.

**Keep comments that code cannot replace:**
- Why a policy or algorithm was chosen.
- Lifetime, invalidation, concurrency, or other non-obvious contracts.
- Public API documentation, including preconditions and failure behavior.
- Required license and attribution notices.

Readable code and useful comments support one another; a clear name does not explain every design constraint.

Reference: [Clean Code, Chapter 4: Comments](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
