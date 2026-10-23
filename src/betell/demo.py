"""Toy repositories with known behavioral ground truth.

Each scenario is a base tree and a head tree. ``build`` turns one into a git
repository with two commits tagged ``base`` and ``head``.
"""
import subprocess
import textwrap
from pathlib import Path

TESTS = textwrap.dedent('''
    from shop.api import checkout, describe, safe_parse

    def test_checkout_small():
        assert checkout([1, 2]) == 3

    def test_checkout_bulk():
        assert checkout([10] * 12) >= 100

    def test_describe():
        assert describe("  Apple ").startswith("item")

    def test_parse():
        assert safe_parse("12") == 12
        assert safe_parse("x") is None
''')

BASE = {
    "shop/__init__.py": "",
    "shop/util.py": textwrap.dedent('''
        def normalize(name):
            return name.strip()

        def discount(total):
            if total > 100:
                return total * 0.9
            return total

        def parse(text):
            return int(text)
    '''),
    "shop/api.py": textwrap.dedent('''
        from shop.util import normalize, discount, parse

        def checkout(prices):
            total = sum(prices)
            return discount(total)

        def describe(name):
            label = normalize(name)
            if label.islower():
                return "item " + label
            return "item " + label.lower()

        def safe_parse(text):
            try:
                return parse(text)
            except ValueError:
                return None
    '''),
    "tests/test_shop.py": TESTS,
}


def variant(**edits):
    tree = dict(BASE)
    for path, (old, new) in edits.items():
        assert old in tree[path], (path, old)
        tree[path] = tree[path].replace(old, new)
    return tree


SCENARIOS = {
    # A pure refactoring: no behavior changes at all.
    "refactor": variant(**{"shop/util.py": ("    if total > 100:\n        return total * 0.9\n    return total",
                                            "    rate = 0.9 if total > 100 else 1\n    return total * rate if rate != 1 else total")}),
    # Editing a helper changes what an untouched caller returns and which branch it takes.
    "helper": variant(**{"shop/util.py": ("return name.strip()", "return name.strip().lower()")}),
    # The bulk discount threshold moves, so an untouched caller returns a different value.
    "threshold": variant(**{"shop/util.py": ("if total > 100:", "if total > 150:")}),
    # The parser stops raising, so the untouched caller no longer handles an exception.
    "exception": variant(**{"shop/util.py": ("return int(text)",
                                             "return int(text) if text.isdigit() else None")}),
    # Lines shift and an unused function appears. No behavior changes.
    "shift": variant(**{"shop/util.py": ("def normalize(name):", "# Helpers.\n# More text.\n\ndef unused():\n    return 1\n\n\ndef normalize(name):"),
                        "shop/api.py": ("def describe(name):", "def helper():\n    return 0\n\n\ndef describe(name):")}),
    # A behavior change that flips a test outcome.
    "outcome": variant(**{"shop/util.py": ("return total * 0.9", "return total * 0.5")}),
}

NONDETERMINISTIC = {
    "shop/clock.py": textwrap.dedent('''
        import random
        import time

        def stamp():
            return time.time()

        def token():
            return random.random()

        class Box(object):
            pass

        def boxed():
            return [Box(), object()]
    '''),
    "tests/test_clock.py": textwrap.dedent('''
        from shop.clock import stamp, token, boxed

        def test_stamp():
            assert stamp() > 0
            assert token() >= 0
            assert len(boxed()) == 2
    '''),
}


def build(directory, base, head):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    def run(*args):
        subprocess.run(["git", *args], cwd=directory, check=True, capture_output=True)

    def write(tree):
        for path, text in tree.items():
            target = directory / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)

    run("init", "-q", "-b", "main")
    run("config", "user.email", "demo@example.org")
    run("config", "user.name", "demo")
    write(base)
    run("add", "-A")
    run("commit", "-q", "-m", "base")
    run("tag", "base")
    write(head)
    run("add", "-A")
    run("commit", "-q", "--allow-empty", "-m", "head")
    run("tag", "head")
    return directory


def main(scenario="helper", directory=None):
    """Build a toy repository for ``scenario`` and print betell's report for it."""
    import tempfile

    from betell.cli import main as cli

    head = SCENARIOS[scenario]
    root = Path(directory or tempfile.mkdtemp(prefix="betell-demo-")) / scenario
    build(root, BASE, head)
    print("Toy repository with tags base and head: %s\n" % root, flush=True)
    subprocess.run(["git", "--no-pager", "-C", str(root), "diff", "base", "head", "--", "shop"], check=False)
    print(flush=True)
    cli(["run", "--repo", str(root), "--base", "base", "--head", "head"])
