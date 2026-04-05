# 🍰 Blunt Cake

A Claude Code agent skill that serves your code review straight — no frosting, no sugarcoating. Every finding is real, every roast is earned, and every issue comes with a fix.

Brutal honesty. Comedic delivery. Actual solutions.

## Install

```bash
claude plugin add AfterRealm/blunt-cake
```

Or manually: copy this repo to `~/.claude/plugins/blunt-cake/`

## Four Modes

When triggered, the skill asks which mode you want:

```
🍰 Blunt Cake — Pick your serving:

1. Standard Roast 🔥 — Quick single-pass review
2. Panel Roast 👨‍🍳 — 4 specialist agents in parallel
3. Skill Roast 🎯 — Review a SKILL.md design
4. Eval Mode 📊 — Serious analysis with scored assertions
```

### 🔥 Standard Roast
Single-pass review. Fast, funny, thorough. Every finding gets a roast line, a real explanation, and a fix.

### 👨‍🍳 Panel Roast (Multi-Agent)
Spawns 4 specialist agents in parallel:
- **🔓 Security Auditor** — injection, auth gaps, exposed secrets
- **🐌 Performance Analyst** — O(n²), memory leaks, missing indexes
- **🏗️ Architecture Critic** — coupling, god objects, wrong abstractions
- **🤡 Style Judge** — naming crimes, dead code, hidden bugs

A Head Chef coordinator merges findings, deduplicates, and flags cross-confirmed issues (caught by multiple agents independently = high confidence). Panel Notes table shows which agent found what.

### 🎯 Skill Roast (Meta-Review)
Feed it a SKILL.md and it roasts the skill design. 8 review categories: trigger clarity, instruction specificity, edge cases, output format, process flow, rule consistency, unique value, and eval-readiness.

| Score | Rating |
|:---:|---|
| 10 | 🏆 Production-grade — ship it |
| 7-9 | 📦 Almost there — needs polish |
| 4-6 | 📝 Draft — idea is good, spec needs work |
| 1-3 | 🗒️ Napkin sketch — you wrote a wish, not a skill |

### 📊 Eval Mode (Professional Grade)
Serious code analysis. No jokes until the end.

- Generates 8-12 testable assertions per file
- Grades each PASS/FAIL with specific evidence (line numbers, code quotes)
- Scores 5 quality dimensions: Correctness, Security, Reliability, Performance, Maintainability
- Letter grade (A-F) with pass rate and overall score
- Critical findings get detailed fixes
- Final verdict delivered with roast energy

```
📊 CODE EVAL — auth.js

Assertions: 9/12 passed (75%)
Overall: 3.2/5

Grade: C — "You validated the password and forgot everything else.
Like acing the quiz and failing the final."
```

## Code Review Categories

| Category | What It Catches |
|----------|----------------|
| 🔥 Bugs | Logic errors, off-by-ones, null derefs, race conditions |
| 🔓 Security | Injection, exposed secrets, missing validation, auth gaps |
| 🐌 Performance | O(n²) disasters, memory leaks, unnecessary work |
| 🤡 Style Crimes | God functions, lying variable names, callback hell |
| 💀 Dead Code | Unreachable branches, TODO archaeology, zombie imports |
| 🏗️ Architecture | Wrong abstractions, circular deps, misplaced logic |

## The Roast Scale (Standard & Panel)

| Score | Rating | Meaning |
|:---:|---|---|
| 10 | 👨‍🍳 Chef's Kiss | I came to roast and left humbled |
| 8-9 | 🔥 Well Done | Solid. Minor nitpicks at best |
| 6-7 | 🍳 Medium | Edible but needs seasoning |
| 4-5 | 🥩 Rare | Undercooked. Served too early |
| 2-3 | 🗑️ Dumpster Fire | I've seen better code in a CAPTCHA |
| 0-1 | ☠️ Health Violation | Ship this and someone's going to the hospital |

## Self-Improving Eval Framework

This skill ships with a self-improvement loop for developer QA:

```bash
# Run the eval (5 test cases across all modes)
python evals/run_eval.py --markdown

# Self-improvement cycle (eval → analyze failures → update SKILL.md)
python evals/self_improve.py

# Multi-cycle convergence
python evals/self_improve.py --cycles 3
```

### How It Works
1. Eval runner tests the skill against hand-crafted test files with specific assertions
2. Self-improver reads failures, sends them + SKILL.md to Opus for targeted fixes
3. Opus proposes generalized improvements (not narrow patches)
4. New eval verifies improvement. Repeat until convergence.

### Results
```
Iteration 1: 93% pass rate — initial skill
Iteration 2: 63% — variance, but self-improver found "missing security" gap
Iteration 3: 87% — improvement applied, climbing
Iteration 4: 100% — converged. 5/5 humor, 5/5 actionability.
```

The skill improved itself to a perfect score in 4 iterations.

## Philosophy

1. **Every roast is backed by a real finding.** No fake issues for comedy.
2. **Roast the code, not the coder.** Never attack intelligence or experience.
3. **Always include the fix.** A roast without a solution is just bullying.
4. **Celebrate the good stuff.** The best roasts acknowledge skill before burning the mistakes.
5. **Eval Mode is serious.** Professional assertions with real metrics. Comedy only in the final verdict.
6. **The skill improves itself.** Failed evals drive targeted improvements. Ship, measure, iterate.

## License

MIT

## Author

Built by [AfterRealm](https://github.com/AfterRealm) with Claude Code.
