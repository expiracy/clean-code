# Clean Code for C++17

A local adaptation of pproenca's book-based clean-code skill for use while
writing, reviewing, and refactoring C++. The installable directory is
`skills/clean-code-cpp/`; all 48 rule topics are preserved and use C++17 examples.
The upstream MIT licence and source commit are included in the package.

The skill follows project conventions, resource ownership, exception policy, and
the declared C++ standard. It retains the book's naming, cohesion, boundary, and
test principles without requiring Java-style class hierarchies or arbitrary quotas.

## Install locally

From this repository, copy the complete directory to a Codex discovery location:

```bash
mkdir -p ~/.agents/skills
cp -R skills/clean-code-cpp ~/.agents/skills/
```

For project-scoped use, place the complete `clean-code-cpp` directory under that
project's `.agents/skills/`. Inspect an existing destination before replacing it.
Codex detects local skill changes; if discovery has not refreshed, restart it.

Invoke explicitly as `$clean-code-cpp`, or request C++ writing/refactoring work
that matches the skill description. Installation is separate from creating this
repository; no user-wide configuration is modified by these files.

Example request:

```text
Use $clean-code-cpp to implement this C++17 feature. Follow the repository's
ownership and error policy, add meaningful behavior tests, and refactor under
passing tests. Report the checks that actually ran.
```

## Verify the package

```bash
python3 scripts/check_skill.py
```

The check uses Python's standard library and `clang++` (or set `CXX` to another
C++17 compiler). It checks local links, the 48-rule index, metadata, syntax for
every documented cpp example with warnings as errors, and runs self-checking
examples that include `main`. It does not run unsafe incorrect examples, fetch
anything, or install dependencies.

See `VALIDATION.md` for the completed application tests and limits. The skill is
MIT licensed; it is an independent adaptation and has no upstream endorsement.

To also repeat the exception-disabled application smoke test on a compatible
macOS/Unix host, run `python3 scripts/check_skill.py --application-smoke`. The
test uses an isolated temporary directory, a directory read-error fixture, and
`/dev/fd` to observe resource release; it is not a cross-platform benchmark.
