---
title: Use Intention-Revealing Names
impact: CRITICAL
impactDescription: eliminates mental mapping overhead
tags: name, intention, readability, clarity
---

## Use Intention-Revealing Names

Choose names that expose the domain meaning of data and operations. Prefer an existing domain type over positional records when that type makes the representation easier to understand.

**Before (readers must decode positions and values):**

```cpp
#include <array>
#include <vector>

std::vector<std::array<int, 2>> getThem(
    const std::vector<std::array<int, 2>>& theList) {
    std::vector<std::array<int, 2>> list1;
    for (const auto& x : theList) {
        if (x[0] == 4) {
            list1.push_back(x);
        }
    }
    return list1;
}
```

**After (the minesweeper rule is visible):**

```cpp
#include <vector>

enum class CellState { covered, uncovered, flagged };
struct Cell {
    CellState state;
    int adjacentMines;
};

std::vector<Cell> flaggedCells(const std::vector<Cell>& board) {
    std::vector<Cell> flagged;
    for (const Cell& cell : board) {
        if (cell.state == CellState::flagged) {
            flagged.push_back(cell);
        }
    }
    return flagged;
}
```

**Keep names proportionate to their scope:**
- `i` is useful for a small index loop; a domain index deserves a domain name.
- Conventional mathematical names are appropriate for mathematical code.
- A short lambda parameter can be clearer than a sentence-length identifier.
- Follow the repository's casing and spelling conventions.

A clear name does not remove the need to document a non-obvious contract or the reason for a business rule.

Reference: [Clean Code, Chapter 2: Meaningful Names](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
