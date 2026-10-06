# Changelog

## 1.0.0 — 2026-10-06

First public release.

- Interviewer behavior: MUST/NEVER rules, sanctioned interventions, good vs. bad examples.
- Real-clock time discipline with a single lifecycle/budget table.
- References split out for on-demand loading: rubric, estimation constants, topic bank.
- Seven-archetype rotation with explicit selection precedence (anti-repetition beats weak-point mode).
- Hardened Excalidraw scripts: input validation, readiness waits, timeouts, clean exit codes, room keys never logged; text writing switched to paste events for headless reliability.
- Personal state (profile, board history) is gitignored and bootstrapped from a template.
- `scripts/check_repo.py` + GitHub Actions hygiene checks.
