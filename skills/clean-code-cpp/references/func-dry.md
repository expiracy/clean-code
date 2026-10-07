---
title: Do Not Repeat Yourself
impact: CRITICAL
impactDescription: keeps shared domain rules consistent
tags: func, dry, duplication, abstraction
---

## Do Not Repeat Yourself

Give one domain rule an authoritative implementation when its callers need to change together. Similar-looking code is not necessarily the same knowledge.

**Before (the same device-name policy is repeated):**

```cpp
#include <map>
#include <stdexcept>
#include <string>
#include <utility>

void addDevice(std::map<int, std::string>& devices, int id, std::string name) {
    if (name.empty() || name.find('/') != std::string::npos) {
        throw std::invalid_argument("Device name must be nonempty without '/'");
    }
    devices.emplace(id, std::move(name));
}

void renameDevice(std::map<int, std::string>& devices, int id, std::string name) {
    if (name.empty() || name.find('/') != std::string::npos) {
        throw std::invalid_argument("Device name must be nonempty without '/'");
    }
    devices.at(id) = std::move(name);
}
```

**After (both operations use the same rule):**

```cpp
#include <map>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>

void validateDeviceName(std::string_view name) {
    if (name.empty() || name.find('/') != std::string_view::npos) {
        throw std::invalid_argument("Device name must be nonempty without '/'");
    }
}

void addDevice(std::map<int, std::string>& devices, int id, std::string name) {
    validateDeviceName(name);
    devices.emplace(id, std::move(name));
}

void renameDevice(std::map<int, std::string>& devices, int id, std::string name) {
    validateDeviceName(name);
    devices.at(id) = std::move(name);
}
```

The helper captures a shared naming contract without adding a validation framework. Map insertion and missing-ID behavior remain the callers' existing contracts.

**When to keep duplication:**
- Similar code may implement policies that will evolve independently.
- A shared helper that needs many mode switches can create more coupling than it removes.
- Across independent components, shared libraries can add unwanted deployment coupling.
- Do not wait for a fixed number of copies when an actual shared invariant is already clear; do not abstract merely because a threshold was reached.

Reference: [Clean Code, Chapter 3: Functions](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
