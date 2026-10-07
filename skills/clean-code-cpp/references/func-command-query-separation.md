---
title: Separate Commands from Queries
impact: MEDIUM
impactDescription: eliminates ambiguous function behavior
tags: func, cqs, command, query, separation
---

## Separate Commands from Queries

Keep ordinary queries free of surprising mutation, and name commands to reveal their effects. A command can return an outcome or extracted value when that result is naturally part of the operation.

**Before (a query-like name hides a mutation):**

```cpp
#include <atomic>

unsigned ticketNumber(std::atomic<unsigned>& nextNumber) noexcept {
    return nextNumber.fetch_add(1, std::memory_order_relaxed);
}
```

**After (the atomic operation has an action name):**

```cpp
#include <atomic>

unsigned issueTicketNumber(std::atomic<unsigned>& nextNumber) noexcept {
    return nextNumber.fetch_add(1, std::memory_order_relaxed);
}
```

The result and increment must remain one atomic read-modify-write operation. Splitting them into a load and a store would allow concurrent callers to issue the same ticket. Relaxed ordering suffices here only because the counter does not publish or synchronize other data; it also assumes exhaustion and wraparound are handled by the surrounding ticket policy.

**Preserve idiomatic combined operations:**
- Stream extraction both reads input and updates the destination.
- `std::map::extract` removes a node and returns ownership of it.
- Container `erase` can return the iterator needed to continue traversal safely.
- `std::atomic::fetch_add`, `exchange`, and compare-exchange return information coupled to their state change.
- Insertion APIs can return whether insertion succeeded without a separate lookup.

**Avoid check-then-act races:**

When correctness depends on the state checked still being current at mutation time, keep checking and changing within one atomic operation, one database transaction, or one lock covering both. A separate `contains`/`exists` call does not make a concurrent insertion safe.

For an immutable value, a function returning a modified copy is also a clear transformation. Follow established APIs and explain their contracts instead of imposing a `void` return rule on every mutator.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
