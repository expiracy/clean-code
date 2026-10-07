---
title: Keep Functions Small
impact: CRITICAL
impactDescription: enables comprehension at a glance
tags: func, size, readability, comprehension
---

## Keep Functions Small

Keep a function easy to understand as one unit. Extract a coherent operation when its name exposes a useful contract or keeps a detail from obscuring the caller. Line counts are a review clue, not a quota.

**Before (CSV escaping obscures writing a reading):**

```cpp
#include <ostream>
#include <string_view>

void writeReading(std::ostream& output, std::string_view device, int value) {
    output << '"';
    for (char ch : device) {
        if (ch == '"') {
            output << '"';
        }
        output << ch;
    }
    output << "\"," << value << '\n';
}
```

**After (the format rule has a useful name):**

```cpp
#include <ostream>
#include <string>
#include <string_view>

std::string csvField(std::string_view value) {
    std::string result = "\"";
    for (char ch : value) {
        if (ch == '"') {
            result += '"';
        }
        result += ch;
    }
    return result + '"';
}

void writeReading(std::ostream& output, std::string_view device, int value) {
    output << csvField(device) << ',' << value << '\n';
}
```

The extracted function names the CSV quoting rule, which can also be reused for other fields. The stream remains an explicit dependency.

**When to keep a function together:**
- A longer function can be clearer when its local sequence implements one cohesive algorithm.
- Do not extract a wrapper whose name merely restates a single obvious statement.
- Do not split a function across classes or files merely to shorten it.
- Keep validation, resource ownership, and exception guarantees visible when extracting code.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
