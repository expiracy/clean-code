---
title: Avoid Encodings in Names
impact: HIGH
impactDescription: reduces mental translation burden
tags: name, encoding, hungarian, prefixes
---

## Avoid Encodings in Names

Let C++ types express representation and ownership. Use domain names rather than prefixes that encode a variable's type or scope. Preserve an established project convention when making a focused change.

**Before (type prefixes bury the meaning):**

```cpp
#include <string>
#include <utility>

class Part {
public:
    void setDsc(std::string strDsc) {
        m_strDsc = std::move(strDsc);
    }

private:
    std::string m_strDsc;
};
```

**After (the name describes the part):**

```cpp
#include <string>
#include <utility>

class Part {
public:
    void setDescription(std::string value) {
        description = std::move(value);
    }

private:
    std::string description;
};
```

**C++ naming constraints:**
- An identifier containing `__` anywhere is reserved to the implementation.
- An identifier beginning with an underscore followed by an uppercase letter is reserved everywhere.
- An identifier beginning with an underscore is reserved when used as a name in the global namespace.

Prefer ordinary domain identifiers and avoid reserved spellings in user code. A repository may consistently use a member suffix such as `description_`; retain that convention rather than imposing a broad rename. Spellings reserved for the implementation are a correctness issue, not a stylistic preference.

Avoid introducing interface prefixes or `Impl` suffixes by habit. If multiple implementations already exist, name them by the behavior or mechanism that distinguishes them. Do not add an interface just to demonstrate a naming rule.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
