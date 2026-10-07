---
title: Make Absence and Borrowing Explicit
impact: HIGH
impactDescription: make required values, optional values, and ownership distinguishable
tags: err, optional, nullptr, reference, ownership, lifetime
---

## Make Absence and Borrowing Explicit

Make required values, optional values, and ownership distinguishable. C++ nullability must be designed together with object lifetime; a non-null dangling pointer is still invalid.

**Incorrect:**

```cpp
#include <vector>

struct Employee { int id; };
const std::vector<Employee>* employees(bool empty,
                                       const std::vector<Employee>& staff) {
    return empty ? nullptr : &staff;
}
```

**Correct (C++17):**

```cpp
#include <cstddef>
#include <functional>
#include <optional>
#include <vector>

struct Employee { int id; };

std::optional<std::reference_wrapper<const Employee>> find_employee(
    const std::vector<Employee>& staff, int id) {
    for (const auto& employee : staff) {
        if (employee.id == id) return std::cref(employee);
    }
    return std::nullopt;
}

std::size_t employee_count(const std::vector<Employee>& staff) {
    return staff.size();
}
```

Pass a required borrowed object as a reference. Return an empty collection for an empty collection result. Use `std::optional<T>` for an optional value and `std::unique_ptr<T>` for transferred exclusive ownership when allocation is warranted.

- An optional borrowed pointer/reference must document that the owner outlives the borrow and which operations invalidate it. The search result above is invalidated by destruction or invalidating vector mutations; do not keep it across them. Prefer a copied value or stable ID when that lifetime cannot be ensured.
- C++17 has no `std::optional<T&>`; use a documented pointer or `optional<reference_wrapper<T>>` when borrowing is appropriate. An optional wrapper does not make lifetime safe by itself.
- A nullable observer pointer can be the clearest API when null means absence. Do not replace every pointer with a shared owner or manufacture a Null Object to hide an error.
- Null from a C API boundary needs checking before use; operational failures need an error representation, not just absence.

Reference: [Clean Code, Chapter 7: Error Handling](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
