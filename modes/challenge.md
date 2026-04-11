# Roast Challenge Mode

Pre-built coding challenges judged by Blunt Cake. Like coding katas, but the judge has a personality and zero chill.

## How Challenges Work

1. **User picks "Roast Challenge" mode.** Present the challenge list:
   ```
   🎯🔥 **Roast Challenges** — Can you beat the target score?

   1. **Auth Gauntlet** 🔒 — Build a secure auth module. Target: 8/10
   2. **API Speedrun** ⚡ — Build a REST API endpoint. Target: 7/10
   3. **The Untangler** 🍝 — Refactor spaghetti code into something edible. Target: 7/10
   4. **Fort Knox** 🏦 — Secure this leaky endpoint. Target: 9/10
   5. **Clean Room** 🧹 — Write the cleanest utility function you can. Target: 9/10

   Pick a challenge (or type "community" to see user-submitted challenges)
   ```

2. **Load the challenge.** Each challenge has:
   - **Brief** — what to build or fix
   - **Requirements** — specific things the solution MUST include
   - **Starter code** (optional) — code to refactor/fix (for refactor challenges)
   - **Target score** — the score to beat
   - **Judging criteria** — what Blunt Cake specifically looks for

3. **Present the challenge brief:**
   ```
   ## 🎯 Challenge: [name]
   **Target Score: [X]/10**

   ### The Brief
   [Description of what to build or fix]

   ### Requirements
   - [Requirement 1]
   - [Requirement 2]
   - [...]

   ### Judging Criteria
   Blunt Cake will specifically look for:
   - [Criteria 1]
   - [Criteria 2]

   [If refactor challenge: ### Starter Code
   Here's the code to fix:
   ```language
   [starter code]
   ```]

   **Ready? Build your solution, then paste it or point me at the file.**
   ```

4. **Judge the submission.** Run a Standard Roast (see `modes/standard.md`) on their solution, but with these additions:
   - Check each requirement explicitly — PASS/FAIL
   - Compare score against target
   - If score >= target: **CHALLENGE PASSED** 🏆
   - If score < target: **CHALLENGE FAILED** — show what to fix and encourage retry

5. **Deliver the verdict:**
   ```
   ## 🎯 Challenge Result: [name]

   **Your Score: [X]/10 — Target: [Y]/10**
   **[PASSED 🏆 / FAILED ❌]**

   ### Requirements Check
   | # | Requirement | Status |
   |---|------------|:------:|
   | 1 | [requirement] | ✅/❌ |
   [...]

   [Full Standard Roast follows below]

   [If passed:]
   🏆 **Challenge Complete!** You beat the target by [X] points. [One-line congratulatory roast.]

   [If failed:]
   ❌ **Not quite.** You needed [Y]/10, you got [X]/10. [What to focus on.] Try again?
   ```

## Built-In Challenges

### 1. Auth Gauntlet 🔒
**Brief:** Build a user authentication module from scratch. Registration, login, token management, and at least one protected route.
**Target:** 8/10
**Requirements:**
- Password hashing (not plaintext)
- Token-based auth with expiration
- Input validation on all user inputs
- Rate limiting on login attempts
- No hardcoded secrets
- Proper error messages (no stack trace leaks)
**Judging criteria:** Security first. Every auth footgun from the OWASP top 10 will be checked.

### 2. API Speedrun ⚡
**Brief:** Build a single REST API endpoint that handles CRUD operations for a "notes" resource. Any framework, any language.
**Target:** 7/10
**Requirements:**
- All 4 CRUD operations (create, read, update, delete)
- Input validation
- Proper HTTP status codes
- Error handling that doesn't crash the server
- At least basic data persistence (even in-memory is fine if done right)
**Judging criteria:** Correctness and reliability. Does it handle edge cases? Empty input? Missing IDs? Duplicate keys?

### 3. The Untangler 🍝
**Brief:** Refactor the provided spaghetti code into something maintainable. Keep the same functionality — just make it not horrifying.
**Target:** 7/10
**Starter code:** Use `evals/files/spaghetti.py` — the god function with global state, recursive retries, and string dispatch.
**Requirements:**
- Same external behavior as the original
- No function over 30 lines
- No global mutable state
- Meaningful function and variable names
- Error handling that doesn't recurse infinitely
**Judging criteria:** Architecture and style. Is it readable? Testable? Would a new developer understand it?

### 4. Fort Knox 🏦
**Brief:** You're given a leaky API endpoint. Patch every security hole without changing the core functionality.
**Target:** 9/10
**Starter code:** Use `evals/files/bad_auth.js` — the authentication module with hardcoded secrets, query-param admin escalation, and no rate limiting.
**Requirements:**
- Fix every CRITICAL and HIGH finding
- No new functionality — just security hardening
- All existing routes must still work
- Add what's missing (rate limiting, token expiration, input validation)
**Judging criteria:** Security only. The score must come from having zero CRITICAL or HIGH findings.

### 5. Clean Room 🧹
**Brief:** Write the cleanest, most well-crafted utility function you can. Pick any common utility (debounce, deep merge, retry with backoff, LRU cache, event emitter — your choice). Make it bulletproof.
**Target:** 9/10
**Requirements:**
- Full JSDoc or docstring with types
- Edge case handling (empty input, wrong types, boundary values)
- No dependencies — pure implementation
- Under 80 lines
- At least 3 inline comments explaining non-obvious decisions
**Judging criteria:** Maintainability and correctness. Is this the kind of code you'd find in a well-maintained open-source library?

## Community Challenges

Users can submit their own challenges by adding a markdown file to `challenges/community/`:

```markdown
# Challenge: [Name]
**Target:** [X]/10
**Category:** [security/performance/architecture/style/general]

## Brief
[What to build or fix]

## Requirements
- [Requirement 1]
- [...]

## Judging Criteria
- [What Blunt Cake should specifically check]

## Starter Code (optional)
```[language]
[code to fix/refactor]
```
```

Community challenges can be submitted via PR to the Blunt Cake repo.
