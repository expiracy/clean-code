---
title: Write Learning Tests for Third-Party Code
impact: MEDIUM
impactDescription: checks the dependency behavior that the application relies on
tags: bound, boundary, learning-tests, third-party, testing
---

## Write Learning Tests for Third-Party Code

Before integrating an unfamiliar API, test the particular behavior your application needs: missing values, failures, ownership, or units. Keep those learning tests when upgrading the dependency. They detect changes only in the assumptions they exercise.

These self-contained examples use an illustrative vendor API. In the project, include the actual dependency and verify its documented behavior with the existing test framework; the stand-in below is not evidence about a real library.

**Incorrect (application silently guesses the meaning of a missing reading):**

```cpp
#include <optional>

namespace vendor {
std::optional<int> read_temperature(bool connected) {
    return connected ? std::optional<int>{215} : std::nullopt;
}
}

int temperature_celsius(bool connected) {
    // Assumes whole degrees and treats missing data as a valid zero.
    return vendor::read_temperature(connected).value_or(0);
}

int main() { return temperature_celsius(false); }
```

**Correct (learning checks record the units and missing-value contract):**

```cpp
#include <optional>
#include <stdexcept>

namespace vendor {
std::optional<int> read_temperature(bool connected) {
    return connected ? std::optional<int>{215} : std::nullopt;
}
}

void require(bool condition) {
    if (!condition) throw std::runtime_error("vendor contract changed");
}

int main() {
    const auto reading = vendor::read_temperature(true);
    require(reading.has_value());
    require(*reading == 215); // Vendor contract: tenths of a degree Celsius.
    require(!vendor::read_temperature(false).has_value());
}
```

Use a controlled fixture or documented sandbox for integration checks. Keep tests repeatable, avoid production devices/accounts, and do not replace required integration coverage with a fake that merely repeats your assumption. The explicit checks above still run when `NDEBUG` is defined.

Reference: [Clean Code, Chapter 8: Boundaries](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
