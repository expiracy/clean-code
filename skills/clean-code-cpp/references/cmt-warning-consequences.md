---
title: Use Warning Comments for Consequences
impact: MEDIUM
impactDescription: prevents costly mistakes by future maintainers
tags: cmt, warning, consequences, safety
---

## Use Warning Comments for Consequences

Document a non-obvious consequence at the API or operation that causes it. A warning should identify the condition and the caller's required action. Prefer an API that prevents misuse when practical.

**Before (the borrowing contract is implicit):**

```cpp
#include <string_view>

std::string_view firstField(std::string_view record) noexcept {
    return record.substr(0, record.find(','));
}
```

**After (the lifetime requirement is stated):**

```cpp
#include <string_view>

// The result borrows record's backing storage. Keep that storage alive and
// avoid operations that invalidate it while the returned view is in use.
std::string_view firstField(std::string_view record) noexcept {
    return record.substr(0, record.find(','));
}
```

A view into a temporary string can dangle after the full expression. If callers must retain the field independently, return an owning `std::string` or use the project's existing owned representation.

**Useful warnings include:**
- Iterator, pointer, reference, or view invalidation.
- A required lock or thread-affinity contract.
- An irreversible external effect or an operation requiring a maintenance window.
- Measured resource costs that affect how the operation should be run.

**Keep warnings actionable:**

State the triggering condition and consequence rather than a vague “be careful.” Do not invent timing or memory estimates. Where possible, use RAII, ownership types, validation, or synchronization to enforce the constraint; a comment is not a substitute for preventing data loss or a data race.

Reference: [Clean Code, Chapter 4: Comments](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
