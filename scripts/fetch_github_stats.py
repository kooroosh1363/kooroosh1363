#!/usr/bin/env python3
"""Fetch public profile, repository, and contribution data for the preview."""

from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

USERNAME = "kooroosh1363"
OUTPUT = Path("data/github_stats.json")


def get(url: str, accept: str = "application/vnd.github+json") -> bytes:
    headers = {"Accept": accept, "User-Agent": "royal-purple-profile"}
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return response.read()


profile = json.loads(get(f"https://api.github.com/users/{USERNAME}"))
repos = json.loads(get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=public"))
contribution_html = get(
    f"https://github.com/users/{USERNAME}/contributions", "text/html"
).decode("utf-8")

pattern = re.compile(
    r'<td[^>]*data-date="([0-9-]+)"[^>]*data-level="([0-4])"[^>]*></td>'
    r"\s*<tool-tip[^>]*>(.*?)</tool-tip>",
    re.S,
)
days = []
for day, level, tooltip in pattern.findall(contribution_html):
    count_match = re.search(r"([0-9,]+) contributions?", tooltip)
    count = int(count_match.group(1).replace(",", "")) if count_match else 0
    days.append({"date": day, "level": int(level), "count": count})

today = date.today()
range_start = today - timedelta(days=364)
recent = [d for d in days if range_start.isoformat() <= d["date"] <= today.isoformat()]
counts_by_date = {item["date"]: item["count"] for item in recent}


def contributions_since(days_back: int) -> int:
    start = today - timedelta(days=days_back - 1)
    return sum(
        count for day, count in counts_by_date.items() if start.isoformat() <= day <= today.isoformat()
    )

payload = {
    "username": USERNAME,
    "refreshed": today.isoformat(),
    "public_repos": int(profile["public_repos"]),
    "followers": int(profile["followers"]),
    "following": int(profile["following"]),
    "stars": sum(int(repo["stargazers_count"]) for repo in repos),
    "contributions": sum(day["count"] for day in recent),
    "today_count": counts_by_date.get(today.isoformat(), 0),
    "last_7_days": contributions_since(7),
    "last_30_days": contributions_since(30),
    "active_days": sum(day["count"] > 0 for day in recent),
    "max_daily": max((day["count"] for day in recent), default=0),
    "days": days,
}
OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: value for key, value in payload.items() if key != "days"}, indent=2))
