# Skill Roast Mode

Review a SKILL.md design instead of code. Meta-review. Be constructive — skill authors are building something new. Roast the gaps, but respect the ambition. Make the skill better, not the builder worse.

## Skill Review Steps

1. **Read the entire skill definition.** Understand what it's trying to do and who it's for.
2. **Evaluate each category.** Score each of the 8 categories below.
3. **Write the roast.** Same energy as code roasts, but constructive. The goal is to make the skill better.
4. **Score it.** Rate on the Skill Roast Scale.
5. **Deliver the verdict.** Follow the Skill Output Format below.

## Skill Review Categories

1. **🎯 TRIGGER** — Is the trigger clear? Will it fire correctly? Will it false-positive on unrelated prompts? Is there priority logic if multiple triggers could match?
2. **📋 INSTRUCTIONS** — Are the instructions specific enough to produce consistent output? Too vague? Too rigid? Would two different models produce the same structure?
3. **🧪 EDGE CASES** — What happens with empty input? Huge input? Ambiguous requests? Multilingual code? Does the skill handle gracefully or crash and burn?
4. **📐 OUTPUT FORMAT** — Is the output format well-defined with a template? Will it produce parseable, consistent results? Could you regex the score out of the output?
5. **🔄 PROCESS** — Is the workflow logical? Missing steps? Redundant steps? Steps in wrong order? Does it tell the model WHEN to do each thing?
6. **⚖️ RULES** — Are the rules internally consistent? Contradictory? Missing obvious guardrails? Prioritized or just a flat list?
7. **✨ CREATIVITY** — Is this skill actually useful? Does it do something a bare prompt can't? What's the unique value? Would you install this?
8. **📊 EVAL-READINESS** — Could you write meaningful pass/fail assertions for this skill's output? If not, the spec is too vague to test.

## Skill Roast Scale

| Score | Rating |
|:---:|---|
| 10 | 🏆 Production-grade — ship it, I'd install this |
| 7-9 | 📦 Almost there — real value, needs polish |
| 4-6 | 📝 Draft — the idea is good, the spec needs work |
| 1-3 | 🗒️ Napkin sketch — you wrote a wish, not a skill |

## Skill Output Format

```
# 🔥 ROAST MY SKILL — [skill name]

## The Verdict
[One-paragraph summary roast of the skill design. Be funny but constructive.]

**Score: [X]/10 — [Rating Emoji] [Rating Name]**

---

## Findings

### [Category Emoji] [CATEGORY] — [Short title]
> [The roast line — one sentence, punchy, funny]

**What's wrong:** [Actual explanation of the design gap]
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW/NITPICK]
**Suggestion:** [How to fix the skill definition — specific wording or structural change]

[Repeat for each finding]

---

## The Scoreboard
| Category | Issues | Worst Severity |
|----------|:------:|---------------|
| 🎯 Trigger | X | ... |
| 📋 Instructions | X | ... |
| 🧪 Edge Cases | X | ... |
| 📐 Output Format | X | ... |
| 🔄 Process | X | ... |
| ⚖️ Rules | X | ... |
| ✨ Creativity | X | ... |
| 📊 Eval-Readiness | X | ... |

## Final Words
[Closing roast. Acknowledge the ambition, then push them to make it better.]
```

**Note:** Skill Roast does NOT offer Auto-Fix — skill design changes are judgment calls, not mechanical edits.
