---
title: Hide Representation When It Has a Reason to Vary
impact: MEDIUM-HIGH
impactDescription: expose useful operations and protect real invariants
tags: obj, abstraction, encapsulation, value-semantics
---

## Hide Representation When It Has a Reason to Vary

Expose useful operations and protect real invariants. A C++ value type can hide representation without virtual dispatch or a getter/setter layer.

**Incorrect:**

```cpp
#include <cmath>

struct Position { double x; double y; };

double distance_from_origin(const Position& position) {
    return std::sqrt(position.x * position.x + position.y * position.y);
}
```

**Correct (C++17):**

```cpp
#include <cmath>

class Position {
public:
    Position(double x, double y) : x_(x), y_(y) {}
    double distance_from_origin() const { return std::hypot(x_, y_); }
private:
    double x_;
    double y_;
};

double describe_distance(const Position& position) {
    return position.distance_from_origin();
}
```

The first design is a smell only when clients should be insulated from the coordinate representation or its invariants. Public `x` and `y` are perfectly reasonable for a plain mathematical aggregate. The second illustrates a stable operation; it needs no interface or factory.

- Prefer concrete values and the rule of zero. Store ownership in standard owners; handwritten copy/move/destructor logic needs a resource-management reason.
- Hide fields whose arbitrary mutation could violate an invariant. Keep simple transport values as aggregates when that is clearer.
- `const` access does not establish thread safety: mutable members, pointed-to objects, and shared external state still matter.
- Do not create abstraction solely because a book example uses Java interfaces.

Reference: [Clean Code, Chapter 6: Objects and Data Structures](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
