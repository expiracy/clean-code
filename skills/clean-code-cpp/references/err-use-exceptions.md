---
title: Separate Error Handling from the Happy Path
impact: HIGH
impactDescription: keep successful work readable and preserve failures
tags: err, exceptions, error-code, expected, separation
---

## Separate Error Handling from the Happy Path

Keep successful work readable and preserve failures. Choose the error mechanism supported by the project, rather than importing Java exception rules.

**Incorrect:**

```cpp
#include <system_error>

std::error_code complete_upload(std::error_code validation,
                                std::error_code storage) {
    if (!validation) {
        if (!storage) {
            return {};
        } else {
            return storage;
        }
    } else {
        return validation;
    }
}
```

**Correct (C++17):**

```cpp
#include <system_error>

std::error_code complete_upload(std::error_code validation,
                                std::error_code storage) {
    if (validation) return validation;
    if (storage) return storage;
    return {};
}
```

This small example isolates control flow; a real operation checks each result immediately after the corresponding work, stopping before dependent work on failure.

- Use exceptions when that is the project's contract. Catch specific exceptions by `const` reference, keep the original cause when translating, and handle once at the level that can act.
- Use an existing result type or `std::error_code` when errors are values. `std::optional<T>` models absence, not the reason for an operational failure. `std::variant<T, Error>` is a C++17 option when alternatives clarify a local API.
- `std::expected` is C++23; it is not available in the C++17 baseline. Do not introduce a custom Result framework just for this rule.
- Do not swallow a failure by returning an empty value or logging and reporting success. Do not promise atomicity for a sequence of separately committed operations.
- Expected domain outcomes (such as a search miss) can be ordinary values. Profile before changing error policy for alleged performance gains.

Reference: [Clean Code, Chapter 3: Functions and Chapter 7: Error Handling](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
