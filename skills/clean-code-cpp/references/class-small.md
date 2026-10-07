---
title: Keep Classes Small
impact: MEDIUM
impactDescription: enables comprehension and focused testing
tags: class, size, srp, cohesion
---

## Keep Classes Small

Measure a class by its responsibilities, not a fixed line count. The Single Responsibility Principle asks which independent requirements could make it change. Separate those requirements when doing so makes the current code easier to understand and maintain.

**Incorrect (one class manages totals and a presentation preference):**

```cpp
#include <string>
#include <vector>

class Dashboard {
    std::vector<int> sales_;
    std::string language_ = "en";
public:
    void record_sale(int amount) { sales_.push_back(amount); }
    int total_sales() const {
        int total = 0;
        for (int amount : sales_) total += amount;
        return total;
    }
    void use_french() { language_ = "fr"; }
    std::string heading() const {
        return language_ == "fr" ? "Ventes" : "Sales";
    }
};

int main() {
    Dashboard dashboard;
    dashboard.record_sale(10);
    return dashboard.total_sales() == 10 ? 0 : 1;
}
```

**Correct (sales state is separate from presentation choices):**

```cpp
#include <numeric>
#include <string_view>
#include <vector>

class Sales {
    std::vector<int> amounts_;
public:
    void record(int amount) { amounts_.push_back(amount); }
    int total() const {
        return std::accumulate(amounts_.begin(), amounts_.end(), 0);
    }
};

enum class Language { english, french };
std::string_view sales_heading(Language language) {
    return language == Language::french ? "Ventes" : "Sales";
}

int main() {
    Sales sales;
    sales.record(10);
    return sales.total() == 10 &&
           sales_heading(Language::french) == "Ventes" ? 0 : 1;
}
```

A plain value type or free function can carry a responsibility without a new class. Use standard containers and the rule of zero; do not add getter/setter layers or one-method interfaces merely to make classes smaller. Keep tightly related behavior together even when it takes more lines.

Reference: [Clean Code, Chapter 10: Classes](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
