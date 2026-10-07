---
title: Define Errors by Caller Needs
impact: HIGH
impactDescription: classify failures by the action a caller can take
tags: err, wrapper, classification, recovery
---

## Define Errors by Caller Needs

Classify failures by the action a caller can take. Translate vendor-specific details at a real boundary while retaining the original cause.

**Incorrect:**

```cpp
enum class VendorFailure { no_device, disconnected, permission_denied };
enum class Recovery { reconnect, request_access };

Recovery choose_recovery(VendorFailure failure) {
    switch (failure) {
    case VendorFailure::no_device: return Recovery::reconnect;
    case VendorFailure::disconnected: return Recovery::reconnect;
    case VendorFailure::permission_denied: return Recovery::request_access;
    }
    return Recovery::reconnect;
}
```

**Correct (C++17):**

```cpp
#include <system_error>

enum class VendorFailure { no_device, disconnected, permission_denied };
enum class PortFailure { unavailable, access_denied };
enum class Recovery { reconnect, request_access };
struct PortError {
    PortFailure kind;
    std::error_code cause;
};

PortError translate(VendorFailure failure, std::error_code cause) {
    return {failure == VendorFailure::permission_denied
                ? PortFailure::access_denied : PortFailure::unavailable,
            cause};
}

Recovery choose_recovery(const PortError& error) {
    return error.kind == PortFailure::access_denied
        ? Recovery::request_access : Recovery::reconnect;
}
```

The first design makes the caller know the vendor's taxonomy. The second has a local error contract aligned with recovery and retains a cause for diagnostics.

- With exceptions, translate specific vendor exceptions into the smallest useful local set and preserve the cause. Do not flatten all failures into one message if recovery differs.
- With error values, use the project's enum/result/error-code convention. A success value and an error must not be simultaneously present; use an existing result type or a discriminated union when necessary.
- Do not build a new exception hierarchy or wrapper layer when the existing API already matches caller needs. Retry only operations known to be safe to retry.

Reference: [Clean Code, Chapter 7: Error Handling](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
