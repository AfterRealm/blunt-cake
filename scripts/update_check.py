"""
Blunt Cake — Update checker.
Compares installed skill version against latest GitHub release.
Runs on SessionStart to notify users of available updates.
"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO = "AfterRealm/blunt-cake"
GITHUB_API = f"https://api.github.com/repos/{REPO}/releases/latest"
CURRENT_VERSION = "2.4.0"


def get_latest_version():
    """Fetch latest release tag from GitHub."""
    req = urllib.request.Request(
        GITHUB_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "blunt-cake-skill",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            tag = data.get("tag_name", "")
            return tag.lstrip("v") if tag else None
    except Exception:
        return None


def version_tuple(v):
    """Convert version string to comparable tuple."""
    try:
        return tuple(int(x) for x in v.split("."))
    except Exception:
        return (0, 0, 0)


def main():
    latest = get_latest_version()
    if not latest:
        return  # Can't reach GitHub, skip silently

    if version_tuple(latest) > version_tuple(CURRENT_VERSION):
        print(f"Blunt Cake update available: v{CURRENT_VERSION} -> v{latest}")
        print(f"Update: claude plugin update afterrealm/blunt-cake")
    # If up to date, print nothing


if __name__ == "__main__":
    main()
