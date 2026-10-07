---
title: Provide Context with Errors
impact: HIGH
impactDescription: error reports should identify the failed operation and useful diagnostic context
tags: err, context, messages, system-error, nested-exception
---

## Provide Context with Errors

Error reports should identify the failed operation and useful diagnostic context. Preserve the underlying error, including its category, rather than replacing it with a vague message.

**Incorrect:**

```cpp
#include <stdexcept>
#include <system_error>

void report_config_failure(std::error_code error) {
    if (error) throw std::runtime_error("Failed");
}
```

**Correct (C++17):**

```cpp
#include <string>
#include <system_error>

void report_config_failure(const std::string& path, std::error_code error) {
    if (error) {
        throw std::system_error(error, "loading configuration from " + path);
    }
}
```

The example assumes an exception-enabled contract. For error-value APIs, include the operation and original `std::error_code` in the existing error record. For exception-to-exception translation, `std::throw_with_nested` can preserve a cause when the reporting layer understands nested exceptions.

- Name what was attempted and the relevant safe identifier or path.
- Avoid secrets, credentials, and personal data in diagnostics. Redact context at trust boundaries.
- Catch `const std::exception&`, not by value. Catch at a point that can recover or report, rather than decorating and rethrowing at every layer.
- Context cannot substitute for handling a failure or preserving program invariants.

Reference: [Clean Code, Chapter 7: Error Handling](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
