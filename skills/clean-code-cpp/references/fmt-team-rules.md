---
title: Follow Team Formatting Rules
impact: HIGH
impactDescription: eliminates style-related code review friction
tags: fmt, team, consistency, standards
---

## Follow Team Formatting Rules

Use the repository's established C++ formatting style. Consistency makes a change easier to review without turning personal preferences into unrelated edits.

**Before (mixed styles in adjacent functions):**

```cpp
#include <numeric>
#include <vector>

int totalReadings(const std::vector<int>& readings){
 return std::accumulate(readings.begin(),readings.end(),0);
}

bool hasReadings( const std::vector<int>& readings )
{
    return !readings.empty();
}
```

**After (one consistent illustrative style):**

```cpp
#include <numeric>
#include <vector>

int totalReadings(const std::vector<int>& readings) {
    return std::accumulate(readings.begin(), readings.end(), 0);
}

bool hasReadings(const std::vector<int>& readings) {
    return !readings.empty();
}
```

The example's brace placement and indentation are illustrative. The project's configuration takes precedence.

**Implementation:**
- Locate and use the existing `.clang-format` or `_clang-format` configuration and the project's formatter version or command.
- Follow established checks and editor settings where provided.
- Keep formatting scoped to the requested change and the repository's normal workflow.
- If there is no formatter configuration, follow nearby maintained code rather than introducing a new style by default.

Do not perform a repository-wide style cleanup, add a formatter dependency, or create a new configuration merely because a functional change touches C++.

Reference: [Clean Code, Chapter 5: Formatting](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
