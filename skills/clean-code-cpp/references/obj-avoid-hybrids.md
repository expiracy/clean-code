---
title: Protect Invariants Without Rejecting Useful Value Types
impact: MEDIUM-HIGH
impactDescription: a problematic hybrid exposes writable state that bypasses its own invariants
tags: obj, hybrid, invariant, structure, value-type
---

## Protect Invariants Without Rejecting Useful Value Types

A problematic hybrid exposes writable state that bypasses its own invariants. Public aggregate fields plus harmless operations are not automatically a design failure in C++.

**Incorrect:**

```cpp
struct Stock {
    unsigned available;
    bool reserve(unsigned quantity) {
        if (quantity > available) return false;
        available -= quantity;
        return true;
    }
};

void bypass_reservation(Stock& stock) {
    stock.available = 0; // Callers can sidestep the reservation contract.
}
```

**Correct (C++17):**

```cpp
class Stock {
public:
    explicit Stock(unsigned available) : available_(available) {}
    unsigned available() const { return available_; }
    bool reserve(unsigned quantity) {
        if (quantity > available_) return false;
        available_ -= quantity;
        return true;
    }
private:
    unsigned available_;
};

struct StockSnapshot { unsigned available; };
```

The reservation returns success while changing state: this is an explicit command result, not a hidden query side effect. Separate snapshot data from controlled mutation only where that boundary serves callers.

- Aggregates with comparisons, serialization, or simple calculations can be idiomatic value types. Avoid declaring every `struct` with a member function a hybrid.
- Do not add getters and setters that merely expose the same unrestricted mutation. Access control should enforce a meaningful contract.
- This example assumes single-threaded ownership. Sharing stock across threads requires synchronization around the complete reservation operation, not a separate availability check.

Reference: [Clean Code, Chapter 6: Objects and Data Structures](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
