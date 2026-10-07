---
title: Isolate Classes from Change
impact: MEDIUM
impactDescription: enables controlled tests of changing dependencies
tags: class, dip, interfaces, coupling
---

## Isolate Classes from Change

Keep application policy independent of volatile I/O details. In C++17, a dependency can be a callable, a reference, or a template parameter; it does not automatically require a virtual interface. Choose the smallest seam the current use needs.

**Incorrect (policy constructs the changing data source):**

```cpp
#include <map>
#include <string>

class ExchangeClient {
public:
    int price_cents(const std::string&) const { return 15000; }
}; // Stand-in for a client that performs external I/O.

class Portfolio {
    std::map<std::string, int> holdings_{{"ACME", 10}};
public:
    int value_cents() const {
        const ExchangeClient exchange;
        int total = 0;
        for (const auto& holding : holdings_) {
            total += exchange.price_cents(holding.first) * holding.second;
        }
        return total;
    }
};

int main() { return Portfolio{}.value_cents() == 150000 ? 0 : 1; }
```

**Correct (policy receives the needed operation):**

```cpp
#include <map>
#include <stdexcept>
#include <string>

struct Portfolio {
    std::map<std::string, int> holdings;
    template<class Price>
    int value_cents(Price price) const {
        int total = 0;
        for (const auto& holding : holdings) {
            total += price(holding.first) * holding.second;
        }
        return total;
    }
};

int main() {
    const Portfolio portfolio{{{"ACME", 10}, {"BETA", 2}}};
    const auto fixed_price = [](const std::string& symbol) {
        return symbol == "ACME" ? 15000 : 5000;
    };
    if (portfolio.value_cents(fixed_price) != 160000) {
        throw std::runtime_error("portfolio must sum every holding");
    }
}
```

The example uses small bounded integer amounts; a real monetary model must define overflow, currency, and rounding. Tests should verify results, not merely calls to the injected operation.

Use runtime polymorphism for an open set of runtime implementations when that need exists. A polymorphic owning base needs a virtual destructor. Borrowed dependencies must outlive their consumers; introducing `std::shared_ptr` solely for injection obscures ownership.

Reference: [Clean Code, Chapter 10: Classes](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
