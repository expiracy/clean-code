---
title: Use Noun Phrases for Class Names
impact: MEDIUM-HIGH
impactDescription: clarifies the concept represented by a type
tags: name, class, noun, identity
---

## Use Noun Phrases for Class Names

Name a `class`, `struct`, or other domain type after the concept it represents. A concrete noun usually communicates more than a vague role such as `Data` or `Manager`.

**Before (names obscure the represented concepts):**

```cpp
#include <string>

struct ProcessInvoice {
    int totalCents;
};

struct Data {
    std::string street;
    std::string postalCode;
};
```

**After (types describe their contents):**

```cpp
#include <string>

struct Invoice {
    int totalCents;
};

struct PostalAddress {
    std::string street;
    std::string postalCode;
};
```

**Choose the actual role:**
- A value type can be `Invoice`, `PostalAddress`, or `Temperature`.
- A real resource owner can be `ConnectionPool` or `SessionRegistry`.
- An existing callable type or functor may appropriately use the repository's action-oriented naming convention.
- `Parser`, `Handler`, and `Manager` are useful when their responsibilities are specific and understood.

This rule does not require turning free functions or simple values into classes. Keep the existing design unless a type contributes a meaningful invariant, lifetime, or domain distinction.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
