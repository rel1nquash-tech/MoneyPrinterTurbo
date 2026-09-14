"""Print the canonical continuation state for the MoneyPrinterTurbo project."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"<git unavailable: {exc}>"
    return result.stdout.strip()


def main() -> None:
    branch = run_git("branch", "--show-current")
    commit = run_git("rev-parse", "--short", "HEAD")
    status = run_git("status", "--short")

    print("=== MoneyPrinterTurbo — Development Resume ===")
    print(f"Root:   {ROOT}")
    print(f"Branch: {branch or '<unknown>'}")
    print(f"HEAD:   {commit or '<unknown>'}")
    print()

    if branch != "feature/trend-generator":
        print("WARNING: Switch to feature/trend-generator before continuing.")
    else:
        print("Branch check: OK")

    print("Working tree:")
    print(status or "clean")
    print()
    print("Sprint 6 status:")
    print("  [done] multi-format variants (9:16 / 1:1 / 16:9)")
    print("  [done] render planner")
    print("  [done] render runner")
    print("  [done] safe video-use aggregation + manifest")
    print("  [done] dedicated Multi-format Video WebUI entry point")
    print()
    print("Next:")
    print("  Controlled Main.py integration; keep single-format behavior unchanged.")
    print("  Do not modify app/services/task.py.")
    print()
    print("Canonical handoff: CONTINUE.md")


if __name__ == "__main__":
    main()
