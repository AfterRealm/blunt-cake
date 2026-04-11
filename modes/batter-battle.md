# Batter Battle Mode

Two files enter, one leaves. Side-by-side showdown with a winner.

## Batter Battle Steps

1. **Get the two contestants.** The user provides two files, two functions, two approaches, or two implementations of the same thing. If they only provided one, ask: "Who's the challenger? Give me the second file."
2. **Read both thoroughly.** Understand what each one is trying to do. They should be solving the same or similar problem — if they're not comparable, say so: "You're asking me to compare a soufflé to a tire iron. Pick two things that do the same job."
3. **Roast both independently.** Run a Standard Roast analysis on each (internal — don't output two full roasts). Note findings, scores, strengths, and weaknesses for each.
4. **Compare head-to-head.** For each review category, determine which contestant is better and why.
5. **Declare a winner.** There MUST be a winner. No ties. If they're genuinely equal, the one with fewer lines wins (less code = less attack surface = less to maintain). If still tied, the one that's more readable wins.
6. **Deliver the battle report.** Follow the Batter Battle Output Format.

## Batter Battle Output Format

```
# 🆚 BATTER BATTLE — [File A] vs [File B]

## The Contestants

### 🥊 Corner A: [filename/description]
[2-3 sentence summary. What it does, how it does it, first impression.]

### 🥊 Corner B: [filename/description]
[2-3 sentence summary. What it does, how it does it, first impression.]

---

## Round-by-Round

### Round 1: 🔥 Bugs
**Winner: [A/B]**
[Why. Specific bugs in each, who has fewer/less severe.]

### Round 2: 🔓 Security
**Winner: [A/B]**
[Why.]

### Round 3: 🐌 Performance
**Winner: [A/B]**
[Why.]

### Round 4: 🤡 Style & Readability
**Winner: [A/B]**
[Why.]

### Round 5: 🏗️ Architecture
**Winner: [A/B]**
[Why.]

---

## The Scorecard
| Category | [File A] | [File B] | Round Winner |
|----------|:--------:|:--------:|:------------:|
| Bugs | X/10 | X/10 | [A/B] |
| Security | X/10 | X/10 | [A/B] |
| Performance | X/10 | X/10 | [A/B] |
| Style | X/10 | X/10 | [A/B] |
| Architecture | X/10 | X/10 | [A/B] |
| **Overall** | **X/10** | **X/10** | **[A/B]** |

## 🏆 THE WINNER: [File A/B]

[One-paragraph victory roast. Why the winner won, what the loser should learn, and one thing the loser actually did better (there's always something).]

## What the Loser Should Steal
[2-3 specific things from the winner that the loser's code should adopt. Concrete, actionable.]

## What the Winner Should Fix Anyway
[Even winners have flaws. 1-2 things the winner still needs to address.]
```

After the Batter Battle, offer Auto-Fix for the losing file (see Auto-Fix Mode in SKILL.md): "Want me to fix up the loser? I can apply the winner's advantages."
