# Validation

Target: C++17. Source: pproenca/dot-skills clean-code version 1.0.7 at commit
`cf93c57cac89d6fc3e4194686000411567f5caf3`. Checked on 7 October 2026 with
Apple Clang 17.0.0 on macOS arm64.

## Package and examples

- Codex's bundled skill-creator `quick_validate.py`: passed.
- All 49 YAML frontmatters parsed; all upstream reference filenames preserved.
- Original MIT licence retained verbatim inside the installable skill.
- `python3 scripts/check_skill.py`: all 48 rule topics indexed, local links and
  metadata checked, 98 cpp blocks compiled individually using C++17 and
  `-Wall -Wextra -Wpedantic -Werror`.
- The 14 explicitly correct examples containing `main` executed successfully
  with `-DNDEBUG`, so their checks did not silently depend on debug assertions.
- Incorrect examples are syntax checked but not executed. Many examples are
  small design illustrations; syntax checking does not establish their domain
  behavior or prove before/after equivalence for every possible input.

The portable package check requires Python's standard library and a compiler.
PyYAML was used only in the author's temporary validation environment to run
Codex's separate validator; the skill and repository check do not require it.

## Baseline reference test

An independent agent evaluated the unadapted reference material before edits.
The request covered C++17 resource cleanup without exceptions, state-changing
container extraction, local naming, and reserved identifiers. General naming
and idiomatic error-policy advice was already applicable. The original material
had no C++ examples, RAII cleanup example, extraction-specific caveat, or
reserved-identifier guidance.

The adaptation supplies these C++ references. This comparison identifies source
gaps; it is not a controlled measurement of model output quality.

## Application smoke test and independent review

A fresh agent applied the skill to an exception-disabled first-byte reader. It
used a C++17 variant result and an RAII FILE owner. The sources are retained in
`tests/application-smoke/`. Run them with
`python3 scripts/check_skill.py --application-smoke` on a compatible macOS/Unix
host. They compile with `-fno-exceptions`, warnings as errors, and `-DNDEBUG`.

Eight functional cases passed: missing/null/empty path, empty file, read error,
first byte of a two-byte file, zero byte, and 0xff. Descriptor counts stayed at
4 before and after 192 opened reads across success, empty-file, and read-error
returns. Three introduced failure cases were observed failing before their
implementation and passing after it. The remaining boundary checks were retained
without manufacturing a failing run.

The agent's review retained a consuming map extraction API, member suffixes, and
an exhaustive switch for a closed enum. It correctly distinguished a scoped
loop index, a legal trailing member underscore, and a reserved global leading
underscore. This exercises the guidance added for the baseline source gaps.

An independent reviewer read all 48 adapted references and compared their
principles and provenance with upstream. The one substantive finding was a
missing explanation of the operation-extension half of data/object asymmetry;
that tradeoff was restored. No C++ correctness or execution-safety blocker was
identified.

The directory read-error fixture and `/dev/fd` resource check passed on the stated
host and need adaptation on platforms without those facilities. No sanitizer or
compiler/platform matrix was run. These are local smoke checks, not evidence of
effectiveness across other models, projects, or production workloads.
