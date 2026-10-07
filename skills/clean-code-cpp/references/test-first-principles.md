---
title: Follow FIRST Principles
impact: MEDIUM
impactDescription: keeps tests useful, repeatable, and independently runnable
tags: test, first, fast, independent, repeatable
---

## Follow FIRST Principles

FIRST means Fast, Independent, Repeatable, Self-Validating, and Timely. Keep focused unit checks quick and isolated. Integration tests still need real boundaries and controlled fixtures; replacing every dependency with a fake can hide integration failures.

**Incorrect (one test leaves state for the next):**

```cpp
#include <stdexcept>
#include <string>

std::string shared_name;
void creates_user() { shared_name = "Ada"; }
void renames_user() {
    if (shared_name != "Ada") throw std::runtime_error("run creation first");
    shared_name = "Grace";
}

int main() {
    creates_user();
    renames_user();
}
```

**Correct (each test creates its own input and validates behavior):**

```cpp
#include <stdexcept>
#include <string>
#include <utility>

struct User {
    std::string name;
    void rename(std::string replacement) { name = std::move(replacement); }
};
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

void retains_initial_name() {
    const User user{"Ada"};
    require(user.name == "Ada", "initial name was lost");
}
void rename_replaces_name() {
    User user{"Ada"};
    user.rename("Grace");
    require(user.name == "Grace", "rename did not replace the name");
}
int main() {
    rename_replaces_name();
    retains_initial_name();
}
```

- **Fast:** keep unit tests local; put necessary network/device checks in a controlled integration suite.
- **Independent:** own test state and clean up resources; tests should not require an execution order.
- **Repeatable:** control clocks, randomness, inputs, and external fixtures.
- **Self-Validating:** report pass/fail automatically; do not rely on inspecting log output.
- **Timely:** add meaningful failing checks for behavior changes and characterization checks before refactors.

Use the project's existing runner. If required infrastructure is unavailable, state which checks could not run. Standalone examples here use explicit runtime checks, so defining `NDEBUG` cannot silently disable them.

Reference: [Clean Code, Chapter 9: Unit Tests](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
