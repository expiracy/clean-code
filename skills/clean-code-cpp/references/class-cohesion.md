---
title: Maintain Class Cohesion
impact: MEDIUM
impactDescription: keeps related state and behavior together
tags: class, cohesion, variables, methods
---

## Maintain Class Cohesion

A cohesive class groups state and operations that maintain one concept or invariant. Count responsibilities rather than fields touched: a method need not access every member, and touching unrelated fields does not make it cohesive.

**Incorrect (independent features bundled as one utility):**

```cpp
#include <string>
#include <utility>
#include <vector>

class Utility {
    std::vector<std::string> users_;
    std::vector<std::string> notifications_;
public:
    void save_user(std::string user) { users_.push_back(std::move(user)); }
    void notify(std::string message) {
        notifications_.push_back(std::move(message));
    }
    std::size_t user_count() const { return users_.size(); }
};

int main() {
    Utility utility;
    utility.save_user("Ada");
    utility.notify("Deploy complete");
    return utility.user_count() == 1 ? 0 : 1;
}
```

**Correct (operations maintain the same stack abstraction):**

```cpp
#include <stdexcept>
#include <vector>

class Stack {
    std::vector<int> elements_;
public:
    std::size_t size() const { return elements_.size(); }
    void push(int value) { elements_.push_back(value); }
    int pop() {
        if (elements_.empty()) throw std::underflow_error("empty stack");
        const int value = elements_.back();
        elements_.pop_back();
        return value;
    }
};

int main() {
    Stack stack;
    stack.push(42);
    return stack.pop() == 42 && stack.size() == 0 ? 0 : 1;
}
```

If a subset of methods and fields forms a separate responsibility, extract it. Prefer composition to extracting subclasses. Do not duplicate state such as a stored stack size when the container already knows it. Standard containers and value members provide cleanup, copying, and moving without custom special members.

Reference: [Clean Code, Chapter 10: Classes](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
