# Changelog

## v1.1.0 — 2026-04-05

> *One mode wasn't enough. Now there are three.*

### Panel Roast (Multi-Agent)
- **4 specialist agents in parallel** — Security Auditor, Performance Analyst, Architecture Critic, Style Judge
- Head Chef coordinator merges, deduplicates, and cross-confirms findings
- Panel Notes table shows which agent found what and where they agreed
- Issues caught by multiple agents independently get flagged as high-confidence

### Skill Roast (Meta-Review)
- Review SKILL.md files instead of code — roast the skill design itself
- 8 review categories: Trigger clarity, instruction specificity, edge cases, output format, process flow, rule consistency, unique value, eval-readiness
- Separate Skill Roast Scale (Napkin Sketch → Draft → Almost There → Production-Grade)

### Self-Improving Eval Loop
- `self_improve.py` — automated improvement cycle: eval → analyze failures → propose SKILL.md changes → re-eval
- Opus analyzes failed assertions and generates generalized fixes (not narrow patches)
- SKILL.md backup saved before each modification
- Iteration tracking with improvement logs
- Multi-cycle support: `--cycles 3` runs 3 improvement rounds, stops early on perfect score

---

## v1.0.0 — 2026-04-05

> *Your code had it coming.*

### The Skill
- Full code review engine with 6 review categories: Bugs, Security, Performance, Style Crimes, Dead Code, Architecture
- Every finding includes a roast, a real explanation, severity rating, AND a concrete fix
- Roast Scale scoring system (0-10): Health Violation → Dumpster Fire → Rare → Medium → Well Done → Chef's Kiss
- Structured output format: Verdict, Findings, Scoreboard, Final Words
- Rules: roast the code not the coder, every roast backed by a real finding, celebrate what's done right

### The Eval
- 3 hand-crafted test files covering the full spectrum
- Automated eval runner with Opus as judge
- 28 total assertions across test cases
- Iteration tracking + markdown report output

### First Eval Results
- **93% assertion pass rate**
- **Accuracy: 4.7/5** — catches real issues
- **Humor: 5.0/5** — actually funny
- **Actionability: 5.0/5** — every finding has a fix
- **Format compliance: 5.0/5** — follows the template
