---
title: Follow the Three Laws of TDD
impact: MEDIUM
impactDescription: links changed behavior to a meaningful failing check
tags: test, tdd, first, laws
---

## Follow the Three Laws of TDD

The three laws limit each step: no production change before a failing test, no more test than needed to fail, and no more implementation than needed to pass. For changed executable behavior, observe the intended failure, implement enough to pass, then refactor with checks green. Use the project's existing framework and runner. A compile failure caused by a missing API can be an initial step; follow it with a check that can expose incorrect behavior.

**Incorrect (a passing example leaves the new boundary untested):**

```cpp
#include <stdexcept>

int shipping_fee_cents(int total_cents) {
    (void)total_cents;
    return 400;
}

int main() {
    if (shipping_fee_cents(4999) != 400) {
        throw std::runtime_error("ordinary shipping changed");
    }
    // Requirement: orders of at least 5000 cents now ship free.
}
```

**Correct (the new boundary and adjacent existing behavior are checked):**

```cpp
#include <stdexcept>

int shipping_fee_cents(int total_cents) {
    return total_cents >= 5000 ? 0 : 400;
}
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

int main() {
    require(shipping_fee_cents(5000) == 0, "threshold must ship free");
    require(shipping_fee_cents(4999) == 400, "below threshold must pay");
    require(shipping_fee_cents(5001) == 0, "above threshold must ship free");
}
```

The second example shows the final green state. First add the threshold check to the original implementation and run it: it must fail because the fee is still 400. Then change the implementation and rerun. Keep failure messages and checks active in release builds; the explicit checks here do not depend on `assert` or `NDEBUG`.

Before refactoring existing code, characterize the behavior being preserved. A test must check an observable requirement, not copy an implementation expression. If the harness or dependency is unavailable, report what could not run and why; do not claim a red-green cycle or invent a replacement project framework.

Reference: [Clean Code, Chapter 9: Unit Tests](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
