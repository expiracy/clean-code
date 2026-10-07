---
name: clean-code-cpp
description: Use when writing, reviewing, or refactoring C++ source, especially when applying Robert C. Martin's Clean Code principles to naming, functions, comments, error handling, boundaries, types, or tests. Applies to C++ projects and their tests; use the declared language standard and project conventions.
license: MIT
metadata:
  version: "1.0.0"
  cpp-baseline: "17"
---

# Clean Code for C++

Adapted from pproenca's Clean Code skill: the same 48 rule topics and ten
categories, with C++17 examples and C++ design caveats. This is an independent
adaptation, not an official Robert C. Martin or C++ Core Guidelines skill.

## While Writing Code

1. Read the project instructions, nearby code, callers, and tests. Establish the
   declared C++ standard, exception policy, ownership, and meaningful check.
2. Make the smallest complete change in the owning unit. Use existing facilities
   and the standard library. Name concepts and effects in the project's vocabulary.
3. Read the relevant rule references below when making a design choice; do not
   load all 48 for a routine edit. Each example is a separate translation unit.
4. For new behavior or a bug, use a focused behavior test and observe the relevant
   failure before implementation when a harness is available. Before a refactor,
   establish a passing baseline and cover unprotected behavior that must survive.
5. Run the appropriate build and tests, then refactor under green. Use existing
   clang-format/clang-tidy configuration and suitable sanitizers when available.
   Report the commands and results; identify checks that could not run.

## C++ Adaptation Rules

- **Standard:** these examples target C++17. Follow the project's actual standard;
  do not silently upgrade it. `std::span`, ranges, concepts, and `std::jthread`
  require C++20; `std::expected` requires C++23. Use them only in a compatible project.
- **Lifetime:** prefer value semantics, the rule of zero, and RAII. Distinguish
  owned resources from borrows. References, pointers, iterators, and string views
  do not extend lifetime; document invalidation. Exclusive ownership uses an
  existing owner or `unique_ptr`; shared ownership needs an actual shared lifetime.
- **Errors:** preserve the project's exception/result/error-code contract.
  Expected absence can be optional; failure needs a useful error. RAII handles
  cleanup on early return and unwinding. Catch where the caller can act; destructors
  do not throw. Resource cleanup alone does not establish transaction atomicity.
- **Abstraction:** choose concrete values, aggregates, free functions, templates,
  enums, variants, or runtime interfaces according to the problem. A closed enum
  with an exhaustive switch is legitimate. Add no hierarchy, factory, forwarding
  layer, allocation, or implicit state solely to satisfy a book pattern or quota.
- **Judgment:** function length and argument count are prompts to inspect cohesion,
  not pass/fail limits. Keep explicit dependencies. Command/query separation permits
  clear mutation results (extraction, insertion, erase, atomic read-modify-write);
  splitting them must not introduce a check-then-act race or change behavior.
- **Conventions:** preserve the project's member suffix/prefix, names, header/source
  layout, public API, and formatter. C++ reserved identifiers are language rules;
  avoiding Hungarian notation is a naming preference. Review changes in scope and
  report unrelated smells without turning a feature into a whole-project cleanup.

## Rule Categories

The index keeps upstream ordering and impact labels for traceability. Correctness,
resource safety, and the caller's contract take precedence over style rankings.

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Meaningful Names | CRITICAL | `name-` |
| 2 | Functions | CRITICAL | `func-` |
| 3 | Comments | HIGH | `cmt-` |
| 4 | Formatting | HIGH | `fmt-` |
| 5 | Error Handling | HIGH | `err-` |
| 6 | Objects and Data Structures | MEDIUM-HIGH | `obj-` |
| 7 | Boundaries | MEDIUM-HIGH | `bound-` |
| 8 | Classes and Systems | MEDIUM-HIGH | `class-` |
| 9 | Unit Tests | MEDIUM | `test-` |
| 10 | Emergence and Simple Design | MEDIUM | `emerge-` |

## Quick Reference

### 1. Meaningful Names (CRITICAL)

- [`name-intention-revealing`](references/name-intention-revealing.md) - Use names that reveal intent
- [`name-avoid-disinformation`](references/name-avoid-disinformation.md) - Avoid misleading names
- [`name-meaningful-distinctions`](references/name-meaningful-distinctions.md) - Make meaningful distinctions
- [`name-pronounceable`](references/name-pronounceable.md) - Use pronounceable names
- [`name-searchable`](references/name-searchable.md) - Use searchable names
- [`name-avoid-encodings`](references/name-avoid-encodings.md) - Avoid encodings in names
- [`name-class-noun`](references/name-class-noun.md) - Use domain names for types
- [`name-method-verb`](references/name-method-verb.md) - Use verb phrases for method names

### 2. Functions (CRITICAL)

