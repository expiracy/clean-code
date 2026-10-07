---
title: Respect Indentation Rules
impact: MEDIUM
impactDescription: preserves visual hierarchy for quick scanning
tags: fmt, indentation, hierarchy, structure
---

## Respect Indentation Rules

Make lexical scope visible with the repository's indentation, braces, and short-expression policy. Nested control flow should be easy to scan without manually reconstructing braces.

**Before (structure is compressed and unindented):**

```cpp
#include <vector>

int sumPositiveReadings(const std::vector<int>& readings) {
int total = 0;
for (int reading : readings) { if (reading > 0) { total += reading; } }
return total;
}
```

**After (scope is visible):**

```cpp
#include <vector>

int sumPositiveReadings(const std::vector<int>& readings) {
    int total = 0;
    for (int reading : readings) {
        if (reading > 0) {
            total += reading;
        }
    }
    return total;
}
```

**Follow the local style:**
- Let the existing `clang-format` configuration choose indentation width and brace placement.
- Keep nested statements visually inside their scopes.
- A short accessor or trivial expression can stay on one line if the project permits it.
- Do not introduce tabs, spaces, or brace changes into unrelated code.

Indentation communicates structure; it does not fix unnecessary nesting. If control flow is hard to understand even after formatting, consider a focused simplification that preserves behavior rather than a style-only rewrite.

Reference: [Clean Code, Chapter 5: Formatting](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
