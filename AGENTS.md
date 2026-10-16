# Instructions for AI agents

- Language: Python 3.12+, managed with `uv`.
- Install: `uv sync`
- **Test command: `uv run pytest -q`** — must pass before a change is done.
- Code lives in `src/expenses/`, tests in `tests/`.
- Every bug fix or feature must include tests that cover it.
- Keep changes small and focused on the issue. Don't reformat unrelated code.
- Use `Decimal` for money, never float.
- Branch name: `agent/<issue-number>-<short-slug>`. Never push to `main`.
