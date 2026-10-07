---
title: Use Vertical Formatting for Readability
impact: HIGH
impactDescription: enables scanning code like a newspaper
tags: fmt, vertical, whitespace, organization
---

## Use Vertical Formatting for Readability

Separate distinct concepts with vertical whitespace and keep related definitions close. Place declarations near their use when doing so preserves clear lifetimes and initialization.

**Before (independent concepts run together):**

```cpp
#include <numeric>
#include <ostream>
#include <string>
#include <vector>
struct Invoice {
    std::string customer;
    std::vector<int> itemPricesCents;
};
int invoiceTotal(const Invoice& invoice) {
    return std::accumulate(invoice.itemPricesCents.begin(), invoice.itemPricesCents.end(), 0);
}
void writeInvoice(std::ostream& output, const Invoice& invoice) {
    output << invoice.customer << '\n';
    const int totalCents = invoiceTotal(invoice);
    output << totalCents << '\n';
}
```

**After (types and operations have visible boundaries):**

```cpp
#include <numeric>
#include <ostream>
#include <string>
#include <vector>

struct Invoice {
    std::string customer;
    std::vector<int> itemPricesCents;
};

int invoiceTotal(const Invoice& invoice) {
    return std::accumulate(invoice.itemPricesCents.begin(),
                           invoice.itemPricesCents.end(), 0);
}

void writeInvoice(std::ostream& output, const Invoice& invoice) {
    output << invoice.customer << '\n';

    const int totalCents = invoiceTotal(invoice);
    output << totalCents << '\n';
}
```

**Guidelines:**
- Use blank lines to distinguish operations or meaningful phases, not every statement.
- Keep related functions together when the existing file structure permits it.
- Respect C++ declaration-before-use rules, template requirements, and header/source organization.
- Do not add forward declarations or reorder large portions of a file purely to enforce top-down reading.

Apply the project's `clang-format` and surrounding conventions; avoid unrelated whitespace churn.

Reference: [Clean Code, Chapter 5: Formatting](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
