# gai-project-template

## Problem

What problem this solves, and for whom.

## Design

How it works: main components and how data moves through them.

## Trade-offs

What was chosen over what, and why.

## Results

Measured outcomes. Eval results go here once `evals/` is populated in Phase 2.

## How to run

```bash
cp .env.example .env      # fill in real values
uv sync                   # install dependencies
uv run python -m app.main # run the app
uv run ruff check .       # lint
uv run ruff format --check .
uv run pytest             # tests
```
