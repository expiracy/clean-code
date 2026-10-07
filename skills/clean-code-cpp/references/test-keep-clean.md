---
title: Keep Tests Clean
impact: MEDIUM
impactDescription: keeps behavior checks readable and maintainable
tags: test, clean, maintainability, quality
---

## Keep Tests Clean

Treat test code as maintained code. Describe the behavior, keep setup visible, and give failures useful context. Reuse the project's existing framework and modest helpers; avoid fixture hierarchies that conceal the inputs and action.

**Incorrect (one vaguely named test mixes different behaviors):**

```cpp
#include <stdexcept>
#include <string>
#include <utility>

struct Profile {
    std::string name;
    bool active = false;
    void activate() { active = true; }
    void rename(std::string value) { name = std::move(value); }
};

int main() {
    Profile p{"Ada"};
    p.activate();
    p.rename("Grace");
    if (!p.active || p.name != "Grace") {
        throw std::runtime_error("test1 failed");
    }
}
```

**Correct (names and checks explain each behavior):**

```cpp
#include <stdexcept>
#include <string>
#include <utility>

struct Profile {
    std::string name;
    bool active = false;
    void activate() { active = true; }
    void rename(std::string value) { name = std::move(value); }
};
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

void activation_enables_profile() {
    Profile profile{"Ada"};
    profile.activate();
    require(profile.active, "activation must enable the profile");
}
void renaming_preserves_activation() {
    Profile profile{"Ada", true};
    profile.rename("Grace");
    require(profile.name == "Grace", "new name must replace old name");
    require(profile.active, "renaming must preserve activation");
}
int main() {
    activation_enables_profile();
    renaming_preserves_activation();
}
```

Prefer checks of returned results and observable state over tests coupled to private members or call order. Test externally meaningful interactions when they are the behavior, such as sending a required notification. Keep representative inputs and expected values explicit; the checks above stay enabled under `NDEBUG`.

Reference: [Clean Code, Chapter 9: Unit Tests](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
