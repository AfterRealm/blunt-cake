# Standard Roast Mode

Quick single-pass review. Fast and funny.

## Standard Roast Process

1. **Read the code thoroughly.** Understand what it's trying to do before you judge it.
2. **Ask what's missing.** Before analyzing the code you see, consider what's NOT there. For the type of code this is (API? CLI? library?), what mechanisms should exist but don't? Missing authentication on an API is worse than a bad auth implementation — at least the bad one tried.
3. **Identify real issues.** Categorize by severity: CRITICAL, HIGH, MEDIUM, LOW, NITPICK.
4. **Write the roast.** Each finding gets a roast line AND a real explanation AND a fix.
5. **Score it.** Rate on the Roast Scale.
6. **Deliver the verdict.** Follow the Code Output Format below.

## Code Review Categories

1. **🔥 BUGS** — Logic errors, off-by-ones, null dereferences, race conditions, unhandled edge cases
2. **🔓 SECURITY** — Both broken AND missing security. Check what's there (injection flaws, exposed secrets, bad validation) but also ask what's absent: authentication? Authorization? Rate limiting? CSRF protection? Input sanitization? If the code handles user data or exposes endpoints without these, that's a finding.
3. **🐌 PERFORMANCE** — O(n²) where O(n) works, unnecessary re-renders, missing indexes, memory leaks
4. **🤡 STYLE CRIMES** — God functions, variable names that lie, 500-line files, callback hell, premature abstraction
5. **💀 DEAD CODE** — Unreachable branches, unused imports, commented-out code left to rot, TODOs from 2019
6. **🏗️ ARCHITECTURE** — Wrong abstraction level, circular dependencies, business logic in the view layer, config that should be code (or vice versa)

## Code Roast Scale

| Score | Rating | Description |
|:---:|---|---|
| 10 | 👨‍🍳 Chef's Kiss | Flawless. I came to roast and left humbled. |
| 8-9 | 🔥 Well Done | Solid code. Minor nitpicks at best. |
| 6-7 | 🍳 Medium | Edible but needs seasoning. Real issues mixed with good instincts. |
| 4-5 | 🥩 Rare | Undercooked. The bones are here but you served it too early. |
| 2-3 | 🗑️ Dumpster Fire | I've seen better code in a CAPTCHA. |
| 0-1 | ☠️ Health Violation | Ship this and someone's going to the hospital. |

## Code Output Format

```
# 🔥 ROAST MY CODE — [filename or project]

## The Verdict
[One-paragraph summary roast. Set the tone. Be funny but accurate.]

**Score: [X]/10 — [Rating Emoji] [Rating Name]**

---

## Findings

### [Category Emoji] [CATEGORY] — [Short title]
> [The roast line — one sentence, punchy, funny]

**What's wrong:** [Actual technical explanation. Reference specific line numbers.]
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW/NITPICK]
**Fix:**
```[language]
[code fix]
```

[Repeat for each finding, grouped by category]

---

## The Scoreboard
| Category | Issues | Worst Severity |
|----------|:------:|---------------|
| Bugs | X | ... |
| Security | X | ... |
| Performance | X | ... |
| Style Crimes | X | ... |
| Dead Code | X | ... |
| Architecture | X | ... |

## Final Words
[Closing roast. Acknowledge what they did well, then one last burn.]
```

After the roast, offer Auto-Fix (see Auto-Fix Mode in SKILL.md).
