---
title: Delete Commented-Out Code
impact: HIGH
impactDescription: prevents code archaeology confusion
tags: cmt, dead-code, version-control, clutter
---

## Delete Commented-Out Code

Remove obsolete executable code instead of leaving it commented out. Version control preserves committed history; a disabled block obscures which implementation is current and can drift away from the active code.

**Before (an abandoned discount path remains):**

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

int invoiceTotal(const std::vector<int>& itemPricesCents, int discountCents) {
    const int subtotal = std::accumulate(itemPricesCents.begin(),
                                         itemPricesCents.end(), 0);
    // if (subtotal > 5000) {
    //     return subtotal - 500;
    // }
    // return subtotal;
    return std::max(0, subtotal - discountCents);
}
```

**After (one current implementation):**

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

int invoiceTotal(const std::vector<int>& itemPricesCents, int discountCents) {
    const int subtotal = std::accumulate(itemPricesCents.begin(),
                                         itemPricesCents.end(), 0);
    return std::max(0, subtotal - discountCents);
}
```

**Before removing a block:**
- Confirm it is obsolete executable code rather than an API usage example.
- Preserve required license, attribution, and meaningful rationale comments.
- If a compatibility path is still required, represent it with the project's actual feature or platform mechanism and verify that path.

A nearby commit or issue reference can help explain a non-obvious removal, but every deletion does not need one. Temporary experiments can remain in scratch work until resolved; do not ship them as commented-out alternatives in maintained source.

Reference: [Clean Code, Chapter 4: Comments](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
