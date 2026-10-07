---
title: Respect Object Boundaries Rather Than Counting Dots
impact: MEDIUM-HIGH
impactDescription: avoid making a client traverse a collaborator graph to accomplish a task
tags: obj, demeter, coupling, encapsulation, fluent-api
---

## Respect Object Boundaries Rather Than Counting Dots

Avoid making a client traverse a collaborator graph to accomplish a task. The issue is dependency on another object's internals, not the number of member accesses in a C++ expression.

**Incorrect:**

```cpp
#include <string>

struct Storage { std::string directory; };
struct Options { Storage storage; };
struct Context { Options options; };

std::string output_path(const Context& context, const std::string& file) {
    return context.options.storage.directory + "/" + file;
}
```

**Correct (C++17):**

```cpp
#include <filesystem>
#include <utility>

class OutputLocation {
public:
    explicit OutputLocation(std::filesystem::path directory)
        : directory_(std::move(directory)) {}
    std::filesystem::path file_path(const std::filesystem::path& file) const {
        return directory_ / file;
    }
private:
    std::filesystem::path directory_;
};

std::filesystem::path output_path(const OutputLocation& output,
                                  const std::filesystem::path& file) {
    return output.file_path(file);
}
```

The first example is a coupling smell when the context is meant to hide storage policy. For a deliberately public configuration aggregate, direct field access is acceptable. The second exposes the needed operation through one cohesive owner.

- Standard containers, iterators, value types, DTOs, and fluent APIs are not object-graph violations merely because calls chain.
- A shorter expression can still leak representation; splitting a chain into temporary variables alone does not remove the coupling.
- A forwarding method that adds no abstraction can be needless indirection. Prefer a narrow existing capability instead of adding pass-through accessors.
- Returned views/references still need a valid owner lifetime. The Law of Demeter does not solve dangling references.
- Path composition here demonstrates responsibility, not validation of an untrusted filename or protection against directory traversal.

Reference: [Clean Code, Chapter 6: Objects and Data Structures](https://www.oreilly.com/library/view/clean-code-a/9780136083238/).
