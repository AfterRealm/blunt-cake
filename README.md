# 🍰 Blunt Cake

A Claude Code agent skill that serves your code review straight — no frosting, no sugarcoating. Every finding is real, every roast is earned, and every issue comes with a fix.

Brutal honesty. Comedic delivery. Actual solutions.

## Install

**Option 1: Via AfterRealm marketplace** (recommended)
```bash
claude plugin marketplace add AfterRealm/marketplace
claude plugin install blunt-cake@afterrealm
```

**Option 2: Copy to skills directory**
```bash
mkdir -p ~/.claude/skills/blunt-cake
curl -o ~/.claude/skills/blunt-cake/SKILL.md https://raw.githubusercontent.com/AfterRealm/blunt-cake/master/SKILL.md
```

**Option 3: Clone the repo** (includes evals, test files, and GitHub Action)
```bash
git clone https://github.com/AfterRealm/blunt-cake.git ~/.claude/skills/blunt-cake
```

After install, run `/skills` in Claude Code to verify it appears, then trigger it with "roast my code" or similar.

> Also available: [Father Time](https://github.com/AfterRealm/father-time) — session-aware time management for Claude Code. Both plugins live in the [AfterRealm marketplace](https://github.com/AfterRealm/marketplace).

## Eight Modes

When triggered, the skill asks which mode you want — plus a personality:

```
🍰 Blunt Cake — Pick your serving:

1. Standard Roast 🔥 — Quick single-pass review
2. Panel Roast 👨‍🍳 — 4 specialist agents in parallel
3. Skill Roast 🎯 — Review a SKILL.md design
4. Eval Mode 📊 — Serious analysis with scored assertions
5. Diff Roast 📝 — Roast a git diff
6. Batter Battle 🆚 — Two files enter, one leaves
7. Roast-a-thon 🏫 — Roast an entire project directory
8. Roast Challenge 🎯🔥 — Coding challenge judged by Blunt Cake

Pick a personality: 🧑‍🍳 Chef · 👵 Grandma · 😐 PR Reviewer · 🎤 Simon Cowell · 🐕 Snoop Dogg · 🏴‍☠️ Pirate · 🎨 Custom (create your own!)
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

### 📝 Diff Roast (NEW)
Roast your git diff before you commit. Targets only what changed — won't blame you for pre-existing sins (unless you made them worse).

- Reviews unstaged, staged, branch diffs, or specific commits
- Reads full file context around changes for accurate assessment
- Scores the DIFF, not the whole file

```
📝 DIFF ROAST — staged changes

3 files changed, 47 additions, 12 deletions
Score: 6/10 — 🥪 Mid Sandwich

"You fixed the auth bug and introduced two new ones.
That's not a net positive, that's a lateral move."
```

### 🆚 Batter Battle (NEW)
Two implementations enter. One leaves. Side-by-side comparison across all review categories with a declared winner.

- 5 rounds: Bugs, Security, Performance, Style, Architecture
- Per-round winners with specific reasoning
- No ties allowed — someone's getting sent home
- Winner still gets roasted for their flaws
- Loser gets actionable advice stolen from the winner

```
🆚 BATTER BATTLE — auth_v1.js vs auth_v2.js

Round 1 (Bugs): auth_v2 ✓
Round 2 (Security): auth_v2 ✓
Round 3 (Performance): auth_v1 ✓
Round 4 (Style): auth_v2 ✓
Round 5 (Architecture): auth_v2 ✓

🏆 WINNER: auth_v2 (4-1)
"v2 won by a landslide, but that memory leak in round 3
means you're celebrating with a slow clap."
```

## 🧑‍🍳 Language Packs (NEW)

Pick a personality for your roast. Same findings, different delivery:

| Personality | Vibe |
|-------------|------|
| 🧑‍🍳 **Chef** (default) | Celebrity chef who found raw chicken in the walk-in |
| 👵 **Disappointed Grandma** | Not mad, just disappointed. Guilt-trip delivery. |
| 😐 **Passive-Aggressive PR Reviewer** | "Interesting choice 🙂" — corporate hostility in polite wrapping |
| 🎤 **Simon Cowell** | Withering. Dramatic pauses. Grudging "you've got potential." |
| 🐕 **Snoop Dogg** | Chill but devastating. Drops wisdom casually. |
| 🏴‍☠️ **Pirate** | Nautical metaphors. Your secrets are "flying a flag sayin' ROB ME BLIND." |

## 🔧 Auto-Fix (NEW)

After any code roast, Blunt Cake offers to apply the fixes it suggested:

```
🔧 Auto-Fix Available — 7 fixable issues found
- All — Apply all fixes
- Critical/High only — Just the important stuff
- Pick — I'll list them, you choose
- Nah — Just the roast, thanks
```

Fixes are applied one at a time, most severe first. After fixing, offers a re-roast to check your new score.

### 🏫 Roast-a-thon (NEW)
Roast an entire project directory, file by file, and get a project GPA.

- Scans all source files (or a custom glob/directory)
- Caps at 20 files per run — focused, not overwhelming
- Each file gets a score and one-line roast summary
- Identifies the Valedictorian (best file) and the Dropout (worst file)
- Finds project-wide patterns — habits that show up across multiple files
- GPA grading: A+ (Dean's List) to F- (Expelled)

```
🏫 ROAST-A-THON — my-api/

12 files reviewed
GPA: 5.8/10 — Grade: D — Below Average

🎓 Valedictorian: utils/validate.ts (9/10)
📎 Dropout: routes/auth.js (2/10)

Project-wide patterns:
  1. No input validation on 8/12 endpoints
  2. Console.log debugging in 5 files
  3. Zero error handling in database calls
```

## 📸 Shareable Roast Cards (NEW)

After any roast, type "card" to get a compact, styled summary designed for Discord, Slack, X/Twitter, or GitHub comments. Includes your score, worst finding, best praise, and a link back to Blunt Cake. Screenshot-ready.

```
┌──────────────────────────────────────┐
│  🍰 BLUNT CAKE — STANDARD ROAST     │
│  📁 auth.js                          │
│  📊 Score: 2/10 — 🗑️ Dumpster Fire   │
│  🔥 Findings: 7                      │
│  💀 "Your JWT secret is 'secret123'" │
│  🏆 "At least you used bcrypt"       │
│  roasted with 🍰 blunt-cake v2.2    │
└──────────────────────────────────────┘
```

## 🤖 CI/CD — GitHub Action (NEW)

Auto-roast every PR with a GitHub Action. Blunt Cake runs a Diff Roast on the PR changes and posts the result as a comment.

### Quick Setup
1. Copy `.github/workflows/blunt-cake-roast.yml` to your repo
2. Add `ANTHROPIC_API_KEY` as a repository secret
3. Open a PR and watch the roast appear

Configurable via env vars:
- `ROAST_MODE` — `diff` (default), `standard`, or `roast-a-thon`
- `ROAST_PERSONALITY` — any language pack name

The PR comment wraps the roast in a collapsible `<details>` block so it doesn't flood the conversation.

## 🏆 Hall of Fame (& Shame)

Community leaderboard! Submit your roast scores to `hall-of-fame/README.md`:

- **Hall of Shame** — lowest scores win. Wear it with pride.
- **Hall of Fame** — highest scores. Clean code heroes.
- **Hall of Improvement** — best before/after glow-ups.
- **Roast-a-thon Honor Roll** — bravest full-project GPAs.
- **Batter Battle Highlights** — best head-to-head matchups.

Submit via PR or [GitHub Discussions](../../discussions).

### 🎯🔥 Roast Challenge (NEW)
Coding katas judged by Blunt Cake. Pick a challenge, build your solution, get roasted. Beat the target score to pass.

5 built-in challenges:

| Challenge | Target | What You Build |
|-----------|:------:|---------------|
| **Auth Gauntlet** 🔒 | 8/10 | Secure auth module from scratch |
| **API Speedrun** ⚡ | 7/10 | REST API with full CRUD |
| **The Untangler** 🍝 | 7/10 | Refactor spaghetti into clean code |
| **Fort Knox** 🏦 | 9/10 | Patch every security hole |
| **Clean Room** 🧹 | 9/10 | Write the cleanest utility function |

Community challenges welcome — submit via PR to `challenges/community/`.

## 🎨 Custom Personality Creator (NEW)

Don't like the built-in personalities? Make your own. Pick "Custom" in the personality picker, describe a voice ("a disappointed TypeScript compiler", "Bob Ross looking at your code", "your mom"), and Blunt Cake generates the personality spec with sample roast lines. Preview it, tweak it, save it for reuse.

Saved custom personalities appear alongside the built-in packs on future roasts.

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
# Run the eval (9 test cases across all modes)
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
7. **Personality is the sauce, not the steak.** Language packs change delivery, never substance.
8. **Fix what you find.** Auto-Fix turns talk into action.
9. **Grade the whole project, not just files.** Roast-a-thon finds patterns individuals miss.
10. **Make it shareable.** If people can't screenshot it, it doesn't spread.

## License

MIT

## Author

Built by [AfterRealm](https://github.com/AfterRealm) with Claude Code.
