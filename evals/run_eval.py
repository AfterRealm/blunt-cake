#!/usr/bin/env python3
"""
Blunt Cake — Evaluation Runner
Runs test cases with and without the skill, judges assertions, produces a report.

Usage:
  python run_eval.py              # full eval
  python run_eval.py --markdown   # also output Discord-friendly markdown
"""

import subprocess
import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

EVAL_DIR = Path(__file__).parent
PROJECT_DIR = EVAL_DIR.parent
SKILL_PATH = PROJECT_DIR / "SKILL.md"
EVALS_FILE = EVAL_DIR / "evals.json"


def run_claude(model, prompt, timeout=120):
    env = os.environ.copy()
    env["MCP_CONNECTION_NONBLOCKING"] = "true"
    try:
        result = subprocess.run(
            ["claude", "-p", "--model", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=timeout,
            env=env,
        )
        return result.stdout.decode("utf-8", errors="replace").strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERROR: {e}]"


def run_eval():
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Load eval config
    evals = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    test_cases = evals["evals"]

    print("=" * 60)
    print("  ROAST MY CODE — EVALUATION")
    print(f"  {now.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  {len(test_cases)} test cases")
    print("=" * 60)
    print()

    results = []

    for tc in test_cases:
        print(f"[{tc['id']}/{len(test_cases)}] {tc['name']}")

        # Load test files
        file_contents = []
        for f in tc.get("files", []):
            fp = PROJECT_DIR / f
            if fp.exists():
                file_contents.append(f"### {fp.name}\n```\n{fp.read_text(encoding='utf-8')}\n```")

        code_block = "\n\n".join(file_contents)

        # ── Run WITHOUT skill ──
        bare_prompt = f"""Review this code. Identify bugs, security issues, performance problems, and style issues. Be thorough.

{code_block}"""

        print("  Without skill...", end=" ", flush=True)
        bare_output = run_claude("opus", bare_prompt, timeout=90)
        print(f"done ({len(bare_output)} chars)")

        # ── Run WITH skill ──
        skill_prompt = f"""You have the following skill loaded. Follow its instructions exactly.

{skill_text}

---

The user says: "{tc['prompt']}"

Here is the code to review:

{code_block}"""

        print("  With skill...", end=" ", flush=True)
        skill_output = run_claude("opus", skill_prompt, timeout=120)
        print(f"done ({len(skill_output)} chars)")

        # ── Judge assertions ──
        assertions = tc.get("assertions", [])
        assertion_text = "\n".join(f"  {i+1}. {a}" for i, a in enumerate(assertions))

        judge_prompt = f"""You are an impartial judge evaluating a code review output against specific assertions.

## Assertions to check:
{assertion_text}

## The output to evaluate:
{skill_output}

For each assertion, determine PASS or FAIL with specific evidence from the output.

Respond with ONLY valid JSON:
{{
  "results": [
    {{"assertion": "the assertion text", "passed": true, "evidence": "quote or reference from the output"}}
  ],
  "overall_quality": {{
    "accuracy": 1-5,
    "humor": 1-5,
    "actionability": 1-5,
    "format_compliance": 1-5
  }}
}}"""

        print("  Judging...", end=" ", flush=True)
        judge_raw = run_claude("opus", judge_prompt, timeout=90)
        print("done")

        # Parse judge
        try:
            json_start = judge_raw.find("{")
            json_end = judge_raw.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                judge = json.loads(judge_raw[json_start:json_end])
            else:
                judge = {"results": [], "overall_quality": {}}
        except json.JSONDecodeError:
            judge = {"results": [], "overall_quality": {}}

        assertion_results = judge.get("results", [])
        quality = judge.get("overall_quality", {})
        passed = sum(1 for r in assertion_results if r.get("passed"))
        total = len(assertions)
        pass_rate = passed / total if total > 0 else 0

        result = {
            "id": tc["id"],
            "name": tc["name"],
            "assertions_total": total,
            "assertions_passed": passed,
            "pass_rate": round(pass_rate, 2),
            "quality": quality,
            "assertion_details": assertion_results,
            "bare_output_len": len(bare_output),
            "skill_output_len": len(skill_output),
        }
        results.append(result)

        # Print summary
        grade = "✅" if pass_rate >= 0.8 else "🟡" if pass_rate >= 0.5 else "❌"
        print(f"  {grade} {passed}/{total} assertions passed ({pass_rate:.0%})")
        print(f"     Quality: accuracy={quality.get('accuracy','?')} humor={quality.get('humor','?')} actionability={quality.get('actionability','?')} format={quality.get('format_compliance','?')}")
        print()

    # ── Aggregate ──
    avg_pass_rate = sum(r["pass_rate"] for r in results) / len(results) if results else 0
    avg_accuracy = sum(r["quality"].get("accuracy", 0) for r in results) / len(results) if results else 0
    avg_humor = sum(r["quality"].get("humor", 0) for r in results) / len(results) if results else 0
    avg_actionability = sum(r["quality"].get("actionability", 0) for r in results) / len(results) if results else 0
    avg_format = sum(r["quality"].get("format_compliance", 0) for r in results) / len(results) if results else 0

    print("=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"  Assertion pass rate:  {avg_pass_rate:.0%}")
    print(f"  Accuracy:             {avg_accuracy:.1f}/5")
    print(f"  Humor:                {avg_humor:.1f}/5")
    print(f"  Actionability:        {avg_actionability:.1f}/5")
    print(f"  Format compliance:    {avg_format:.1f}/5")
    print("=" * 60)

    # Save results
    iteration = len(list(EVAL_DIR.glob("iteration-*"))) + 1
    iter_dir = EVAL_DIR / f"iteration-{iteration}"
    iter_dir.mkdir(parents=True)

    benchmark = {
        "timestamp": now.isoformat() + "Z",
        "iteration": iteration,
        "test_cases": len(results),
        "avg_pass_rate": round(avg_pass_rate, 2),
        "avg_accuracy": round(avg_accuracy, 1),
        "avg_humor": round(avg_humor, 1),
        "avg_actionability": round(avg_actionability, 1),
        "avg_format_compliance": round(avg_format, 1),
        "per_case": results,
    }

    (iter_dir / "benchmark.json").write_text(
        json.dumps(benchmark, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n  Saved to {iter_dir}/")
    return results, benchmark


def markdown_report(results, benchmark):
    lines = []
    lines.append("# 🔥 Blunt Cake — Eval Results")
    lines.append(f"*Iteration {benchmark['iteration']} — {benchmark['timestamp'][:10]}*\n")

    lines.append("## Scores")
    lines.append(f"- **Assertion pass rate:** {benchmark['avg_pass_rate']:.0%}")
    lines.append(f"- **Accuracy:** {benchmark['avg_accuracy']}/5")
    lines.append(f"- **Humor:** {benchmark['avg_humor']}/5")
    lines.append(f"- **Actionability:** {benchmark['avg_actionability']}/5")
    lines.append(f"- **Format compliance:** {benchmark['avg_format_compliance']}/5")
    lines.append("")

    lines.append("## Per-Case Breakdown")
    lines.append("| Test Case | Assertions | Pass Rate | Accuracy | Humor |")
    lines.append("|-----------|:----------:|:---------:|:--------:|:-----:|")

    for r in results:
        grade = "✅" if r["pass_rate"] >= 0.8 else "🟡" if r["pass_rate"] >= 0.5 else "❌"
        lines.append(
            f"| {r['name']} | {r['assertions_passed']}/{r['assertions_total']} | "
            f"{grade} {r['pass_rate']:.0%} | {r['quality'].get('accuracy','?')}/5 | "
            f"{r['quality'].get('humor','?')}/5 |"
        )

    lines.append(f"\n*{len(results)} test cases, Opus reviewer + Opus judge.*")

    md = "\n".join(lines)
    out_path = EVAL_DIR / "eval-report.md"
    out_path.write_text(md, encoding="utf-8")
    print(md)
    print(f"\n--- Saved to {out_path} ---", file=sys.stderr)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Blunt Cake Eval Runner")
    parser.add_argument("--markdown", "--md", action="store_true", help="Also output markdown report")
    args = parser.parse_args()

    results, benchmark = run_eval()

    if args.markdown:
        print()
        markdown_report(results, benchmark)
