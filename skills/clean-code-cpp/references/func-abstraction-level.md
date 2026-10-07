---
title: Maintain One Level of Abstraction
impact: CRITICAL
impactDescription: prevents jarring context switches
tags: func, abstraction, stepdown, readability
---

## Maintain One Level of Abstraction

Keep domain steps visible when implementation details would obscure them. Extract a detail when it has a meaningful policy or contract; there is no need to wrap every STL operation.

**Before (word normalization is embedded in counting):**

```cpp
#include <cctype>
#include <istream>
#include <map>
#include <string>

std::map<std::string, int> countWords(std::istream& input) {
    std::map<std::string, int> counts;
    for (std::string word; input >> word;) {
        for (char& ch : word) {
            ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
        }
        ++counts[word];
    }
    return counts;
}
```

**After (the normalization policy has a boundary):**

```cpp
#include <cctype>
#include <istream>
#include <map>
#include <string>
#include <utility>

std::string normalizeWord(std::string word) {
    for (char& ch : word) {
        ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
    }
    return word;
}

std::map<std::string, int> countWords(std::istream& input) {
    std::map<std::string, int> counts;
    for (std::string word; input >> word;) {
        ++counts[normalizeWord(std::move(word))];
    }
    return counts;
}
```

This example folds individual bytes with the current C locale; it is not Unicode case folding. A real text-processing requirement may need the project's existing Unicode library.

**Keep useful exceptions:**
- Small utilities can mix domain decisions and implementation without becoming confusing.
- Test setup and assertions naturally operate at different levels.
- Keep simple operations inline when a helper only adds a jump.
- C++ declaration order and templates can determine the placement of definitions; readability does not require artificial forward declarations.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
