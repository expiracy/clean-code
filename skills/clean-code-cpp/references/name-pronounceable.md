---
title: Use Pronounceable Names
impact: HIGH
impactDescription: enables verbal communication about code
tags: name, pronounceable, communication, readability
---

## Use Pronounceable Names

Names should make code easy to discuss with other people. Prefer recognizable domain words to private abbreviation schemes.

**Before (the reader must expand compressed words):**

```cpp
#include <chrono>
#include <string>

struct DtaRcrd102 {
    std::chrono::system_clock::time_point genymdhms;
    std::chrono::system_clock::time_point modymdhms;
    std::string pszqint;
};
```

**After (the record can be discussed by name):**

```cpp
#include <chrono>
#include <string>

struct CustomerRecord {
    std::chrono::system_clock::time_point createdAt;
    std::chrono::system_clock::time_point updatedAt;
    std::string recordId;
};
```

The type expresses that these values are time points; the field names explain the events they record.

**Keep useful conventions:**
- Common domain abbreviations such as `HTTP`, `URL`, and `ID` can be clearer than expanded names.
- Use the repository's casing convention for acronyms.
- Keep protocol and external API names when spelling is part of their contract.
- Short conventional symbols are suitable in tightly scoped mathematical code.

Do not expand a familiar abbreviation into a long phrase merely to make it pronounceable. The goal is a shared vocabulary, not maximum identifier length.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
