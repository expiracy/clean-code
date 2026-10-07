---
title: Avoid Horizontal Alignment
impact: MEDIUM
impactDescription: prevents alignment maintenance burden
tags: fmt, horizontal, alignment, whitespace
---

## Avoid Horizontal Alignment

Manual column alignment can make small edits touch many unrelated lines. Prefer ordinary spacing unless the project's formatter deliberately uses aligned declarations or assignments.

**Before (hand-aligned columns invite reformatting):**

```cpp
#include <string>

struct DeviceSettings {
    std::string   label;
    int           sampleIntervalSeconds;
    bool          enabled;
};

void enable(DeviceSettings& settings) {
    settings.label                 = "Outdoor sensor";
    settings.sampleIntervalSeconds = 15;
    settings.enabled               = true;
}
```

**After (spacing follows the local formatter style):**

```cpp
#include <string>

struct DeviceSettings {
    std::string label;
    int sampleIntervalSeconds;
    bool enabled;
};

void enable(DeviceSettings& settings) {
    settings.label = "Outdoor sensor";
    settings.sampleIntervalSeconds = 15;
    settings.enabled = true;
}
```

**Use the existing policy:**
- A longer identifier should not require manually padding surrounding code.
- `clang-format` can intentionally align declarations; honor that configuration.
- Tables or carefully arranged data can have a real readability reason for alignment.
- Do not change the project's alignment options during an unrelated task.

The example illustrates a style without aligned columns. Project consistency takes precedence, and formatting changes should stay within the requested scope.

Reference: [Clean Code, Chapter 5: Formatting](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
