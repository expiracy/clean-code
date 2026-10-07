---
title: Choose Open or Closed Types Deliberately
impact: MEDIUM-HIGH
impactDescription: choose representation according to the extension boundary
tags: obj, asymmetry, variant, virtual, polymorphism
---

## Choose Open or Closed Types Deliberately

Choose representation according to the extension boundary. Runtime polymorphism supports an open family of implementations; C++17 variants and exhaustive switches suit a known closed set.

**Incorrect:**

```cpp
#include <stdexcept>

struct Shape {
    int kind;
    double first;
    double second;
};

double area(const Shape& shape) {
    if (shape.kind == 0) return shape.first * shape.first;
    if (shape.kind == 1) return shape.first * shape.second;
    throw std::invalid_argument("unknown shape");
}
```

**Correct (C++17):**

```cpp
#include <type_traits>
#include <variant>

struct Square { double side; };
struct Rectangle { double width; double height; };
using Shape = std::variant<Square, Rectangle>;

double area(const Shape& shape) {
    return std::visit([](const auto& value) {
        using T = std::decay_t<decltype(value)>;
        if constexpr (std::is_same_v<T, Square>) {
            return value.side * value.side;
        } else {
            static_assert(std::is_same_v<T, Rectangle>, "handle new shape");
            return value.width * value.height;
        }
    }, shape);
}
```

The variant expresses valid alternatives and stores them by value. Adding a type intentionally requires updating operations; that is useful for a closed domain, not automatically an Open/Closed Principle violation.

The tradeoff has two sides: with data or a variant, a new operation can usually be a local free function or visitor, while a new alternative requires revisiting existing operations. With a virtual object interface, a new implementation supplies the existing operations without changing callers, while adding a virtual operation affects the implementations. Choose according to the domain's actual extension needs, not a blanket preference for either form.

- For plugin/runtime extension without recompiling callers, an abstract base can be appropriate. Define a safe destruction contract: a public virtual destructor for deletion through the base, or a protected non-virtual destructor when such deletion is forbidden.
- Templates and free functions can provide static polymorphism without ownership or dispatch overhead. Use the mechanism that fits actual extensibility requirements.
- Avoid type-erased `void*`, raw integer tags, or unchecked casts when a typed alternative can represent the domain.
- Do not replace a deliberate enum/switch with allocated class hierarchies solely to satisfy a style rule.

Reference: [Clean Code, Chapter 6: Objects and Data Structures](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
