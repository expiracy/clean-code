---
title: Use Comments to Explain Intent
impact: HIGH
impactDescription: preserves decision rationale for future readers
tags: cmt, intent, why, rationale
---

## Use Comments to Explain Intent

Comments add value when they explain a decision or constraint that cannot be inferred from the implementation. Keep the rationale close to the code it explains.

**Before (comments narrate visible operations):**

```cpp
#include <algorithm>
#include <chrono>
#include <vector>

struct Session {
    std::chrono::system_clock::time_point lastUsed;
};

void orderSessions(std::vector<Session>& sessions) {
    // Sort the sessions.
    std::stable_sort(sessions.begin(), sessions.end(),
                     [](const Session& left, const Session& right) {
                         // Compare their timestamps.
                         return left.lastUsed > right.lastUsed;
                     });
}
```

**After (the comment explains the ordering policy):**

```cpp
#include <algorithm>
#include <chrono>
#include <vector>

struct Session {
    std::chrono::system_clock::time_point lastUsed;
};

void orderSessions(std::vector<Session>& sessions) {
    // Operators look for the session they just used first; keep ties in input order.
    std::stable_sort(sessions.begin(), sessions.end(),
                     [](const Session& left, const Session& right) {
                         return left.lastUsed > right.lastUsed;
                     });
}
```

**Useful comment subjects:**
- A business requirement or external format constraint.
- An algorithm choice supported by actual requirements or measurements.
- A non-obvious API limitation, lifetime rule, or compatibility workaround.
- A temporary follow-up tied to a concrete issue when the project uses TODOs.
- Required copyright, license, and attribution information.

Do not invent performance claims or issue links. If a rationale changes, update the comment with the code; comments can become stale even when they explain intent.

Reference: [Clean Code, Chapter 4: Comments](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
