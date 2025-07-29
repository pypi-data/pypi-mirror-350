# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands
- Setup environment: `uv venv && source .venv/bin/activate && uv sync --all-groups`
- Build: `hatch build`
- Run tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function_name`
- Skip integration tests: `pytest -m "not integration"` (default)
- Run only asyncio tests: `pytest -m asyncio`
- Never perform git add. I manage git manually.

## Code Style Guidelines
- Python 3.11+ with strict type annotations
- Imports: standard library first, third-party second, local modules third
- Error handling: Use structured hierarchy with `TaskError` base class
- Async patterns: Proper cancellation handling with try/finally and asyncio.timeout
- Naming: CamelCase for classes, snake_case for functions/methods, UPPER_SNAKE_CASE for constants
- Documentation: Docstrings with type annotations in code
- Testing: Use pytest fixtures with proper async teardown
- Clean code: maintain proper resource cleanup in all async contexts