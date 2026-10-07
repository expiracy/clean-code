#!/usr/bin/env python3
"""Check package links and compile its C++17 examples without dependencies."""

from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / 'skills/clean-code-cpp'
FLAGS = ['-std=c++17', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
RULE_PREFIX = re.compile(r'^(name|func|cmt|fmt|err|obj|bound|class|test|emerge)-')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--application-smoke', action='store_true',
                        help='also run the macOS/Unix exception-disabled file test')
    options = parser.parse_args()
    errors = []
    entry = (SKILL / 'SKILL.md').read_text()
    metadata = json.loads((SKILL / 'metadata.json').read_text())
    if metadata.get('name') != 'clean-code-cpp' or metadata.get('rule_count') != 48:
        errors.append('Unexpected skill name or upstream rule count in metadata')
    if not re.search(r'^name: clean-code-cpp$', entry, re.M):
        errors.append('Missing matching SKILL.md name')
    if not re.search(r'^description: Use when .{20,1024}$', entry, re.M):
        errors.append('Missing useful skill discovery description')

    rules = sorted(p for p in (SKILL / 'references').glob('*.md')
                   if RULE_PREFIX.match(p.name))
    indexed = set(re.findall(r'\]\(references/([^()]+\.md)\)', entry))
    if len(rules) != 48 or {p.name for p in rules} - indexed:
        errors.append('The skill must contain and index all 48 upstream rule topics')
    if not (SKILL / 'LICENSE').is_file():
        errors.append('Missing redistributable upstream licence')

    examples = []
    for document in sorted(SKILL.rglob('*.md')):
        content = document.read_text()
        for target in re.findall(r'\]\(([^)\s]+)\)', content):
            if re.match(r'^[a-z][a-z0-9+.-]*:', target) or target.startswith('#'):
                continue
            local = target.split('#', 1)[0]
            if not (document.parent / local).is_file():
                errors.append(f'{document.relative_to(REPO)}: broken link {target}')
        for match in re.finditer(r'^```([^\n]*)\n(.*?)^```\s*$', content,
                                 re.M | re.S):
            language, code = match.groups()
            if language.strip() != 'cpp':
                errors.append(f'{document.relative_to(REPO)}: non-C++ example {language}')
                continue
            # Each block is a separate translation unit. Only explicitly correct
            # self-checking programs execute; incorrect examples never execute.
            labels = re.findall(r'\*\*(Incorrect|Correct)[^\n]*',
                                content[:match.start()])
            runnable = (labels and labels[-1] == 'Correct'
                        and re.search(r'\bint\s+main\s*\(', code) is not None)
            line = content[:match.start()].count('\n') + 1
            examples.append((document, line, code, bool(runnable)))

    if not examples:
        errors.append('No documented C++ examples found')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1

    compiler = shlex.split(os.environ.get('CXX', 'clang++'))
    with tempfile.TemporaryDirectory(prefix='clean-code-cpp-check-') as directory:
        scratch = Path(directory)

        def check(item):
            index, (document, line, code, runnable) = item
            source = scratch / f'example-{index}.cpp'
            source.write_text(code)
            syntax = subprocess.run(compiler + FLAGS + ['-fsyntax-only', str(source)],
                                    capture_output=True, text=True, timeout=60)
            context = f'{document.relative_to(REPO)}:{line}'
            if syntax.returncode:
                return f'{context}\n{syntax.stderr}', 0
            if runnable:
                binary = scratch / f'example-{index}'
                build = subprocess.run(compiler + FLAGS + ['-DNDEBUG', str(source),
                                       '-o', str(binary)], capture_output=True,
                                       text=True, timeout=60)
                if build.returncode:
                    return f'{context}\n{build.stderr}', 0
                run = subprocess.run([str(binary)], cwd=scratch, capture_output=True,
                                     text=True, timeout=10)
                if run.returncode:
                    return f'{context}: runtime exit {run.returncode}\n{run.stderr}', 0
                return None, 1
            return None, 0

        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(check, enumerate(examples)))

    failures = [failure for failure, _ in results if failure]
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'PASS: 48 indexed rules; local links and metadata; '
          f'{len(examples)} C++17 examples compiled; '
          f'{sum(count for _, count in results)} correct self-checks executed with NDEBUG')
    if options.application_smoke:
        if not Path('/dev/fd').is_dir():
            parser.error('the application smoke test requires /dev/fd and a Unix read-error fixture')
        sources = REPO / 'tests/application-smoke'
        with tempfile.TemporaryDirectory(prefix='clean-code-cpp-smoke-') as directory:
            binary = Path(directory) / 'smoke'
            subprocess.run(compiler + FLAGS + ['-fno-exceptions', '-DNDEBUG',
                           str(sources / 'first_byte.cpp'),
                           str(sources / 'test_first_byte.cpp'), '-o', str(binary)],
                           check=True, timeout=60)
            subprocess.run([str(binary)], cwd=directory, check=True, timeout=10)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
