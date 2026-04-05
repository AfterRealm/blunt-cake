# Changelog

## v1.2.0 — 2026-04-05

> *Four modes. Because one way to judge your code was never enough.*

### Eval Mode (Professional Grade)
- Serious code analysis with scored assertions — no jokes until the final verdict
- Generates 8-12 testable assertions per file across 5 categories: Correctness, Security, Reliability, Performance, Maintainability
- Each assertion graded PASS/FAIL with specific evidence (line numbers, code quotes)
- 5 quality dimension scores (1-5) with one-line justifications
- Letter grade (A-F) with pass rate and overall score
- Critical findings get detailed fixes in serious tone
- Final verdict delivered with roast energy — the payoff

### Interactive Mode Selection
- Skill now asks which mode on trigger: Standard 🔥 / Panel 👨‍🍳 / Skill Roast 🎯 / Eval 📊
- Skips the question if user already specified mode in their trigger
- Clear descriptions for each mode so users know what they're getting

### Self-Roast Fixes (from running Skill Roast on ourselves)
- Trigger priority order formalized (Skill → Panel → Standard → Eval)
- Panel agent prompts expanded from one-liners to full specs with severity scales, JSON schemas, and line number requirements
- Edge case handling added (trivially simple code gets a short roast, not manufactured issues)
- Skill Roast output format fully specified (was inheriting code format)
- Rules section moved to top of SKILL.md (behavioral constraints read first)

---

## v1.1.0 — 2026-04-05

> *One mode wasn't enough. Now there are three.*

### Panel Roast (Multi-Agent)
- 4 specialist agents in parallel — Security Auditor, Performance Analyst, Architecture Critic, Style Judge
- Head Chef coordinator merges, deduplicates, and cross-confirms findings
- Panel Notes table shows which agent found what and where they agreed

### Skill Roast (Meta-Review)
- Review SKILL.md files instead of code — roast the skill design itself
- 8 review categories: Trigger, Instructions, Edge Cases, Output Format, Process, Rules, Creativity, Eval-Readiness
- Separate Skill Roast Scale (Napkin Sketch → Draft → Almost There → Production-Grade)

### Self-Improving Eval Loop
- `self_improve.py` — automated improvement cycle: eval → analyze failures → propose SKILL.md changes → re-eval
- Opus analyzes failed assertions and generates generalized fixes
- SKILL.md backup saved before each modification
- Multi-cycle support: `--cycles 3`, stops early on perfect score

---

## v1.0.0 — 2026-04-05

> *Your code had it coming.*

### The Skill
- Full code review engine with 6 review categories: Bugs, Security, Performance, Style Crimes, Dead Code, Architecture
- Every finding includes a roast, a real explanation, severity rating, AND a concrete fix
- Roast Scale scoring (0-10): Health Violation → Dumpster Fire → Rare → Medium → Well Done → Chef's Kiss
- Structured output: Verdict, Findings, Scoreboard, Final Words

### The Eval
- 3 hand-crafted test files (security nightmare, decent code, spaghetti monster)
- Automated eval runner with Opus as judge
- 28 assertions across test cases
- First run: 93% pass rate, 5/5 humor, 5/5 actionability
- Self-improved to 100% in 4 iterations
