# System Design Interviewer

An agent skill that turns your AI coding agent into a **strict, realistic FAANG-style system design interviewer**. It runs a timed 45-minute mock interview, can watch your live Excalidraw board, keeps track of your weak spots across sessions, and grades you honestly.

> It interviews. It does not teach during the interview. No hints, no solutions, no lists of options to pick from. You do 100% of the design work, and the teaching happens in the debrief afterward.

## Features

- **Realistic pacing**: a real 45-minute clock with a phase/time badge on every turn and a hard stop at T = 40.
- **Interviewer discipline**: Flip-Back rule, one question per turn, consequence-only probing, no technology name-dropping, no made-up pop quizzes.
- **Silent guardrails**: scoping before boxes, no single points of failure, every technology justified, read and write paths connected end-to-end. These are graded, never announced.
- **Uninflated scorecard**: Strong Hire → No Hire with an E4/E5/E6 leveling signal, five scored dimensions, and a list of every intervention used.
- **Live whiteboard** *(optional)*: headless snapshots of a shared Excalidraw room, so the interviewer reacts to what you actually drew.
- **Persistent progress**: a local candidate profile tracks your skill radar, recurring mistakes, and session history, with archived board snapshots.
- **Weak-point mode**: "Interview me on my weak points" picks a topic aimed at your lowest-rated dimensions.
- **Topic rotation**: seven system design archetypes, and never the same archetype twice in a row.

## Install

Clone into your agent's skills directory. Examples:

```bash
# Antigravity / generic agents
git clone https://github.com/AbdullahMadoun/SystemDesignInterviewer ~/.agents/skills/system-design-interviewer

# Claude Code
git clone https://github.com/AbdullahMadoun/SystemDesignInterviewer ~/.claude/skills/system-design-interviewer
```

The folder name should match the skill name: `system-design-interviewer`.

### Optional: live Excalidraw support

```bash
cd <skill-dir>
pip install -r requirements.txt
python3 -m playwright install chromium
```

Chat-only interviews work without this.

## Usage

Ask your agent:

- *"Give me a system design mock interview."*
- *"Interview me on my weak points."*
- *"Let's do a system design interview. Here's my board: https://excalidraw.com/#room=…"*

To use a board, open [excalidraw.com](https://excalidraw.com), click **Share → Live collaboration → Start session**, and paste the link.

## Repository layout

```
.
├── SKILL.md                      # Skill entrypoint: interviewer behavior and lifecycle
├── references/
│   ├── rubric.md                 # Leveling, grade calibration, scorecard template
│   ├── estimation.md             # Constants for checking the candidate's math
│   └── topics.md                 # Archetype matrix, topic bank, weak-point mapping
├── templates/
│   └── candidate_profile.md      # Blank profile, copied on first run
├── scripts/
│   ├── snap_board.py             # Snapshot a live Excalidraw room
│   ├── write_board.py            # Post a text card onto a live Excalidraw room
│   └── check_repo.py             # Repo hygiene checks (run in CI)
└── requirements.txt
```

## Your data stays local

On first run the skill creates two files next to `SKILL.md`:

| Path | Contents |
| :--- | :--- |
| `candidate_profile.md` | Your skill radar, mistakes, study plan, session log |
| `history/` | Your archived final-board snapshots |

Both are **gitignored**, so `git pull` updates the skill without touching your progress, and they can't be committed by accident. Room URLs (which contain the board's encryption key) are never written to disk by the skill.

## Contributing

PRs are welcome. Before pushing, run:

```bash
python3 scripts/check_repo.py
```

It blocks personal data, absolute user paths, Excalidraw room keys, CRLF line endings, broken `SKILL.md` references, and invalid frontmatter.

## Disclaimer

The interview structure is inspired by publicly available material such as the [Hello Interview](https://www.hellointerview.com) delivery framework. This project is not affiliated with or endorsed by Hello Interview, Excalidraw, or any company named in the topic bank. Grades are practice signals, not predictions of real interview outcomes.

## License

[MIT](LICENSE)
