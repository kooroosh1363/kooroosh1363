#!/usr/bin/env python3
"""Generate a GitHub-safe animated royal-purple terminal profile preview."""

import json
from datetime import date, timedelta
from pathlib import Path

W, H = 1200, 1740
BG = "#0d1117"
PANEL = "#10071f"
PANEL_2 = "#160a2b"
ROYAL = "#7c3aed"
VIOLET = "#a78bfa"
LAV = "#d8b4fe"
PINK = "#f0abfc"
TEXT = "#f8f7ff"
MUTED = "#968ba8"
STATS = json.loads(Path("data/github_stats.json").read_text(encoding="utf-8"))


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, value, size=14, fill=TEXT, weight=400, family="mono", anchor="start", spacing=0):
    return f'<text x="{x}" y="{y}" class="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{esc(value)}</text>'


def rect(x, y, w, h, r=12, fill=PANEL, stroke=ROYAL, opacity=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-opacity=".75"/>'


def window(x, y, w, h, command, live=""):
    out = [rect(x, y, w, h, 18), f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="18" fill="#ffffff" fill-opacity=".025"/>',
           f'<path d="M{x} {y+40}H{x+w}" stroke="{VIOLET}" stroke-opacity=".22"/>']
    for i, color in enumerate((ROYAL, VIOLET, PINK)):
        out.append(f'<circle cx="{x+20+i*17}" cy="{y+20}" r="5" fill="{color}"/>')
    out.append(text(x+w/2, y+25, command, 11, LAV, 500, "mono", "middle"))
    if live:
        out.append(text(x+w-18, y+25, live, 9, VIOLET, 700, "mono", "end", 1.3))
    return out


parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Peyman Raad royal-purple animated GitHub profile preview</title>
<desc id="desc">Terminal-style profile with animated identity, build activity, evidence signals, technical stack, and selected repositories.</desc>
<defs>
  <linearGradient id="page" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0d1117"/><stop offset=".52" stop-color="#120922"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
  <linearGradient id="royal" x1="0" x2="1"><stop stop-color="#6d28d9"/><stop offset=".55" stop-color="#a78bfa"/><stop offset="1" stop-color="#f0abfc"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#7c3aed" stop-opacity=".36"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#c4b5fd" stroke-opacity=".035"/></pattern>
  <filter id="soft"><feGaussianBlur stdDeviation="22"/></filter>
</defs>
<style>
.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.sans{{font-family:Inter,Segoe UI,Arial,sans-serif}}
.glow{{filter:drop-shadow(0 0 5px rgba(192,132,252,.7))}}
</style>
<rect width="1200" height="1740" fill="url(#page)"/><rect width="1200" height="1740" fill="url(#grid)"/>
<circle cx="950" cy="230" r="290" fill="url(#glow)" filter="url(#soft)"/>
<rect x="0" y="0" width="1200" height="64" fill="#0d1117" stroke="#30363d"/>
<path d="M22 23h20v17H22zM32 23v17" fill="none" stroke="#8b949e" stroke-width="2"/>
{text(55,40,'README',16,TEXT,700,'sans')}
''']

# Identity terminal
parts += window(44, 96, 1112, 465, "peyman@github:~ $ whoami --royal", "SYSTEM ONLINE")
parts.append(f'<path d="M465 136V561" stroke="{VIOLET}" stroke-opacity=".22"/>')
parts.append(text(70, 171, "IDENTITY.ASCII / PEYMAN", 11, PINK, 700, "mono", spacing=1.4))
art = Path("assets/portrait.txt").read_text(encoding="utf-8").splitlines()
for i, line in enumerate(art):
    parts.append(f'<text x="70" y="{200+i*15}" class="mono glow" font-size="12" fill="{LAV}" opacity="0">{esc(line)}<animate attributeName="opacity" from="0" to="1" begin="{i*.055:.3f}s" dur=".22s" fill="freeze"/></text>')
parts += [text(70, 526, "AI_AGENT_ENGINEER", 10, MUTED, 500, "mono"), text(435, 526, "ROYAL/01", 10, MUTED, 500, "mono", "end")]

parts.append(text(505, 208, "PEYMAN", 61, TEXT, 850, "sans", spacing=6))
parts.append(f'<rect x="505" y="225" width="530" height="3" rx="2" fill="url(#royal)"><animate attributeName="width" from="0" to="530" dur="1.2s" fill="freeze"/></rect>')
parts.append(text(505, 262, "AI Agent & Automation Engineer", 21, LAV, 700, "sans"))
rows = [
    ("NOW", "Reliable agentic and automation systems"),
    ("BUILD", "Verified decisions → controlled actions"),
    ("STACK", "Python · SQL · n8n · FastAPI · Docker"),
    ("FOCUS", "Evaluation · guardrails · recovery · observability"),
    ("POLICY", "Proof over claims · no paid API dependency"),
]
for i, (key, value) in enumerate(rows):
    yy = 307 + i*39
    parts += [text(505, yy, key, 12, MUTED, 500, "mono"), text(600, yy, value, 13, "#e9d5ff", 500, "mono")]
parts.append(rect(505, 494, 384, 35, 17, "#241044", VIOLET))
parts.append(f'<circle cx="525" cy="511" r="5" fill="{PINK}" class="glow"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
parts.append(text(540, 516, "OPEN TO AI AGENT & AUTOMATION WORK", 10, LAV, 700, "mono", spacing=.8))

# Activity
parts.append(text(600, 590, "peyman@github ~ $ ./contributions.sh --royal", 11, LAV, 500, "mono", "middle"))
parts += window(44, 610, 1112, 320, "RECENT BUILD ACTIVITY / PUBLIC SIGNAL", "LIVE")
graph_days = {item["date"]: item for item in STATS["days"]}
today = date.fromisoformat(STATS["refreshed"])
start = min(date.fromisoformat(value) for value in graph_days)
month_positions = []
cursor = date(start.year, start.month, 1)
if cursor < start:
    cursor = date(cursor.year + (cursor.month == 12), 1 if cursor.month == 12 else cursor.month + 1, 1)
while cursor <= today:
    column = (cursor - start).days // 7
    if 0 <= column < 53:
        month_positions.append((column, cursor.strftime("%b").upper()))
    cursor = date(cursor.year + (cursor.month == 12), 1 if cursor.month == 12 else cursor.month + 1, 1)
for column, month in month_positions:
    parts.append(text(94+column*18, 681, month, 9, MUTED, 500, "mono"))
colors = ["#1d102d", "#32145c", "#542099", ROYAL, VIOLET, PINK]
for col in range(53):
    for row in range(7):
        current = start + timedelta(days=col*7+row)
        level = graph_days.get(current.isoformat(), {}).get("level", 0)
        x, y = 94+col*18, 704+row*20
        parts.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{colors[level]}" stroke="{VIOLET}" stroke-opacity=".08" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{.25+col*.018+row*.025:.3f}s" dur=".35s" fill="freeze"/></rect>')
parts += [text(94, 877, f'{STATS["contributions"]} contributions · {STATS["active_days"]} active days · best day {STATS["max_daily"]}', 11, "#b8afc7", 500, "mono"), text(1095, 877, "LESS  ◼ ◼ ◼ ◼ ◼  MORE", 10, LAV, 500, "mono", "end")]

# Profile signal
parts.append(text(600, 959, "peyman@github ~ $ signal --verified", 11, LAV, 500, "mono", "middle"))
parts += window(44, 980, 1112, 230, "PROFILE SIGNAL / REAL REPOSITORY EVIDENCE", "VERIFIED")
cards = [(str(STATS["public_repos"]), "PUBLIC REPOSITORIES", "Live GitHub portfolio"), (str(STATS["contributions"]), "CONTRIBUTIONS / 12 MONTHS", f'{STATS["active_days"]} active days'), (str(STATS["followers"]), "GITHUB FOLLOWERS", f'{STATS["following"]} following'), (str(STATS["stars"]), "TOTAL REPOSITORY STARS", f'Refreshed {STATS["refreshed"]}')]
for i, (num, label, sub) in enumerate(cards):
    x = 70+i*267
    parts += [rect(x, 1043, 246, 130, 14, PANEL_2, VIOLET), text(x+20, 1090, num, 34, TEXT, 800, "sans"), text(x+20, 1120, label, 10, MUTED, 600, "mono", spacing=.7), text(x+20, 1147, sub, 11, LAV, 600, "mono")]
    parts.append(f'<rect x="{x}" y="1170" width="0" height="3" fill="url(#royal)"><animate attributeName="width" values="0;246;246" keyTimes="0;.55;1" dur="3.4s" repeatCount="indefinite"/></rect>')

# Lower panels
parts.append(text(600, 1239, "peyman@github ~ $ inspect --stack --systems", 11, LAV, 500, "mono", "middle"))
parts += window(44, 1260, 540, 385, "CONTROL STACK / SYSTEM LAYERS", "CORE")
stack = [("PYTHON", .94, "CORE"), ("SQL / DATA", .86, "CORE"), ("AGENTS / RAG", .91, "FOCUS"), ("n8n / APIs", .88, "FOCUS"), ("DOCKER / CI", .78, "BUILD")]
for i, (name, val, kind) in enumerate(stack):
    y=1333+i*54
    parts += [text(70,y,name,11,"#c4b5fd",600,"mono"), f'<rect x="180" y="{y-11}" width="300" height="10" rx="5" fill="#211038"/>', f'<rect x="180" y="{y-11}" width="0" height="10" rx="5" fill="url(#royal)"><animate attributeName="width" from="0" to="{300*val:.0f}" begin="{i*.14:.2f}s" dur="1.4s" fill="freeze"/></rect>', text(548,y,kind,9,MUTED,600,"mono","end")]

parts += window(602, 1260, 554, 385, "COMMAND SYSTEMS / SELECTED WORK", "04")
repos = [
    ("Applied Agentic Systems", "State · SLA · recovery · local adapters", "AGENTS / RELIABILITY"),
    ("Evidence-First Data-to-Text Agent", "Deterministic KPIs · 24 tests · optional Ollama", "PYTHON / CI"),
    ("Agentic Automation Lab", "RAG · multi-agent · n8n infrastructure", "AUTOMATION / RAG"),
    ("Supply Chain Inventory Analytics", "Real UCI data · strict schema · 12 tests", "DATA / TESTS"),
]
for i,(name,desc,tags) in enumerate(repos):
    y=1320+i*73
    parts += [text(628,y,name,13,"#e9d5ff",700,"sans"), text(628,y+23,desc,10,MUTED,500,"mono"), text(1118,y+23,tags,9,VIOLET,600,"mono","end")]
    if i<3: parts.append(f'<path d="M628 {y+39}H1128" stroke="{VIOLET}" stroke-opacity=".16"/>')

parts += [text(600, 1681, "Data → Verified Facts → Decisions → Controlled Automation", 15, LAV, 700, "sans", "middle"), text(600, 1712, "LINKEDIN   ·   GITHUB SYSTEMS   ·   KAGGLE", 10, VIOLET, 700, "mono", "middle", 1.2), '</svg>']

Path("assets/royal-terminal.svg").write_text("".join(parts), encoding="utf-8")
