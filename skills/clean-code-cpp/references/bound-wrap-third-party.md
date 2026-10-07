---
title: Wrap Third-Party APIs
impact: HIGH
impactDescription: localizes dependency-specific units and error handling
tags: bound, boundary, wrapper, third-party, dependency
---

## Wrap Third-Party APIs

Introduce a boundary when it translates vendor-specific units, errors, resource lifetimes, or concepts into what callers actually need. Keep the boundary small and own it by value where possible. A pass-through wrapper around a stable API adds little value.

The `vendor` namespace below is an illustrative API stand-in, not a real library contract.

**Incorrect (each caller must understand vendor codes and units):**

```cpp
#include <stdexcept>

namespace vendor {
struct Reading { int status; int millivolts; };
Reading sample(int channel) {
    return channel == 2 ? Reading{0, 3300} : Reading{1, 0};
}
}

double supply_voltage(int channel) {
    const auto reading = vendor::sample(channel);
    if (reading.status != 0) throw std::runtime_error("code 1");
    return reading.millivolts / 1000.0;
}

int main() { return supply_voltage(2) > 3.0 ? 0 : 1; }
```

**Correct (one boundary exposes the application concept):**

```cpp
#include <stdexcept>
#include <string>

namespace vendor {
struct Reading { int status; int millivolts; };
Reading sample(int channel) {
    return channel == 2 ? Reading{0, 3300} : Reading{1, 0};
}
}

class VoltageSensor {
    int channel_;
public:
    explicit VoltageSensor(int channel) : channel_{channel} {}
    double volts() const {
        const auto reading = vendor::sample(channel_);
        if (reading.status != 0) {
            throw std::runtime_error("sensor read failed on channel " +
                                     std::to_string(channel_));
        }
        return reading.millivolts / 1000.0;
    }
};

int main() {
    const VoltageSensor supply{2};
    return supply.volts() > 3.0 ? 0 : 1;
}
```

Wrap the actual dependency, and translate only failures the caller can handle consistently; preserve useful causes and context. Resource-owning vendor handles need RAII cleanup at this boundary. Prefer the rule of zero when the vendor already supplies a safe owning type.

Do not wrap standard containers or add virtual interfaces just to mirror another API. Add a test seam only when a real dependency needs substitution, using a function, reference, or template as appropriate.

Reference: [Clean Code, Chapter 8: Boundaries](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
