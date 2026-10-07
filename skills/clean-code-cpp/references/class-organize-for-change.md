---
title: Organize Classes for Change
impact: MEDIUM
impactDescription: keeps each change close to the policy it affects
tags: class, ocp, change, design
---

## Organize Classes for Change

Organize code around the changes you actually expect. The Open-Closed Principle is a tool for protecting stable policy from changing details, not a requirement to create a class hierarchy for every option.

**Incorrect (a closed set encoded as unchecked text):**

```cpp
#include <stdexcept>
#include <string>

class Exporter {
public:
    std::string extension(const std::string& format) const {
        if (format == "csv") return ".csv";
        if (format == "json") return ".json";
        throw std::invalid_argument("unknown format");
    }
};

int main() { return Exporter{}.extension("csv") == ".csv" ? 0 : 1; }
```

**Correct (a deliberate exhaustive switch for a closed domain):**

```cpp
#include <stdexcept>
#include <string_view>

enum class Format { csv, json };

std::string_view extension(Format format) {
    switch (format) {
    case Format::csv: return ".csv";
    case Format::json: return ".json";
    }
    throw std::invalid_argument("invalid format value");
}

int main() {
    if (extension(Format::csv) != ".csv" ||
        extension(Format::json) != ".json") {
        throw std::runtime_error("wrong export extension");
    }
}
```

Changing the enum deliberately prompts a review of its switches; compiler warnings help when every enumerator is listed and no `default` masks new values. This is reasonable for a small closed domain. Validate text when converting external input to `Format`.

For alternatives with distinct value data, consider `std::variant` and visitation. For compile-time interchangeable operations, a template or callable may suffice. Use a virtual interface only for genuine open runtime extension, with safe destruction and explicit ownership. Characterize current behavior before reorganizing it.

Reference: [Clean Code, Chapter 10: Classes](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
