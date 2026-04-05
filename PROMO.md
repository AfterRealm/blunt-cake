# 🔥 Roast My Code — a Claude Code Agent Skill

Your code review called. It said it's tired of being boring.

**Roast My Code** is an agent skill that does real code review — bugs, security holes, performance issues, architectural crimes — but delivers every finding like a standup set. Every roast is backed by a real finding. Every finding comes with a fix.

## Three modes because one wasn't enough

**🔥 Standard Roast** — single-pass review. Fast, funny, thorough.

**👨‍🍳 Panel Roast** — spawns 4 specialist agents in parallel (Security Auditor, Performance Analyst, Architecture Critic, Style Judge). They review simultaneously, then a Head Chef merges findings. Cross-confirmed issues get flagged with higher confidence. It's a roast *panel*.

**🎯 Skill Roast** — feed it a SKILL.md and it roasts the *skill design itself*. Trigger clarity, instruction gaps, edge cases, eval-readiness. Meta.

## Sample roasts
> *"You hashed the password with bcrypt but stored the session token in localStorage. That's like locking your front door and leaving the key taped to the window."*

> *"`proc()` takes 8 parameters, handles 7 modes, and has a default behavior for when you pass no mode at all. It's not a function — it's a microservice disguised as a `def`."*

> *"These JWTs live forever. You've issued immortal credentials. If one leaks, it's valid until the heat death of the universe."*

## The Roast Scale
| Score | Rating |
|:---:|---|
| 10 | 👨‍🍳 Chef's Kiss — I came to roast and left humbled |
| 6-7 | 🍳 Medium — Edible but needs seasoning |
| 2-3 | 🗑️ Dumpster Fire — I've seen better code in a CAPTCHA |
| 0-1 | ☠️ Health Violation — Ship this and someone's going to the hospital |

## It improves itself
Ships with a self-improving eval loop. The skill runs tests, reads its own failures, proposes fixes to its own SKILL.md, and re-evaluates. Automated iteration until convergence. `python evals/self_improve.py --cycles 3`

**First eval: 93% assertion pass rate. 5/5 humor. 5/5 actionability.**

## Install
```
claude plugin add AfterRealm/roast-my-code
```

**GitHub:** https://github.com/AfterRealm/roast-my-code

Your code's been talking behind your back. Time to find out what it's saying. 🔥
