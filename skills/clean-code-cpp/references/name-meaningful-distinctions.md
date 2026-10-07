---
title: Make Meaningful Distinctions
impact: CRITICAL
impactDescription: eliminates ambiguity between similar concepts
tags: name, distinction, noise-words, clarity
---

## Make Meaningful Distinctions

Different names should explain different roles. Number suffixes and generic words such as `data` or `info` are poor substitutes for a domain distinction.

**Before (parameter order and roles need decoding):**

```cpp
#include <string>
#include <vector>

void copyChars(const std::vector<char>& a1, std::vector<char>& a2) {
    a2.assign(a1.begin(), a1.end());
}

struct Product {
    std::string name;
};
struct ProductData {
    int quantity;
};
```

**After (names explain direction and contents):**

```cpp
#include <string>
#include <vector>

void copyChars(const std::vector<char>& source,
               std::vector<char>& destination) {
    destination.assign(source.begin(), source.end());
}

struct Product {
    std::string name;
};
struct ProductStock {
    int availableUnits;
};
```

**Use the distinction that callers need:**
- `source` and `destination` explain data flow.
- `currentPrice` and `quotedPrice` identify different business values.
- `ProductStock` explains what information it adds.
- Avoid adding a type suffix that repeats the declaration, such as `nameString`.

Words like `data`, `info`, or `record` can be accurate domain names. Keep them when they identify a real wire format, database record, or other established concept; judge their meaning in context.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
