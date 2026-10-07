---
title: One Concept Per Test
impact: MEDIUM
impactDescription: enables precise failure diagnosis
tags: test, assert, concept, focus
---

## One Concept Per Test

Focus each test on one behavior. Several assertions can describe that behavior's result; an arbitrary one-assertion limit creates duplicated setup and fragments the story. Use the existing framework's checks and diagnostics.

**Incorrect (an unrelated formatting check shares a calculation test):**

```cpp
#include <stdexcept>
#include <string>

struct Rectangle { int width; int height; };
int area(Rectangle rectangle) { return rectangle.width * rectangle.height; }
std::string greeting(const std::string& name) { return "Hello, " + name; }

int main() {
    if (area({3, 4}) != 12) throw std::runtime_error("area failed");
    if (greeting("Ada") != "Hello, Ada") {
        throw std::runtime_error("greeting failed");
    }
}
```

**Correct (several observations describe a single resize operation):**

```cpp
#include <stdexcept>

struct Rectangle { int width; int height; };
int area(Rectangle rectangle) { return rectangle.width * rectangle.height; }
void double_width(Rectangle& rectangle) { rectangle.width *= 2; }
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

void doubling_width_preserves_height_and_doubles_area() {
    Rectangle rectangle{3, 4};
    double_width(rectangle);
    require(rectangle.width == 6, "width must double");
    require(rectangle.height == 4, "height must stay unchanged");
    require(area(rectangle) == 24, "area must double");
}
int main() { doubling_width_preserves_height_and_doubles_area(); }
```

All three checks explain one operation's contract. These explicit checks remain active under `NDEBUG`; in a project, use its runner rather than installing a new test library for this pattern.

Keep field checks together when they validate one returned value. Split unrelated behavior into independently named tests. For costly or irreversible operations, a controlled integration scenario can check several relevant outcomes from one execution; do not repeat external side effects solely to meet an assertion count.

Reference: [Clean Code, Chapter 9: Unit Tests](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
