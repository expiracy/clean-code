---
title: Use Verb Phrases for Method Names
impact: MEDIUM-HIGH
impactDescription: clarifies operations and query contracts
tags: name, method, verb, action
---

## Use Verb Phrases for Method Names

Use action names for functions that change state or perform work. For queries and accessors, follow C++ and repository conventions: names such as `size()`, `empty()`, and `name()` can be clear without a `get` prefix.

**Before (a noun hides the mutation):**

```cpp
#include <string>
#include <utility>
#include <vector>

struct Basket {
    std::vector<std::string> products;

    void product(std::string value) {
        products.push_back(std::move(value));
    }
};
```

**After (the operation is explicit):**

```cpp
#include <cstddef>
#include <string>
#include <utility>
#include <vector>

struct Basket {
    std::vector<std::string> products;

    void addProduct(std::string value) {
        products.push_back(std::move(value));
    }

    std::size_t size() const noexcept {
        return products.size();
    }
};
```

**Name the contract:**
- `addProduct`, `writeInvoice`, and `eraseSession` signal effects.
- `empty`, `isReady`, and `hasPermission` can express predicates.
- A conversion or factory should identify what it produces or consumes.
- Keep `get`/`set` prefixes if they are the established project or framework convention.

Do not import JavaBean requirements into C++, or rename conventional STL-like queries solely because their names are nouns.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
