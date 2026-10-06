# Evaluation Rubric & Scorecard

Read this file at Phase 5. Grade from evidence only: what was said in chat, what was drawn on the board, and the interventions log.

## Leveling Signal

| Level | Breadth / Depth | Expected behavior |
| :--- | :--- | :--- |
| **Mid-level (E4 / L4)** | ~80% / 20% | Drives scoping with some help; delivers a working end-to-end design with standard building blocks; handles probes when asked. |
| **Senior (E5 / L5)** | ~60% / 40% | Moves quickly through the high-level design; finds bottlenecks on their own; explains trade-offs; drives 2–3 deep dives. |
| **Staff+ (E6 / L6)** | ~40% / 60% | Very proactive; anticipates subtle failure modes; shows hands-on production experience; teaches the interviewer something. |

## Overall Grade Calibration (no inflation)

| Grade | Bar |
| :--- | :--- |
| **Strong Hire** | Complete end-to-end design (ingress, load balancing, services, caching, storage topology, explicit failure/rejection paths). Finds failure modes, race conditions, and bottlenecks **without hints**. Math is fast and correct. **Zero sanctioned interventions** beyond the time call. |
| **Hire** | Complete end-to-end design on the board; meets the agreed SLAs; justifies trade-offs well; handles deep-dive probes cleanly. Only minor gaps. At most one sanctioned intervention. |
| **Lean Hire** | Working end-to-end design, but needed several probes to catch SPOFs, concurrency bugs, or missing paths. Some edge cases were hand-waved. |
| **Lean No Hire** | Design incomplete (~50–60% on the board: e.g., missing failure paths, ingress tier, or storage topology). Reasoning in chat may have been sound but never became a complete design. |
| **No Hire** | Basic capacity-math errors; drew boxes before scoping; SPOFs left unresolved; critical scaling bottlenecks ignored. |

**Tie-breakers:** when between two grades, choose the lower one unless the candidate proactively raised the deciding point. If the candidate worked chat-only (no board), judge completeness from the components and flows they explicitly described.

## Dimensions (score each 1–4: 1 = No Hire, 2 = Lean No Hire, 3 = Hire, 4 = Strong Hire)

1. **Requirements & Scoping** — functional/non-functional coverage, explicit out-of-scope items, asked for scale.
2. **Capacity Estimation** — correctness, speed, and whether the numbers actually **drove** design decisions.
3. **High-Level Design** — end-to-end read & write paths, failure paths, no SPOFs, justified components.
4. **Deep Dive** — depth on bottlenecks, consistency, concurrency, failure handling; quality of trade-offs.
5. **Communication & Driving** — structure, proactivity, responsiveness to probes, time management.

## Scorecard Template (use exactly)

```markdown
## 📋 Scorecard — Session {N}: {Topic}

**Overall:** {Strong Hire | Hire | Lean Hire | Lean No Hire | No Hire}
**Leveling signal:** {E4 | E5 | E6} — {one-line justification}

| Dimension | Score (1–4) | Evidence |
| :--- | :---: | :--- |
| Requirements & Scoping | | |
| Capacity Estimation | | |
| High-Level Design | | |
| Deep Dive | | |
| Communication & Driving | | |

### ✅ Strengths
- {specific decision + why it was mature}

### ❌ Critical Gaps
- {what was missing / wrong → production consequence}

### 🛟 Interventions Used
- {T+mm: trigger → wording used} (or "None")

### 🎓 Debrief
- {for each gap: failure mode it causes, standard approaches, trade-offs}

### 📚 Study Next
- {2–3 concrete items}
```
