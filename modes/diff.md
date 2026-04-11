# Diff Roast Mode

Roast a git diff instead of a whole file. Focused, surgical, and perfect for reviewing changes before committing or after a PR.

## Diff Roast Steps

1. **Get the diff.** Run `git diff` (unstaged), `git diff --cached` (staged), or `git diff <branch>` depending on what the user asked. If they didn't specify, ask:
   ```
   📝 What am I roasting?
   - **Unstaged changes** — what you haven't added yet
   - **Staged changes** — what's about to be committed
   - **Branch diff** — compare against a branch (e.g., main)
   - **Specific commit** — roast a single commit's changes
   ```
2. **Read the diff thoroughly.** Understand what changed AND what the surrounding code does. A diff without context is a trap.
3. **For each changed file**, also read the full file for context. Don't roast a one-line change without understanding the function it lives in.
4. **Focus on what CHANGED.** Don't roast pre-existing code unless the change made it worse or interacts badly with it. Pre-existing issues get a passing mention at most: "This was already bad, but you managed to make it worse."
5. **Identify issues in the changes.** Same categories as Standard Roast (see `modes/standard.md`), but only for changed/added code.
6. **Score the diff**, not the whole file. A clean diff on a messy file can still score high.

## Diff Roast Scale

| Score | Rating | Description |
|:---:|---|---|
| 10 | 🧈 Clean Spread | Perfect diff. Nothing to roast. You may proceed. |
| 8-9 | 🍞 Good Toast | Solid changes. Minor crumbs. |
| 6-7 | 🥪 Mid Sandwich | Edible but you left some ingredients out. |
| 4-5 | 🧀 Half-Baked | The changes need more time in the oven. |
| 2-3 | 🥴 Food Poisoning | This diff actively makes things worse. |
| 0-1 | 🚨 Kitchen Fire | Revert. Revert now. |

## Diff Output Format

```
# 📝 DIFF ROAST — [branch/commit/staged/unstaged]

## The Changelist
[Quick summary: X files changed, Y additions, Z deletions. What is this diff trying to do?]

## The Verdict
[One-paragraph roast of the overall diff quality.]

**Score: [X]/10 — [Rating Emoji] [Rating Name]**

---

## Findings

### [File: filename] — [+X/-Y lines]

#### [Category Emoji] [CATEGORY] — [Short title]
> [The roast line]

**What changed:** [What the diff did and why it's a problem]
**Line:** [diff line reference, e.g., +42 or -15/+15]
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW/NITPICK]
**Fix:**
```[language]
[code fix]
```

[Repeat per finding, grouped by file then category]

---

## Diff Scoreboard
| File | Changes | Issues | Worst Severity |
|------|:-------:|:------:|---------------|
| [file] | +X/-Y | X | ... |

## Final Words
[Closing roast about the diff. Should they commit or should they sit back down?]
```

After the Diff Roast, offer Auto-Fix (see Auto-Fix Mode in SKILL.md).
