#!/usr/bin/env python3
"""Refresh the small profile signal SVG from GitHub's public API."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

USERNAME = os.getenv("GH_USERNAME", "kooroosh1363")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUTPUT = Path("assets/signal.svg")


def public_repo_count() -> int:
    count = 0
    page = 1
    while True:
        request = Request(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}&type=public",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "royal-purple-profile",
                **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
            },
        )
        with urlopen(request, timeout=20) as response:
            repos = json.load(response)
        count += sum(not repo.get("private", False) for repo in repos)
        if len(repos) < 100:
            return count
        page += 1


def render(count: int, refreshed: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="150" viewBox="0 0 1200 150" role="img" aria-labelledby="title desc">
  <title id="title">Live portfolio signal</title><desc id="desc">Public repository count and engineering evidence priorities, refreshed from GitHub.</desc>
  <defs><linearGradient id="b" x1="0" x2="1"><stop stop-color="#10071F"/><stop offset="1" stop-color="#241044"/></linearGradient></defs>
  <style>.s{{font-family:Inter,Segoe UI,Arial,sans-serif}}.m{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.p{{animation:p 2.8s ease-in-out infinite}}@keyframes p{{50%{{opacity:.35}}}}@media(prefers-reduced-motion:reduce){{.p{{animation:none}}}}</style>
  <rect width="1200" height="150" rx="22" fill="url(#b)"/>
  <circle cx="48" cy="34" r="5" fill="#C4B5FD" class="p"/><text x="62" y="39" class="m" fill="#A78BFA" font-size="12" letter-spacing="2">LIVE PORTFOLIO SIGNAL</text>
  <g class="s"><text x="48" y="96" fill="#F8F7FF" font-size="36" font-weight="750">{count}</text><text x="99" y="92" fill="#AFA6BE" font-size="13">PUBLIC REPOSITORIES</text>
  <path d="M310 42V111M595 42V111M885 42V111" stroke="#8B5CF6" stroke-opacity=".25"/>
  <text x="348" y="73" fill="#D8B4FE" font-size="13" font-weight="700">VERIFICATION</text><text x="348" y="98" fill="#AFA6BE" font-size="14">tests · CI · data contracts</text>
  <text x="633" y="73" fill="#D8B4FE" font-size="13" font-weight="700">CONTROL</text><text x="633" y="98" fill="#AFA6BE" font-size="14">guardrails · human approval</text>
  <text x="923" y="73" fill="#D8B4FE" font-size="13" font-weight="700">REFRESHED</text><text x="923" y="98" fill="#AFA6BE" font-size="14">{refreshed} UTC</text></g>
</svg>'''


if __name__ == "__main__":
    today = datetime.now(timezone.utc).date().isoformat()
    OUTPUT.write_text(render(public_repo_count(), today), encoding="utf-8")
