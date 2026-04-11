# Changelog

## v2.4.0 — 2026-04-10

> *Thin router, fat modes. SKILL.md lost 80% of its body weight without losing a single mode.*

### Changed — Progressive Disclosure Refactor
- **SKILL.md is now a thin router** (969 → 194 lines, 80% reduction)
- **8 mode files extracted to `modes/`** — loaded only when that mode is picked:
  - `modes/standard.md`, `modes/panel.md`, `modes/skill.md`, `modes/eval.md`
  - `modes/diff.md`, `modes/batter-battle.md`, `modes/roast-a-thon.md`, `modes/challenge.md`
- **Panel subagent prompts extracted** to `modes/panel-subagents/` — `security.md`, `performance.md`, `architecture.md`, `style.md`. Head Chef instructs each spawned specialist to read its own prompt file instead of inlining all 4 prompts (panel.md dropped from 105 → 61 lines as a result).
- **Custom Personality Creator extracted** to `personalities/custom.md` — loaded only when user picks Custom
- **Per-invocation context budget: ~72% smaller** (SKILL.md + 1 mode file ≈ 270 lines vs. 969 before)
- **Rules, Step 1, personality list, Auto-Fix, Roast Card all stay in SKILL.md** — they apply to every mode

### Why
Following Anthropic's recommended skill pattern: keep SKILL.md lean so the model can stay focused, especially on smaller models (Haiku). The 8 modes are mutually exclusive — loading all of them when the user picks one wastes context. Challenge mode alone was 165 lines that most roasts never touched. Now every mode only loads what it needs, and Panel mode's 4 subagent prompts only load when the Head Chef dispatches them.

