---
title: Minimize Function Arguments
impact: HIGH
impactDescription: reduces cognitive load and testing complexity
tags: func, arguments, parameters, simplicity
---

## Minimize Function Arguments

Make arguments easy to interpret and difficult to swap accidentally. Group values that form a real domain concept, and consider strong types for interchangeable primitive arguments. There is no ideal argument-count quota.

**Before (coordinates and a boolean mode need explanation):**

```cpp
#include <ostream>
#include <string_view>

void writeMarker(std::ostream& output, double latitude, double longitude,
                 std::string_view title, bool compact) {
    output << latitude << ',' << longitude << ':' << title;
    if (!compact) {
        output << '\n';
    }
}
```

**After (grouped coordinates and a named mode):**

```cpp
#include <ostream>
#include <string_view>

struct Location {
    double latitude;
    double longitude;
};

enum class MarkerFormat { compact, lineDelimited };

void writeMarker(std::ostream& output, Location location,
                 std::string_view title, MarkerFormat format) {
    output << location.latitude << ',' << location.longitude << ':' << title;
    if (format == MarkerFormat::lineDelimited) {
        output << '\n';
    }
}
```

The stream stays explicit even though it adds an argument. Hiding it in a global or a new object's fields solely to reduce the count would obscure a dependency.

**Choose the smallest useful API:**
- Reuse an existing value type when parameters already form one concept.
- An `enum class` mode can be clearer than a boolean or two duplicated functions.
- Separate operations when modes represent genuinely different responsibilities.
- A builder or options object needs a real construction or configuration problem; argument count alone does not justify one.
- Use `const&`, values, or views according to ownership and lifetime needs, not argument-count rules.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
