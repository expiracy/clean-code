---
title: Separate Construction from Use
impact: MEDIUM
impactDescription: separates startup choices from application behavior
tags: class, construction, factories, separation
---

## Separate Construction from Use

Build external dependencies at the application entry point, then pass the required operations or objects to the code that uses them. Ordinary constructors, references, and callables usually suffice; a dependency injection framework or abstract factory is not a prerequisite.

**Incorrect (each operation chooses and constructs its output destination):**

```cpp
#include <sstream>
#include <string>

class OrderProcessor {
public:
    std::string confirm(int order_id) const {
        std::ostringstream message;
        message << "Confirmed order " << order_id << '\n';
        return message.str();
    }
    void process(int order_id) const {
        std::ostringstream buried_destination;
        buried_destination << confirm(order_id);
        // Caller cannot select or observe this destination.
    }
};

int main() { OrderProcessor{}.process(7); }
```

**Correct (startup supplies the output destination):**

```cpp
#include <ostream>
#include <sstream>
#include <stdexcept>

class OrderProcessor {
    std::ostream& confirmations_;
public:
    explicit OrderProcessor(std::ostream& confirmations)
        : confirmations_{confirmations} {}
    void process(int order_id) const {
        confirmations_ << "Confirmed order " << order_id << '\n';
        if (!confirmations_) throw std::runtime_error("confirmation failed");
    }
};

int main() {
    std::ostringstream confirmations;
    const OrderProcessor processor{confirmations};
    processor.process(7);
    if (confirmations.str() != "Confirmed order 7\n") {
        throw std::runtime_error("confirmation missing");
    }
}
```

The entry point owns `confirmations`, which outlives the processor borrowing it. A production entry point can supply the actual configured destination. Keep such lifetime relationships explicit; avoid shared ownership when one owner is enough.

Construct cheap local values where they are used. Move construction outward when configuration, resource acquisition, replacement in tests, or lifetime management makes it a separate concern.

Reference: [Clean Code, Chapter 11: Systems](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