### Eval Validation — Iteration 8
- 9 test cases, Opus reviewer + Opus judge
- **85% overall pass rate** — matches v2.1.0 baseline (86%) within noise
- **5/9 tests at 100%** — skill-roast, diff-roast, batter-battle, language-pack-snoop, auto-fix-offer
- **3/9 standard mode tests at 88-90%** — same as prior iterations
- Panel Roast 0% — known limitation (subagents can't spawn in `claude -p` headless, unchanged from prior versions)
- All quality metrics 4.4-4.6/5 — refactor introduces zero regression in output quality

### Fixed
- `scripts/update_check.py` `CURRENT_VERSION` bumped to 2.4.0 (was stuck on 2.2.2 since v2.3 releases — missed in prior bumps)
- `evals/run_eval.py` now composes the router + relevant mode file per test case (required by the new split — the old runner only inlined SKILL.md text, which would have broken every test under the new architecture)

### Personality Picker — Two-Stage Fix (UX bug)
- **Bug:** `AskUserQuestion` caps at 4 options per question. Blunt Cake has 6 built-in personalities + Custom = 7 options. The old picker showed Chef + 2 rotating + Custom = only 3 of 6 personalities visible per invocation, with the other 3 hidden behind the "Other" text input.
- **Fix:** Sequential two-stage personality picker. Mode and Personality fire as **separate sequential `AskUserQuestion` calls** — bundled calls render simultaneously and break the gateway pattern. Stage 1 always shows: Chef · Custom · 1 contextually relevant pick · 🎭 **More personalities** (gateway). If the user picks "More personalities", Stage 2 fires as a third sequential call with the 4 personalities that weren't in Stage 1.
- **Result:** Every personality reachable in ≤2 clicks. Custom is always 1 click. No personality is hidden.
- **Important:** The router explicitly forbids bundling Mode + Personality into one `AskUserQuestion` call. Bundled questions submit together and cannot conditionally fire Stage 2 based on Stage 1's answer.
- Found during interactive validation of the v2.4.0 refactor (Curb Cut skill roast with Simon Cowell — Meredith noticed only 3 personalities showed in the picker; second test caught the bundled-vs-sequential bug).

### Description Optimized per agentskills.io Guide
- **Old description** was descriptive ("Brutal but brilliant code reviewer with 8 modes...") and listed internal mechanics rather than user intent.
- **New description** follows the [agentskills.io optimizing-descriptions guide](https://agentskills.io/skill-creation/optimizing-descriptions):
  - Imperative phrasing: "Use this skill when the user wants..."
  - Focuses on user intent (code review with personality, structured findings, fixes), not implementation details
  - Lists trigger categories pushy-style: roast/review/audit/check/judge requests, two-impl comparisons, git diffs, project grading, skill design meta-reviews
  - Explicit "even if the user doesn't say 'roast' or 'Blunt Cake'" pushiness
  - Explicit NOT clause: "Does NOT replace static analyzers, linters, formatters, or test runners" — prevents over-triggering
  - 746 chars, well under the 1024-char spec limit

### Description Optimization Loop — skill-creator systematic run
After applying the principles-based rewrite above, ran Anthropic's `skill-creator` Skill end-to-end optimization loop per the agentskills.io guide's full process — not just the principles section.

**Setup:**
- **20 trigger eval queries** designed by hand: 10 should-trigger (with realistic phrasing, varied detail, inline code so the model could actually invoke the test command), 10 should-not-trigger near-misses (prettier/refactor/accessibility/explain-regex/translate-language/library-lookup — all queries Claude could plausibly handle without reaching for blunt-cake)
- **60/40 train/test split** — train guides changes, held-out test catches overfitting
- **3 trials per query per iteration** for reliable trigger rates
- **5 iterations max** of: evaluate → propose improved description via Claude → re-evaluate
- **Best description selected by held-out test score**, not train score
- **4 parallel workers** (ThreadPoolExecutor) on Windows for ~4× speedup
- **Model:** claude-opus-4-6 (matches the model the user actually runs the skill against)

**Test environment patches** (logged here for transparency and so future maintainers know the system was instrumented):
- `skill-creator/scripts/run_eval.py` — replaced `select.select()` on stdout pipes with a thread-based reader (Windows compat: `select.select()` only accepts sockets on Windows, causing `WinError 10038` on every query); swapped `ProcessPoolExecutor` → `ThreadPoolExecutor` (Windows multiprocessing+subprocess incompatibility kills parallelism otherwise)
- Temporarily replaced global `~/.claude/CLAUDE.md` with a 6-line placeholder during the run — the user's normal global instructions tell every Claude session to do a Vox Memori session startup before handling any user prompt, which caused the eval's trigger detection to miss every signal (the first tool call was always `Read MEMORY-LAYER.md`, never the test command)
- Temporarily moved installed `~/.claude/skills/blunt-cake/` to `~/.claude/blunt-cake.optimization-stash` so the unique-ID test command was the only thing in the available_skills list matching the description (otherwise the model would invoke the real installed blunt-cake skill, which the eval scoring would not recognize as a "trigger" of the test command)
- Both temporary changes restored after the loop completed

**Results (5 iterations, 11 minutes total wall-clock):**

| Iteration | Train accuracy | Train recall | Test accuracy | Test recall | Per-query test |
|---|---|---|---|---|---|
| 1 (principles-based) | 53% | 6% | 50% | **0%** | 4/8 |
| **2 ⭐ winner** | **61%** | **22%** | **62%** | **25%** | **5/8** |
| 3 | 58% | 17% | 54% | 8% | 4/8 |
| 4 | 58% | 17% | 50% | 0% | 4/8 |
| 5 | 61% | 22% | 54% | 8% | 4/8 |

- **Precision was 100% across all iterations** — no description ever false-triggered on the should-not-trigger near-misses (prettier, refactor, accessibility, regex explain, language translation, library recs, test generation, debugging, logging, useEffect example). The polish-pass NOT clause holds firm.
- **The principles-based description's weakness was recall, not precision** — it caught 0% of the held-out should-trigger queries. The realistic test queries used implicit signals ("tear apart," "rip apart," "is this bad," "this is dogshit/trash," self-deprecating dumps) that the principles-based description didn't strongly match.
- **Iteration 2 fixed this** by enumerating aggressive synonyms and emotional signals: "brutal/savage/harsh/merciless feedback," "rip apart," "don't hold back," profanity-about-own-code, "should I push this," etc. This more than tripled the recall (0% → 25% on held-out) and added one full passing query to the test set (4/8 → 5/8).
- **Best selected by held-out test score** (62%, 5/8) — not train (61%, 6/12) — to avoid overfitting per the agentskills.io guide.

**Final description selected: iteration 2.** 960 chars (under the 1024-char spec limit). Replaces the principles-based description with the loop-optimized variant. The winning description is materially more pushy about catching synonyms and emotional signals while preserving the precision-protecting NOT clause.

**Honest caveats:**
- 5/8 on test isn't a great absolute score — it means the loop's best variant still misses ~75% of the should-trigger queries. That's a ceiling on what description-only optimization can do; the queries themselves are intentionally hard (realistic, casual, no explicit "roast" keyword). A perfect description would still struggle with queries like "does this regex suck" where the user's intent is implicit.
- The improvement is real (+12 points test accuracy, 0% → 25% recall) but modest in absolute terms.
- A future v2.4.1 could expand the eval set to ~50 queries and re-run for tighter signal — this run was the minimum viable optimization following the guide's recommended ~20-query design.

### Polish Pass — Final Review Findings
Five additional fixes from the pre-ship review of the v2.4.0 refactor:

1. **Step 1.5 added** — `Confirm There's Something to Roast`. Bridges the gap between personality selection and mode-file load: if no file/code/diff was provided in the trigger, the router asks for it before proceeding. Mode-specific exceptions documented (Roast Challenge skips it; Skill Roast searches for the SKILL.md file).
2. **Batter Battle contextual personality mapping added** — was previously absent from the contextual pick list, falling through to the Simon Cowell default by accident. Now explicit: `Batter Battle / head-to-head → 🎤 Simon Cowell (judge-panel vibe)`.
3. **Markdown menu vs AskUserQuestion guidance** — added one-line clarification at the top of the AskUserQuestion section: the chat-style markdown menu in Step 1 is the fallback for non-interactive contexts (headless `claude -p`, CI), while AskUserQuestion is the primary interface for interactive sessions.
4. **Panel mode merge logic clarified** — `modes/panel.md` Step 2 now defines what counts as cross-confirmed: same line range OR same root cause in different words. "When in doubt, treat as separate" rule added (false splits are easier to clean up than false merges). Cross-confirmed findings get a `[CROSS-CONFIRMED ×N]` badge in the output.
5. **Roast Card version placeholder** — `v2.4` hardcode replaced with `{VERSION}` placeholder. Rule #7 added to Roast Card Rules: read the version from SKILL.md frontmatter at runtime, don't hardcode. Eliminates manual version-bump-stale risk for the card footer.

### No Behavior Changes
All 8 modes, all 6 personalities, all rules, all output formats are identical. This is a pure architectural refactor — every roast produces the same result as v2.3.1 with less context burned. The personality picker fix and the polish pass are UX improvements, not behavior changes — the same personalities exist with the same voices, the same findings get reported with the same severities.

## v2.3.1 — 2026-04-09

### Added
- YAML frontmatter (`name`, `description`) for Agent Skills spec compliance and cross-platform discoverability (skills.sh, etc.)

## v2.3.0 — 2026-04-09

### Added
- **Update checker** — SessionStart hook checks installed version against latest GitHub release and notifies if an update is available

### Fixed
- GitHub Action PR comment footer now shows correct version (was stuck on v2.0)

## v2.2.0 — 2026-04-05

> *Eight modes. Create your own personality. Coding challenges with target scores. This thing has a curriculum now.*

### Custom Personality Creator 🎨
- Pick "Custom" in the personality picker and describe any voice you want
- Blunt Cake generates a full personality spec with sample roast lines
- Preview, tweak, and save custom personalities for reuse
- Saved personalities appear alongside built-in packs on future roasts
- Stored in `.blunt-cake/custom-personalities/` as markdown files

### Roast Challenges 🎯🔥
- 5 built-in coding challenges with target scores to beat
- Auth Gauntlet (8/10), API Speedrun (7/10), The Untangler (7/10), Fort Knox (9/10), Clean Room (9/10)
- Each challenge has: brief, requirements checklist, judging criteria, and optional starter code
- Solutions judged by Standard Roast with per-requirement PASS/FAIL checks
- Community challenges: submit via PR to `challenges/community/`
- Challenge results show score vs target, requirements check table, and full roast

---

## v2.1.0 — 2026-04-05

> *86% eval pass rate. 97% excluding the one mode that literally can't run in headless.*

### Eval Results — Iteration 7
- 9 test cases, 82 assertions, Opus reviewer + Opus judge
- **86% overall pass rate** (97% excluding Panel Roast timeout)
- 7/9 tests at **100%**: security-nightmare, spaghetti-monster, skill-roast, diff-roast, batter-battle, auto-fix, and decent-code at 88%
- Snoop Dogg personality: **88%** — consistent voice throughout, accurate findings
- Auto-Fix offer: **100%** — correct format, correct placement
- Panel Roast: 0% — known limitation (can't spawn subagents in `claude -p` headless mode)
- All quality metrics 4.4-4.6/5 (accuracy, humor, actionability, format compliance)

### Eval Framework Fixes
- All test prompts now explicitly specify mode (e.g., "Standard roast this") to skip interactive mode picker in headless eval
- Fixed eval report template to show correct test case count
- Iteration 6 (pre-fix) and Iteration 7 (post-fix) results included

---

## v2.0.0 — 2026-04-05

> *Seven modes. Six personalities. CI/CD. Hall of Fame. The full bakery.*

### Roast-a-thon 🏫
- Roast an entire project directory — every source file gets scored
- Project GPA with letter grades (A+ Dean's List to F- Expelled)
- Valedictorian (best file) and Dropout (worst file) callouts
- Cross-file pattern detection — finds habits that repeat across the codebase
- Caps at 20 files per run with customizable scope (directory, glob, excludes)

### Shareable Roast Cards 📸
- Compact, styled summary card after any roast — designed for Discord, Slack, X, GitHub
- Includes score, worst finding, best praise, and Blunt Cake link
- Max 20 lines — screenshot-ready, no scrolling
- Works for all modes including Batter Battle and Roast-a-thon

### CI/CD GitHub Action 🤖
- Auto-roast PRs with `.github/workflows/blunt-cake-roast.yml`
- Runs Diff Roast on PR changes, posts result as a collapsible PR comment
- Configurable mode and personality via env vars
- Skips diffs over 2000 lines (too large for single pass)
- Requires only `ANTHROPIC_API_KEY` secret

### Hall of Fame (& Shame) 🏆
- Community leaderboard in `hall-of-fame/README.md`
- Five boards: Shame (lowest wins), Fame (highest wins), Improvement (best glow-ups), Roast-a-thon Honor Roll, Batter Battle Highlights
- Submit via PR or GitHub Discussions

### Language Packs 🧑‍🍳👵😐🎤🐕🏴‍☠️
- 6 roast personalities: Chef (default), Disappointed Grandma, Passive-Aggressive PR Reviewer, Simon Cowell, Snoop Dogg, Pirate
- Personality selection integrated into the initial mode picker
- Same findings, same fixes, same severity — different delivery voice
- Personality affects roast lines, verdicts, and commentary only. Technical substance never changes.

### Diff Roast 📝
- Roast a git diff instead of a whole file — unstaged, staged, branch, or specific commit
- Reads full file context around changes for accurate assessment
- Scores the DIFF, not the whole file — won't blame pre-existing sins (unless you made them worse)
- Diff-specific roast scale (Clean Spread → Kitchen Fire)
- Per-file breakdown with diff line references (+42, -15/+15)

### Batter Battle 🆚
- Two implementations enter, one leaves — head-to-head comparison
- 5 rounds: Bugs, Security, Performance, Style, Architecture
- Per-round winners with specific reasoning, no ties allowed
- Winner gets roasted for remaining flaws, loser gets actionable steal-list
- After battle, offers Auto-Fix for the losing file

### Auto-Fix Mode 🔧
- After any code roast, offers to apply the fixes
- Three fix scopes: All, Critical/High only, or Pick individual fixes
- Applies edits one at a time, most severe first
- After fixing, offers a re-roast to check your new score
- Won't refactor beyond the finding — fixes exactly what was roasted

---

## v1.2.0 — 2026-04-05

> *Four modes. Because one way to judge your code was never enough.*

### Eval Mode (Professional Grade)
- Serious code analysis with scored assertions — no jokes until the final verdict
- Generates 8-12 testable assertions per file across 5 categories: Correctness, Security, Reliability, Performance, Maintainability
- Each assertion graded PASS/FAIL with specific evidence (line numbers, code quotes)
- 5 quality dimension scores (1-5) with one-line justifications
- Letter grade (A-F) with pass rate and overall score
- Critical findings get detailed fixes in serious tone
- Final verdict delivered with roast energy — the payoff

### Interactive Mode Selection
- Skill now asks which mode on trigger: Standard 🔥 / Panel 👨‍🍳 / Skill Roast 🎯 / Eval 📊
- Skips the question if user already specified mode in their trigger
- Clear descriptions for each mode so users know what they're getting

### Self-Roast Fixes (from running Skill Roast on ourselves)
- Trigger priority order formalized (Skill → Panel → Standard → Eval)
- Panel agent prompts expanded from one-liners to full specs with severity scales, JSON schemas, and line number requirements
- Edge case handling added (trivially simple code gets a short roast, not manufactured issues)
- Skill Roast output format fully specified (was inheriting code format)
- Rules section moved to top of SKILL.md (behavioral constraints read first)

---

## v1.1.0 — 2026-04-05

> *One mode wasn't enough. Now there are three.*

### Panel Roast (Multi-Agent)
- 4 specialist agents in parallel — Security Auditor, Performance Analyst, Architecture Critic, Style Judge
- Head Chef coordinator merges, deduplicates, and cross-confirms findings
- Panel Notes table shows which agent found what and where they agreed

### Skill Roast (Meta-Review)
- Review SKILL.md files instead of code — roast the skill design itself
- 8 review categories: Trigger, Instructions, Edge Cases, Output Format, Process, Rules, Creativity, Eval-Readiness
- Separate Skill Roast Scale (Napkin Sketch → Draft → Almost There → Production-Grade)

### Self-Improving Eval Loop
- `self_improve.py` — automated improvement cycle: eval → analyze failures → propose SKILL.md changes → re-eval
- Opus analyzes failed assertions and generates generalized fixes
- SKILL.md backup saved before each modification
- Multi-cycle support: `--cycles 3`, stops early on perfect score

---

## v1.0.0 — 2026-04-05

> *Your code had it coming.*

### The Skill
- Full code review engine with 6 review categories: Bugs, Security, Performance, Style Crimes, Dead Code, Architecture
- Every finding includes a roast, a real explanation, severity rating, AND a concrete fix
- Roast Scale scoring (0-10): Health Violation → Dumpster Fire → Rare → Medium → Well Done → Chef's Kiss
- Structured output: Verdict, Findings, Scoreboard, Final Words

### The Eval
- 3 hand-crafted test files (security nightmare, decent code, spaghetti monster)
- Automated eval runner with Opus as judge
- 28 assertions across test cases
- First run: 93% pass rate, 5/5 humor, 5/5 actionability
- Self-improved to 100% in 4 iterations
