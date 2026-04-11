# Panel Roast Mode

4 specialist agents review in parallel, Head Chef merges. Deep and thorough.

## Panel Roast Process

You are the **Head Chef**. You don't review the code yourself first — you dispatch specialists, then synthesize.

### Step 1: Dispatch the Panel

Spawn all 4 agents **in parallel** using the Agent tool. Each specialist has its own prompt file in `modes/panel-subagents/`. Tell the subagent to read its prompt file, then apply it to the code. Use `model: "opus"` for speed.

**Four specialists to dispatch (all in parallel, single message, 4 Agent calls):**

| Specialist | Prompt file |
|---|---|
| 🔓 Security Auditor | `modes/panel-subagents/security.md` |
| 🐌 Performance Analyst | `modes/panel-subagents/performance.md` |
| 🏗️ Architecture Critic | `modes/panel-subagents/architecture.md` |
| 🤡 Style Judge | `modes/panel-subagents/style.md` |

**Dispatch pattern for each Agent call:**
```
Agent(
  subagent_type: "general-purpose",
  description: "[Specialist name] panel review",
  model: "opus",
  prompt: "Read `modes/panel-subagents/[specialist-file].md` and follow those instructions exactly. Apply the review to the code below. Respond with ONLY the JSON specified in the instructions.\n\nCode to review:\n[FULL CODE HERE]"
)
```

**Path resolution:** The subagent's Read tool resolves paths relative to the current working directory. If the subagent can't find the file via the relative path, fall back to passing the prompt inline — check `${CLAUDE_PLUGIN_ROOT}/modes/panel-subagents/[file]` or glob `**/modes/panel-subagents/[file]` to locate the skill install root.

**Fallback behavior:** If any subagent returns an error or empty JSON, the Head Chef proceeds with the remaining specialists' findings and notes the missing perspective in Panel Notes.

### Step 2: Merge Findings

Once all 4 agents return:
1. Parse each agent's JSON findings.
2. **Deduplicate cross-agent findings.** Two findings from different specialists count as **cross-confirmed** (higher confidence) if EITHER:
   - They reference the same line number (or overlapping line ranges), OR
   - They describe the same root cause in different words (e.g., "SQL injection" and "Unparameterized query string concatenation" are the same finding; "missing input validation" and "user input passed directly to query" are the same finding).

   When in doubt, treat them as **separate** findings — false splits are easier to clean up than false merges. Cross-confirmed findings get a `[CROSS-CONFIRMED ×N]` badge in the final roast where N is the number of specialists who flagged it.
3. Categorize all findings into the 6 review categories (see `modes/standard.md` Code Review Categories).
4. Rank by severity (CRITICAL first).

### Step 3: Write the Roast

As the Head Chef, write the final roast using the merged findings. Follow the **Code Output Format** from `modes/standard.md`, but add the Panel Notes section before Final Words:

```
## Panel Notes
| Agent | Findings | Highlight |
|-------|:--------:|-----------|
| 🔓 Security Auditor | X | [their worst finding] |
| 🐌 Performance Analyst | X | [their worst finding] |
| 🏗️ Architecture Critic | X | [their worst finding] |
| 🤡 Style Judge | X | [their worst finding] |
| **Cross-confirmed** | X | [findings multiple agents independently caught] |
```

Cross-confirmed findings should be emphasized in the roast — if 3 out of 4 specialists independently flagged the same thing, that's a real problem.

After the panel roast, offer Auto-Fix (see Auto-Fix Mode in SKILL.md).
