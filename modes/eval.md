# Eval Mode

Serious code analysis with scored assertions. Professional grade. The SERIOUS layer — structured assertions, scored metrics, reproducible results. The comedy stays in the back seat until the final delivery.

## Eval Steps

1. **Read the code thoroughly.** Same deep read as Standard mode.
2. **Generate assertions.** Based on what the code IS (API? CLI? Library? Script?), generate 8-12 specific, testable assertions. These should be objective pass/fail checks, not opinions.

**Assertion categories:**
- **Correctness** — Does the logic do what it claims? Edge cases handled?
- **Security** — Are inputs validated? Secrets protected? Auth present where needed?
- **Reliability** — Will it fail gracefully? Connections closed? Errors handled?
- **Performance** — Algorithmic complexity appropriate? Resources managed?
- **Maintainability** — Could someone else read and modify this? Separation of concerns?

3. **Grade each assertion.** PASS or FAIL with specific evidence (line numbers, quotes from code). No opinions — only facts.
4. **Score quality dimensions.** Rate 1-5 on each:
   - **Correctness** — Does it work?
   - **Security** — Is it safe?
   - **Reliability** — Will it stay up?
   - **Performance** — Is it fast enough?
   - **Maintainability** — Can it evolve?
5. **Compute the results.** Pass rate, average quality score, worst dimension.
6. **Deliver the verdict.** Serious report format, THEN a roast-style final summary.

## Eval Output Format

```
# 📊 CODE EVAL — [filename or project]

## Assertions
| # | Category | Assertion | Result | Evidence |
|---|----------|-----------|:------:|----------|
| 1 | Correctness | [specific testable claim] | ✅/❌ | [line number or code quote] |
| 2 | Security | [specific testable claim] | ✅/❌ | [evidence] |
[... 8-12 assertions total]

**Pass rate: X/Y (Z%)**

## Quality Scores
| Dimension | Score | Notes |
|-----------|:-----:|-------|
| Correctness | X/5 | [one-line justification] |
| Security | X/5 | [one-line justification] |
| Reliability | X/5 | [one-line justification] |
| Performance | X/5 | [one-line justification] |
| Maintainability | X/5 | [one-line justification] |

**Overall: X.X/5**

## Critical Findings
[List only FAIL assertions with detailed explanation and fix. Serious tone. No jokes here — these are real problems.]

### [Category] — [Title]
**Assertion:** [what was tested]
**Evidence:** [specific lines/code that failed]
**Impact:** [what goes wrong if this isn't fixed]
**Fix:**
```[language]
[code fix]
```

[Repeat for each FAIL]

## The Verdict 🔥
[NOW bring the roast energy. One paragraph that summarizes the eval results with comedic delivery. This is the payoff — serious data, funny delivery. Reference specific pass/fail results. Make it memorable.]

**Grade: [A/B/C/D/F] — [one-line roast summary]**
```

## Eval Grading Scale

| Grade | Pass Rate | Overall Score | Meaning |
|:---:|:---:|:---:|---|
| A | >90% | >4.0 | Production-ready. Ship it. |
| B | >75% | >3.5 | Solid with fixable gaps. |
| C | >60% | >2.5 | Needs work. Real issues. |
| D | >40% | >1.5 | Significant problems. Don't deploy. |
| F | <40% | <1.5 | Start over. Sorry. |

**Note:** Eval Mode does NOT offer Auto-Fix — assertions are evaluative, not prescriptive edits.
