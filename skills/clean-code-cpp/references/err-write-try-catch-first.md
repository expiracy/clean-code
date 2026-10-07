---
title: Design Failure Paths First and Use RAII
impact: HIGH
impactDescription: define failure behavior before implementing the happy path
tags: err, raii, cleanup, tdd, exceptions-disabled
---

## Design Failure Paths First and Use RAII

Define failure behavior before implementing the happy path. C++ cleanup belongs to resource owners; it works on early returns and during exception unwinding. C++ has no finally block.

**Incorrect:**

```cpp
#include <cstdio>
#include <optional>

std::optional<unsigned char> read_first_byte(const char* path) {
    auto* file = std::fopen(path, "rb");
    if (!file) return std::nullopt;
    unsigned char byte{};
    if (std::fread(&byte, 1, 1, file) != 1) return std::nullopt;
    std::fclose(file); // The early read-failure return leaks the handle.
    return byte;
}
```

**Correct (C++17):**

```cpp
#include <cstdio>
#include <memory>
#include <variant>

enum class ReadError { open_failed, read_failed };
using ReadResult = std::variant<unsigned char, ReadError>;

ReadResult read_first_byte(const char* path) {
    using File = std::unique_ptr<std::FILE, decltype(&std::fclose)>;
    File file{std::fopen(path, "rb"), &std::fclose};
    if (!file) return ReadError::open_failed;
    unsigned char byte{};
    if (std::fread(&byte, 1, 1, file.get()) != 1) {
        return ReadError::read_failed;
    }
    return byte;
}
```

Start with tests for open failure, an empty/unreadable file, and success. The correct example also compiles with exceptions disabled and closes the handle on every exit.

- Prefer standard owners (streams, containers, smart pointers, lock guards) and existing project wrappers. A custom deleter is useful at a C API boundary.
- Define the required exception guarantee for mutating operations. RAII releases resources; it does not roll back business state or make multiple writes transactional.
- Destructors must not throw. For output files or transactions, expose and check an explicit flush/close/commit operation when its failure matters; destructor cleanup alone cannot report it reliably.
- Catch exceptions only where recovery, translation, or reporting is possible. In an exception-disabled project, use its existing error-value mechanism; do not add try/catch or throwing APIs.

Reference: [Clean Code, Chapter 7: Error Handling](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
