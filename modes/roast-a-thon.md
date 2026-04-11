# Roast-a-thon Mode

Roast an entire project directory, file by file, and deliver a project-wide report card with a GPA.

## Roast-a-thon Steps

1. **Scope the project.** Ask the user what to include:
   ```
   🏫 **Roast-a-thon** — Let's grade the whole project.

   What should I review?
   - **All source files** — every .js/.ts/.py/.go/etc. in the project
   - **Specific directory** — just one folder (e.g., `src/api/`)
   - **Custom glob** — you pick the pattern (e.g., `**/*.py`)

   Anything to exclude? (e.g., node_modules, vendor, tests)
   ```
2. **Discover files.** Use Glob to find all matching source files. Skip binaries, lockfiles, generated code, and anything in the exclude list. Cap at 20 files — if there are more, tell the user and ask them to narrow scope or confirm the top 20 by size/importance.
3. **Roast each file.** Run a Standard Roast analysis on each file (internal — abbreviated, not full output per file). For each file, record:
   - Score (0-10)
   - Finding count by severity (CRITICAL, HIGH, MEDIUM, LOW, NITPICK)
   - Top finding (the worst issue)
   - One-line roast summary
4. **Calculate the GPA.** Average all file scores, then convert to a letter grade:
   | GPA | Grade | Honor Roll Status |
   |:---:|:---:|---|
   | 9.0+ | A+ | Dean's List — your code professors are proud |
   | 8.0-8.9 | A | Honor Roll — solid work across the board |
   | 7.0-7.9 | B | Above Average — some files are dragging you down |
   | 6.0-6.9 | C | Average — you pass, but barely |
   | 5.0-5.9 | D | Below Average — summer school recommended |
   | 4.0-4.9 | F | Failing — academic probation |
   | 0-3.9 | F- | Expelled — the dean wants to see you |
5. **Identify the valedictorian and the dropout.** The highest-scoring file is the valedictorian (celebrate it). The lowest-scoring file is the dropout (roast it extra).
6. **Cross-file patterns.** Look for issues that appear in multiple files — these are project-wide habits, not one-off mistakes. Flag the top 3 project-wide patterns.
7. **Deliver the report card.** Follow the Roast-a-thon Output Format.

## Roast-a-thon Output Format

```
# 🏫 ROAST-A-THON — [project name or directory]

## The Enrollment
[X files reviewed. Brief description of the project scope.]

## The GPA
**[X.X]/10 — Grade: [Letter] — [Honor Roll Status]**

---

## The Transcript
| File | Score | Grade | Findings | Worst Issue |
|------|:-----:|:-----:|:--------:|-------------|
| [file1] | X/10 | [emoji] | X | [one-line summary] |
| [file2] | X/10 | [emoji] | X | [one-line summary] |
[... all files, sorted by score ascending (worst first)]

---

## 🎓 Valedictorian: [best file]
> [One-line roast celebrating the best file]
[What it did right. 2-3 sentences.]

## 📎 The Dropout: [worst file]
> [One-line roast burning the worst file]
[What it did wrong. 2-3 sentences. Top 3 findings.]

---

## 🔄 Project-Wide Patterns
These showed up in multiple files — they're habits, not accidents:

### Pattern 1: [name]
**Files affected:** [list]
**What's happening:** [description]
**Fix:** [project-wide recommendation]

### Pattern 2: [name]
[...]

### Pattern 3: [name]
[...]

---

## The Report Card 🍰
[One-paragraph summary roast of the entire project. Acknowledge strengths, burn the weaknesses, give an overall vibe check. This is the quotable paragraph — make it shareable.]
```

After the Roast-a-thon, offer Auto-Fix for the dropout file (see Auto-Fix Mode in SKILL.md): "Want me to fix up the dropout? Start with the worst and work our way up."
