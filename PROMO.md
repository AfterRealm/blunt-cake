# 🔥 Roast My Code — a Claude Code Agent Skill

Your code review called. It said it's tired of being boring.

**Roast My Code** is an agent skill with four modes that cover everything from quick laughs to professional-grade analysis. Every roast is backed by a real finding. Every finding comes with a fix.

## Four modes

**🔥 Standard Roast** — single-pass review. Fast, funny, thorough.

**👨‍🍳 Panel Roast** — spawns 4 specialist agents in parallel (Security Auditor, Performance Analyst, Architecture Critic, Style Judge). Head Chef merges findings. Cross-confirmed issues get flagged with higher confidence. It's a roast *panel*.

**🎯 Skill Roast** — feed it a SKILL.md and it roasts the *skill design itself*. Trigger clarity, instruction gaps, edge cases, eval-readiness. Meta.

**📊 Eval Mode** — dead serious code analysis. Generates testable assertions, grades each PASS/FAIL with evidence, scores 5 quality dimensions, assigns a letter grade. Professional report. Then delivers the verdict with roast energy.

## Sample roasts
> *"You hashed the password with bcrypt but stored the session token in localStorage. That's like locking your front door and leaving the key taped to the window."*

> *"`proc()` takes 8 parameters, handles 7 modes, and has a default behavior for when you pass no mode at all. It's not a function — it's a microservice disguised as a `def`."*

## Sample eval verdict
> *Grade: C — "You validated the password and forgot everything else. Like acing the quiz and failing the final."*

## The Roast Scale
| Score | Rating |
|:---:|---|
| 10 | 👨‍🍳 Chef's Kiss — I came to roast and left humbled |
| 6-7 | 🍳 Medium — Edible but needs seasoning |
| 2-3 | 🗑️ Dumpster Fire — I've seen better code in a CAPTCHA |
| 0-1 | ☠️ Health Violation — Ship this and someone's going to the hospital |

## It improves itself
Ships with a self-improving eval loop. The skill runs tests, reads its own failures, proposes fixes to its own SKILL.md, and re-evaluates. Went from 93% → 100% in 4 iterations. Automated.

## Install
```
claude plugin add AfterRealm/roast-my-code
```

**GitHub:** https://github.com/AfterRealm/roast-my-code

Your code's been talking behind your back. Time to find out what it's saying. 🔥
