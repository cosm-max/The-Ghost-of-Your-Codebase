# The Ghost of Your Codebase

A haunted code reviewer for Python. Paste code; a ghost developer points out what is haunting it.
Built for The Turing Club Tech Team Auditions 2026 (Halloween edition).

## Run
    pip install -r requirements.txt
    python app.py          # open http://127.0.0.1:5000
    python -m unittest     # run the tests

## Architecture
    analyzer/rules.py   AST rules, each yields Findings (the core logic)
    analyzer/engine.py  runs all rules, computes the haunting score
    ghost/voice.py      turns findings into in-character messages (presentation only)
    app.py              Flask API: POST /api/review {code} -> score, verdict, findings
    static/index.html   frontend that marks haunted lines and shows the ghost's notes

Flow: code -> ast.parse -> rules -> findings -> score + ghost voice -> JSON -> UI.

## Add a rule
Write a function in `analyzer/rules.py`, decorate it with `@rule`, add its messages to
`ghost/voice.py`, and add a test.

## Known limitations
- Python only; rules are heuristics, so false positives are possible
  (e.g. an `elif` chain counts as nesting).
- Unused-variable check ignores loop variables and tuple unpacking on purpose.
- No auth or rate limiting; input is capped at 20,000 characters.
