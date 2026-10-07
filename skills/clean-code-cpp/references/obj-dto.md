---
title: Use Explicit Data Types at Transfer Boundaries
impact: MEDIUM
impactDescription: represent transferred data with fields intended for that consumer
tags: obj, dto, transfer, boundary, owning-data
---

## Use Explicit Data Types at Transfer Boundaries

Represent transferred data with fields intended for that consumer. A C++ aggregate can be a DTO; it does not need accessors, heap allocation, or an Active Record layer.

**Incorrect:**

```cpp
#include <string>

struct User {
    std::string display_name;
    std::string password_hash;
    std::string access_token;
};

User response_payload(const User& user) {
    return user; // An external serializer could expose every field.
}
```

**Correct (C++17):**

```cpp
#include <string>

struct User {
    std::string display_name;
    std::string password_hash;
    std::string access_token;
};
struct UserSummary { std::string display_name; };

UserSummary response_payload(const User& user) {
    return {user.display_name};
}
```

Define serialization explicitly; an aggregate alone is not a serialization format or an authorization check. The owning `std::string` in the response remains valid after the source user is destroyed.

- Use owning values for queued/asynchronous messages unless the borrow is explicitly safe. `std::string_view`, spans, pointers, and references do not extend the owner's lifetime.
- Validate external bytes before constructing trusted domain values. Layout, padding, endianness, and ABI make raw memory copies an unsuitable general wire format.
- Separate DTOs when a boundary needs a different contract. Reuse an existing value type when it already exposes exactly the intended data; avoid one DTO per function by habit.

Reference: [Clean Code, Chapter 6: Objects and Data Structures](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
