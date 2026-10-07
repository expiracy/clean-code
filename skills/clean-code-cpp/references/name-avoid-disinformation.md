---
title: Avoid Disinformation in Names
impact: CRITICAL
impactDescription: prevents incorrect mental models
tags: name, disinformation, misleading, types
---

## Avoid Disinformation in Names

Names should describe the actual role and contract of an object. A container's implementation is less useful than what its keys, values, or ordering mean.

**Before (the name implies the wrong lookup model):**

```cpp
#include <map>
#include <string>

struct Account {
    int balanceCents;
};

std::map<std::string, Account> accountList;

int lookupBalance(const std::string& name) {
    return accountList.at(name).balanceCents;
}
```

**After (the key and contents are explicit):**

```cpp
#include <map>
#include <string>

struct Account {
    int balanceCents;
};

std::map<std::string, Account> accountsByName;

int lookupBalance(const std::string& name) {
    return accountsByName.at(name).balanceCents;
}
```

**Watch for misleading distinctions:**
- Avoid nearly identical long names whose important difference is buried.
- Avoid `l`, `O`, and similar characters when they are easily confused with digits.
- Do not label a borrowed view as an owned buffer, or a count as a byte size.
- Include units when a numeric type cannot express them: `balanceCents`, for example.

Do not rename established APIs or project conventions merely to enforce a preferred naming style. Rename when the existing name causes a concrete misunderstanding, and update its callers together.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
