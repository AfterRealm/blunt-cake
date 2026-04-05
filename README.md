# 🔥 Roast My Code

A Claude Code agent skill that reviews your code with brutal honesty and comedic delivery. Every finding is real, every roast is earned, and every issue comes with a fix.

Think Gordon Ramsay doing code review.

## Install

```bash
claude plugin add AfterRealm/roast-my-code
```

Or manually: copy this repo to `~/.claude/plugins/roast-my-code/`

## Three Modes

### 🔥 Standard Roast
Single-pass review. Fast, funny, thorough.
```
/roast                    # roast the current file
roast my code             # same thing
roast this function       # scope to a specific function
```

### 👨‍🍳 Panel Roast (Multi-Agent)
Spawns 4 specialist agents in parallel — Security Auditor, Performance Analyst, Architecture Critic, and Style Judge — each reviewing from their lens simultaneously. A Head Chef coordinator merges findings, deduplicates, cross-confirms issues caught by multiple agents, and writes the final roast.

```
panel roast               # bring the whole panel
full roast                # same thing
roast this hard           # go deep
```

**Why it's better:** 4 focused specialists catch more than 1 generalist. Cross-confirmed findings (caught by multiple agents independently) are flagged with higher confidence. The Panel Notes table shows which agent found what.

### 🎯 Skill Roast (Meta-Review)
Feed it a SKILL.md and it roasts the skill design itself. Reviews trigger clarity, instruction specificity, edge case handling, output format, process flow, rule consistency, unique value, and eval-readiness.

```
roast my skill            # review a SKILL.md file
roast this skill          # same thing
```

**Skill Roast Scale:**
| Score | Rating |
|:---:|---|
| 10 | 🏆 Production-grade — ship it, I'd install this |
| 7-9 | 📦 Almost there — real value, needs polish |
| 4-6 | 📝 Draft — idea is good, spec needs work |
| 1-3 | 🗒️ Napkin sketch — you wrote a wish, not a skill |

## Review Categories (Code Mode)

| Category | What It Catches |
|----------|----------------|
| 🔥 Bugs | Logic errors, off-by-ones, null derefs, race conditions |
| 🔓 Security | Injection, exposed secrets, missing validation, auth gaps |
| 🐌 Performance | O(n²) disasters, memory leaks, unnecessary work |
| 🤡 Style Crimes | God functions, lying variable names, callback hell |
| 💀 Dead Code | Unreachable branches, TODO archaeology, zombie imports |
| 🏗️ Architecture | Wrong abstractions, circular deps, misplaced logic |

## The Roast Scale (Code)

| Score | Rating | Meaning |
|:---:|---|---|
| 10 | 👨‍🍳 Chef's Kiss | I came to roast and left humbled |
| 8-9 | 🔥 Well Done | Solid. Minor nitpicks at best |
| 6-7 | 🍳 Medium | Edible but needs seasoning |
| 4-5 | 🥩 Rare | Undercooked. Served too early |
| 2-3 | 🗑️ Dumpster Fire | I've seen better code in a CAPTCHA |
| 0-1 | ☠️ Health Violation | Ship this and someone's going to the hospital |

## Self-Improving Eval

This skill doesn't just ship with tests — it ships with a self-improvement loop. The eval runner tests the skill, identifies failed assertions, and an improvement engine proposes targeted changes to SKILL.md. Run it iteratively until the skill converges.

```bash
# Run the eval
python evals/run_eval.py --markdown

# Run one self-improvement cycle (eval → analyze failures → update SKILL.md)
python evals/self_improve.py

# Run 3 cycles (eval → improve → eval → improve → eval → improve)
python evals/self_improve.py --cycles 3
```

### How It Works
1. `run_eval.py` runs each test case with and without the skill, Opus judges assertions
2. `self_improve.py` reads failed assertions, sends them + current SKILL.md to Opus
3. Opus analyzes failures, proposes generalized fixes (not narrow patches), outputs updated SKILL.md
4. New eval run verifies the improvement. Repeat until convergence.
5. Every iteration is tracked in `evals/iteration-N/` with benchmarks and improvement logs

### First Eval Results
```
Assertion pass rate:  93%
Accuracy:             4.7/5
Humor:                5.0/5
Actionability:        5.0/5
Format compliance:    5.0/5
```

## Example Output

```
# 🔥 ROAST MY CODE — auth.js

## The Verdict
This authentication module is like a nightclub bouncer who checks IDs
but leaves the back door propped open with a brick. You validated the
JWT perfectly, then stored the session token in localStorage like it's
a grocery list.

Score: 4/10 — 🥩 Rare

### 🔓 SECURITY — Session tokens in localStorage
> You hashed the password with bcrypt but stored the session token where
> any XSS script can grab it. That's like locking your front door and
> leaving the key taped to the window.

What's wrong: localStorage is accessible to any JavaScript running
on the page. An XSS vulnerability anywhere in the app exposes all
session tokens.
Severity: CRITICAL
Fix: Use httpOnly cookies for session tokens.
```

## Philosophy

1. **Every roast is backed by a real finding.** No fake issues for comedy.
2. **Roast the code, not the coder.** Never attack intelligence or experience.
3. **Always include the fix.** A roast without a solution is just bullying.
4. **Celebrate the good stuff.** The best roasts acknowledge skill before burning the mistakes.
5. **The skill improves itself.** Failed evals drive targeted improvements. Ship, measure, iterate.

## License

MIT

## Author

Built by [AfterRealm](https://github.com/AfterRealm) with Claude Code.