- [`func-small`](references/func-small.md) - Keep cohesive functions understandable
- [`func-one-thing`](references/func-one-thing.md) - Functions should do one thing
- [`func-abstraction-level`](references/func-abstraction-level.md) - Maintain one level of abstraction
- [`func-minimize-arguments`](references/func-minimize-arguments.md) - Minimize function arguments
- [`func-no-side-effects`](references/func-no-side-effects.md) - Avoid side effects
- [`func-command-query-separation`](references/func-command-query-separation.md) - Separate commands from queries
- [`func-dry`](references/func-dry.md) - Do not repeat yourself

### 3. Comments (HIGH)

- [`cmt-express-in-code`](references/cmt-express-in-code.md) - Express yourself in code, not comments
- [`cmt-explain-intent`](references/cmt-explain-intent.md) - Use comments to explain intent
- [`cmt-avoid-redundant`](references/cmt-avoid-redundant.md) - Avoid redundant comments
- [`cmt-avoid-commented-out-code`](references/cmt-avoid-commented-out-code.md) - Delete commented-out code
- [`cmt-warning-consequences`](references/cmt-warning-consequences.md) - Use warning comments for consequences

### 4. Formatting (HIGH)

- [`fmt-vertical-formatting`](references/fmt-vertical-formatting.md) - Use vertical formatting for readability
- [`fmt-horizontal-alignment`](references/fmt-horizontal-alignment.md) - Avoid horizontal alignment
- [`fmt-team-rules`](references/fmt-team-rules.md) - Follow team formatting rules
- [`fmt-indentation`](references/fmt-indentation.md) - Respect indentation rules

### 5. Error Handling (HIGH)

- [`err-use-exceptions`](references/err-use-exceptions.md) - Separate error handling from happy path
- [`err-write-try-catch-first`](references/err-write-try-catch-first.md) - Design failure paths first; use RAII
- [`err-provide-context`](references/err-provide-context.md) - Provide context with exceptions
- [`err-define-by-caller-needs`](references/err-define-by-caller-needs.md) - Define exceptions by caller needs
- [`err-avoid-null`](references/err-avoid-null.md) - Make absence, borrowing, and ownership explicit

### 6. Objects and Data Structures (MEDIUM-HIGH)

- [`obj-data-abstraction`](references/obj-data-abstraction.md) - Hide data behind abstractions
- [`obj-data-object-asymmetry`](references/obj-data-object-asymmetry.md) - Understand data/object anti-symmetry
- [`obj-law-of-demeter`](references/obj-law-of-demeter.md) - Respect object boundaries rather than count dots
- [`obj-avoid-hybrids`](references/obj-avoid-hybrids.md) - Protect invariants; keep useful value types
- [`obj-dto`](references/obj-dto.md) - Use DTOs for data transfer

### 7. Boundaries (MEDIUM-HIGH)

- [`bound-wrap-third-party`](references/bound-wrap-third-party.md) - Wrap third-party APIs
- [`bound-learning-tests`](references/bound-learning-tests.md) - Write learning tests for third-party code

### 8. Classes and Systems (MEDIUM-HIGH)

- [`class-small`](references/class-small.md) - Keep classes small
- [`class-cohesion`](references/class-cohesion.md) - Maintain class cohesion
- [`class-organize-for-change`](references/class-organize-for-change.md) - Organize classes for change
- [`class-isolate-from-change`](references/class-isolate-from-change.md) - Isolate classes from change
- [`class-separate-concerns`](references/class-separate-concerns.md) - Separate construction from use

### 9. Unit Tests (MEDIUM)

- [`test-first-law`](references/test-first-law.md) - Follow the three laws of TDD
- [`test-keep-clean`](references/test-keep-clean.md) - Keep tests clean
- [`test-one-assert`](references/test-one-assert.md) - One concept per test
- [`test-first-principles`](references/test-first-principles.md) - Follow FIRST principles
- [`test-build-operate-check`](references/test-build-operate-check.md) - Use Build-Operate-Check pattern

### 10. Emergence and Simple Design (MEDIUM)

- [`emerge-simple-design`](references/emerge-simple-design.md) - Follow the four rules of simple design
- [`emerge-expressiveness`](references/emerge-expressiveness.md) - Maximize expressiveness

## Supporting Material

- [Section definitions](references/_sections.md): topic boundaries and priorities.
- [Rule authoring example](assets/templates/_template.md): when extending the rule set.
- [Source provenance](UPSTREAM.md) and [metadata](metadata.json): attribution and baseline.
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines):
  check C++ contracts and resource semantics when adapting a rule.

Examples demonstrate a design choice in a small context; they do not establish
that every rewrite is suitable for every program. Preserve behavior, ABI/API,
thread safety, and measured performance requirements when they matter.
