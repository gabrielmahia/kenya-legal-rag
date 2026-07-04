"""Smoke tests — AST parse gate."""
import ast
import pathlib


def test_all_sources_parse():
    root = pathlib.Path(__file__).parent.parent
    errors = []
    for f in root.rglob("*.py"):
        if ".venv" in str(f) or "node_modules" in str(f):
            continue
        try:
            ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError as e:
            errors.append(f"{f}: {e}")
    assert not errors, "\n".join(errors)
