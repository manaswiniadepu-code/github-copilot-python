# Copilot Instructions

## Project
Flask Sudoku app refactored from legacy code. Features: difficulty levels, timer,
hints, check button, top 10 scoreboard (localStorage), dark mode.

## Code style
- Python 3.10+, type hints, PEP 8, docstrings on all functions
- Split logic into small modules (puzzle generation, solver, validation, routes)
- Consistent error handling, with clear comments where logic is non-obvious

## Frontend
- Plain CSS, responsive (mobile + desktop), light and dark mode
- Alternating colors for 3x3 boxes, readable text and controls

## Testing
- Use pytest; run tests after every change
- Do not break existing behavior when refactoring

## Rules
- Keep changes small and focused; explain what changed
- Puzzles must always have exactly one unique solution