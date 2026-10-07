---
title: Use Build-Operate-Check Pattern
impact: MEDIUM
impactDescription: makes a test's setup, action, and result easy to identify
tags: test, boc, arrange-act-assert, structure
---

## Use Build-Operate-Check Pattern

Make each test's setup, action, and expected result clear. Build-Operate-Check, Arrange-Act-Assert, and Given-When-Then describe the same useful structure. Use the project's existing framework; these standalone examples use checks that remain active under `NDEBUG`.

**Incorrect (several actions and checks obscure the behavior under test):**

```cpp
#include <stdexcept>

struct Order {
    int count = 0;
    int total_cents = 0;
    void add(int price_cents) { ++count; total_cents += price_cents; }
};
void require(bool condition) {
    if (!condition) throw std::runtime_error("order check failed");
}

int main() {
    Order order;
    require(order.count == 0);
    order.add(999);
    require(order.count == 1);
    require(order.total_cents == 999);
    order.add(999);
    require(order.count == 2);
    require(order.total_cents == 1998);
}
```

**Correct (one operation with a clearly grouped result):**

```cpp
#include <stdexcept>

struct Order {
    int count = 0;
    int total_cents = 0;
    void add(int price_cents) { ++count; total_cents += price_cents; }
};
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

void adding_one_item_updates_the_order() {
    // Build
    Order order;
    const int widget_price_cents = 999;

    // Operate
    order.add(widget_price_cents);

    // Check
    require(order.count == 1, "one item expected");
    require(order.total_cents == 999, "item price must be included");
}
int main() { adding_one_item_updates_the_order(); }
```

Multiple checks can describe one result. Use additional tests for other behaviors, such as adding the same item twice. A lifecycle or integration scenario may legitimately need several operations; make that sequence explicit rather than forcing artificial phase boundaries.

Reference: [Clean Code, Chapter 9: Unit Tests](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
