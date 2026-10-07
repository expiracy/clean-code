---
title: Follow the Four Rules of Simple Design
impact: HIGH
impactDescription: prevents speculative structure while preserving behavior
tags: emerge, simple-design, kent-beck, refactoring
---

## Follow the Four Rules of Simple Design

The book presents Kent Beck's four simple-design rules in this order: pass the tests, eliminate duplication, express intent, and minimize classes and methods. Start from observed behavior and current requirements. Passing an incomplete suite is useful evidence, not proof of correctness.

**Incorrect (an abstract hierarchy provides no current variation):**

```cpp
#include <memory>

class AbstractDiscount {
public:
    virtual ~AbstractDiscount() = default;
    virtual int apply(int price) const = 0;
};
class DefaultDiscount final : public AbstractDiscount {
public:
    int apply(int price) const override { return price - price / 10; }
};
class DiscountFactory {
public:
    std::unique_ptr<AbstractDiscount> create() const {
        return std::make_unique<DefaultDiscount>();
    }
};

int main() {
    const auto discount = DiscountFactory{}.create();
    return discount->apply(1000) == 900 ? 0 : 1;
}
```

**Correct (the current policy is a function):**

```cpp
#include <stdexcept>

int discounted_price(int price_cents) {
    return price_cents - price_cents / 10;
}

int main() {
    if (discounted_price(1000) != 900 || discounted_price(9) != 9) {
        throw std::runtime_error("discount rounding changed");
    }
}
```

These bounded nonnegative inputs use an explicit integer rounding policy. A real monetary API must validate its inputs and define its allowed range, currency, and rounding requirements.

Characterize current behavior before removing structure. Distinguish duplicated policy from coincidentally similar code; merging unrelated concepts can make future changes harder. Add structure when an existing runtime extension, external dependency, or framework needs it. Multiple implementations can use values, callables, templates, or `std::variant`; a virtual interface is one option.

Reference: [Clean Code, Chapter 12: Emergence](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
