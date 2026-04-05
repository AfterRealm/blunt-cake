#!/usr/bin/env python3
"""
Blunt Cake — Self-Improving Eval Loop
Runs the eval, reads failures, proposes SKILL.md improvements, and tracks iterations.

Usage:
  python self_improve.py              # run one improvement cycle
  python self_improve.py --cycles 3   # run 3 improvement cycles
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


def get_latest_iteration():
    """Find the most recent iteration directory."""
    iters = sorted(EVAL_DIR.glob("iteration-*"), key=lambda p: int(p.name.split("-")[1]))
    return iters[-1] if iters else None


def run_improvement_cycle():
    """Run one cycle: eval → analyze failures → propose improvements."""

    print("=" * 60)
    print("  SELF-IMPROVEMENT CYCLE")
    print("=" * 60)

    # Step 1: Run the eval
    print("\n📊 Step 1: Running eval...")
    result = subprocess.run(
        [sys.executable, str(EVAL_DIR / "run_eval.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)

    # Step 2: Read the latest benchmark
    latest = get_latest_iteration()
    if not latest:
        print("❌ No eval results found. Run the eval first.")
        return None

    benchmark = json.loads((latest / "benchmark.json").read_text(encoding="utf-8"))
    iteration = benchmark["iteration"]
    avg_pass_rate = benchmark["avg_pass_rate"]

    print(f"\n📈 Iteration {iteration}: {avg_pass_rate:.0%} pass rate")

    # Step 3: Collect failed assertions
    failures = []
    for case in benchmark.get("per_case", []):
        for detail in case.get("assertion_details", []):
            if not detail.get("passed", True):
                failures.append({
                    "test_case": case["name"],
                    "assertion": detail.get("assertion", "unknown"),
                    "evidence": detail.get("evidence", "no evidence"),
                })

    if not failures:
        print("\n✅ No failures! Skill is performing at maximum. Nothing to improve.")
        return benchmark

    print(f"\n🔍 Step 2: Analyzing {len(failures)} failed assertions...")
    for f in failures:
        print(f"  ❌ [{f['test_case']}] {f['assertion'][:70]}")

    # Step 4: Read current SKILL.md
    current_skill = SKILL_PATH.read_text(encoding="utf-8")

    # Step 5: Ask Opus to propose improvements
    print(f"\n🧠 Step 3: Proposing improvements...")

    improve_prompt = f"""You are improving a Claude Code agent skill based on eval failures.

## Current SKILL.md
{current_skill}

## Failed Assertions (from eval run)
{json.dumps(failures, indent=2)}

## Task
Analyze why each assertion failed and propose specific changes to SKILL.md that would fix them.

Rules:
- Generalize from the failures. Don't add narrow patches for specific test cases.
- Keep the skill lean. Fewer, better instructions outperform exhaustive rules.
- Explain the "why" for each change. Reasoning-based instructions work better than rigid directives.
- Don't change the personality or tone — only improve accuracy, format compliance, and coverage.
- PRESERVE the existing structure and modes. Only modify what needs fixing.

Respond with ONLY valid JSON:
{{
  "analysis": "brief analysis of why assertions failed",
  "changes": [
    {{
      "section": "which section of SKILL.md to change",
      "what": "what to change",
      "why": "why this fixes the failure"
    }}
  ],
  "new_skill_md": "THE COMPLETE UPDATED SKILL.MD TEXT"
}}"""

    response = run_claude("opus", improve_prompt, timeout=180)

    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            result = json.loads(response[json_start:json_end])
        else:
            print("❌ Failed to parse improvement response")
            return benchmark
    except json.JSONDecodeError:
        print("❌ Failed to parse improvement JSON")
        return benchmark

    # Step 6: Show proposed changes
    print(f"\n📝 Proposed changes:")
    for change in result.get("changes", []):
        print(f"  • [{change.get('section', '?')}] {change.get('what', '?')}")
        print(f"    Why: {change.get('why', '?')}")

    # Step 7: Save the improved SKILL.md
    new_skill = result.get("new_skill_md")
    if new_skill and len(new_skill) > 100:
        # Backup current
        backup_path = latest / "SKILL.md.before"
        backup_path.write_text(current_skill, encoding="utf-8")

        # Write new
        SKILL_PATH.write_text(new_skill, encoding="utf-8")
        print(f"\n✅ SKILL.md updated ({len(new_skill)} chars)")
        print(f"   Backup saved to {backup_path}")

        # Save the improvement analysis
        (latest / "improvement.json").write_text(
            json.dumps(result.get("changes", []), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    else:
        print("\n⚠️  No valid SKILL.md in response. Skipping update.")

    return benchmark


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Blunt Cake Self-Improvement Loop")
    parser.add_argument("--cycles", type=int, default=1, help="Number of improvement cycles")
    args = parser.parse_args()

    for i in range(args.cycles):
        print(f"\n{'=' * 60}")
        print(f"  CYCLE {i + 1} of {args.cycles}")
        print(f"{'=' * 60}")

        benchmark = run_improvement_cycle()

        if benchmark and benchmark.get("avg_pass_rate", 0) >= 1.0:
            print(f"\n🏆 Perfect score reached at cycle {i + 1}. Stopping.")
            break

        if i < args.cycles - 1:
            print(f"\n  Running next cycle to verify improvement...")

    print(f"\n{'=' * 60}")
    print(f"  SELF-IMPROVEMENT COMPLETE")
    print(f"{'=' * 60}")

    # Show iteration history
    iters = sorted(EVAL_DIR.glob("iteration-*"), key=lambda p: int(p.name.split("-")[1]))
    if iters:
        print("\n  Iteration History:")
        for it in iters:
            try:
                b = json.loads((it / "benchmark.json").read_text(encoding="utf-8"))
                improved = " (improved)" if (it / "improvement.json").exists() else ""
                print(f"    {it.name}: {b['avg_pass_rate']:.0%} pass rate, "
                      f"accuracy={b.get('avg_accuracy','?')}, humor={b.get('avg_humor','?')}{improved}")
            except Exception:
                print(f"    {it.name}: (no benchmark)")


if __name__ == "__main__":
    main()
