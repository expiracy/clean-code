# Adding a C++ Rule

Copy a nearby rule's frontmatter and structure. Keep the principle, then write
one focused before/after pair, the C++ contract and useful counterexamples, and
the original source citation. Use qualitative impact descriptions unless a
measurement directly supports a numerical claim. Do not copy book passages.

Each cpp block must be a self-contained C++17 translation unit. Label a newer
standard explicitly and update validation if that standard is intentionally used.

For example, a rule about ownership can contrast ambiguous allocation with an
owner returned by value:

**Incorrect:**

```cpp
struct Session { int id; };
Session* make_session(int id) {
    return new Session{id};
}
```

**Correct (exclusive ownership is part of the contract):**

```cpp
#include <memory>
struct Session { int id; };
std::unique_ptr<Session> make_session(int id) {
    return std::make_unique<Session>(Session{id});
}
```

For this tiny type, a plain `Session` value is simpler still if a stable allocated
identity is unnecessary. The owner example demonstrates a specific resource
contract, not a requirement to allocate every object.
