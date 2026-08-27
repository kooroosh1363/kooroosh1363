#!/usr/bin/env python3
"""Generate a GitHub-safe animated royal-purple terminal profile preview."""

import json
from datetime import date, timedelta
from pathlib import Path

W, H = 1200, 1550
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
<desc id="desc">Terminal-style profile with an animated PR agent network, live build activity, evidence signals, and technical stack.</desc>
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
<rect width="{W}" height="{H}" fill="url(#page)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
<circle cx="950" cy="230" r="290" fill="url(#glow)" filter="url(#soft)"/>
<rect x="0" y="0" width="1200" height="64" fill="#0d1117" stroke="#30363d"/>
<path d="M22 23h20v17H22zM32 23v17" fill="none" stroke="#8b949e" stroke-width="2"/>
{text(55,40,'README',16,TEXT,700,'sans')}
''']

# Identity terminal
parts += window(44, 96, 1112, 465, "peyman@github:~ $ whoami --royal", "SYSTEM ONLINE")
parts.append(f'<path d="M465 136V561" stroke="{VIOLET}" stroke-opacity=".22"/>')
parts.append(text(70, 171, "IDENTITY.NODE / PR", 11, PINK, 700, "mono", spacing=1.4))
# A brand mark is more stable and recruiter-friendly than a low-resolution
# portrait. Only internal nodes and packets animate; the panel never moves.
cx, cy = 252, 337
nodes = [(112, 220), (180, 190), (324, 190), (396, 236), (410, 372), (340, 455), (166, 460), (96, 378)]
for index, (nx, ny) in enumerate(nodes):
    parts.append(f'<path d="M{cx} {cy}L{nx} {ny}" stroke="{VIOLET}" stroke-opacity=".42" stroke-width="1.5" stroke-dasharray="5 8"><animate attributeName="stroke-dashoffset" from="0" to="-52" dur="{4.3+index*.22:.2f}s" repeatCount="indefinite"/></path>')
parts.append(f'<circle cx="{cx}" cy="{cy}" r="111" fill="#1b0a35" stroke="{ROYAL}" stroke-width="2"/>')
parts.append(f'<circle cx="{cx}" cy="{cy}" r="94" fill="none" stroke="{VIOLET}" stroke-opacity=".62" stroke-width="2" stroke-dasharray="4 10"><animate attributeName="stroke-dashoffset" from="0" to="-84" dur="8s" repeatCount="indefinite"/></circle>')
parts.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="#2b1050" stroke="{PINK}" stroke-opacity=".72"/>')
parts.append(text(cx, cy+27, "PR", 74, TEXT, 850, "sans", "middle", 3))
parts.append(text(cx, cy+53, "AGENTIC SYSTEMS", 9, LAV, 700, "mono", "middle", 1.5))
for index, (nx, ny) in enumerate(nodes):
    parts.append(f'<circle cx="{nx}" cy="{ny}" r="5" fill="{PINK if index % 3 == 0 else VIOLET}" class="glow"><animate attributeName="r" values="4;7;4" begin="{index*.18:.2f}s" dur="2.8s" repeatCount="indefinite"/></circle>')
for index, (nx, ny) in enumerate(nodes[::2]):
    parts.append(f'<circle r="3.5" fill="{LAV}" class="glow"><animateMotion path="M{nx} {ny}L{cx} {cy}" begin="{index*.65:.2f}s" dur="2.6s" repeatCount="indefinite"/></circle>')
parts += [text(70, 526, "ROYAL_AGENT_NETWORK", 10, MUTED, 500, "mono"), text(435, 526, "PR/ONLINE", 10, MUTED, 500, "mono", "end")]

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
# Animated scanner travels beneath the real heatmap without changing panel layout.
parts.append(f'<path d="M94 850H1048" stroke="{VIOLET}" stroke-opacity=".24" stroke-dasharray="3 8"/>')
parts.append(f'<g class="glow"><path d="M85 857L94 840L103 857L94 853Z" fill="{PINK}" stroke="{LAV}"/><animateTransform attributeName="transform" type="translate" from="0 0" to="954 0" dur="8s" repeatCount="indefinite"/></g>')
parts.append(text(1095, 854, "ROYAL COMMIT SCANNER", 8, VIOLET, 700, "mono", "end", 1))
live_windows = [("TODAY", STATS["today_count"]), ("LAST 7 DAYS", STATS["last_7_days"]), ("LAST 30 DAYS", STATS["last_30_days"]), ("LAST 12 MONTHS", STATS["contributions"])]
for index, (label, value) in enumerate(live_windows):
    x = 94 + index * 250
    parts.append(text(x, 882, label, 9, MUTED, 600, "mono", spacing=.7))
    parts.append(text(x, 908, str(value), 21, LAV, 800, "sans"))
parts.append(text(1095, 908, "LESS  ◼ ◼ ◼ ◼ ◼  MORE", 9, VIOLET, 600, "mono", "end"))

# Profile signal
parts.append(text(600, 959, "peyman@github ~ $ signal --verified", 11, LAV, 500, "mono", "middle"))
parts += window(44, 980, 1112, 230, "PROFILE SIGNAL / REAL REPOSITORY EVIDENCE", "VERIFIED")
cards = [(str(STATS["public_repos"]), "PUBLIC REPOSITORIES", "Live GitHub portfolio"), (str(STATS["contributions"]), "CONTRIBUTIONS / 12 MONTHS", f'{STATS["active_days"]} active days'), (str(STATS["followers"]), "GITHUB FOLLOWERS", f'{STATS["following"]} following'), (str(STATS["stars"]), "TOTAL REPOSITORY STARS", f'Refreshed {STATS["refreshed"]}')]
for i, (num, label, sub) in enumerate(cards):
    x = 70+i*267
    parts += [rect(x, 1043, 246, 130, 14, PANEL_2, VIOLET), text(x+20, 1090, num, 34, TEXT, 800, "sans"), text(x+20, 1120, label, 10, MUTED, 600, "mono", spacing=.7), text(x+20, 1147, sub, 11, LAV, 600, "mono")]
    parts.append(f'<rect x="{x}" y="1170" width="0" height="3" fill="url(#royal)"><animate attributeName="width" values="0;246;246" keyTimes="0;.55;1" dur="3.4s" repeatCount="indefinite"/></rect>')

# Technical control stack. Clickable project cards are rendered as independent
# SVG files and linked directly from README below this main panel.
parts.append(text(600, 1239, "peyman@github ~ $ inspect --stack", 11, LAV, 500, "mono", "middle"))
parts += window(44, 1260, 1112, 205, "CONTROL STACK / SYSTEM LAYERS", "CORE")
stack = [("PYTHON", .94, "CORE"), ("SQL / DATA", .86, "CORE"), ("AGENTS / RAG", .91, "FOCUS"), ("n8n / APIs", .88, "FOCUS"), ("DOCKER / CI", .78, "BUILD")]
for i, (name, val, kind) in enumerate(stack):
    x = 72 + i * 215
    parts += [text(x,1329,name,10,"#c4b5fd",650,"mono"), f'<rect x="{x}" y="1350" width="175" height="10" rx="5" fill="#211038"/>', f'<rect x="{x}" y="1350" width="{175*val:.0f}" height="10" rx="5" fill="url(#royal)"><animate attributeName="width" from="0" to="{175*val:.0f}" begin="{i*.14:.2f}s" dur="1.4s" fill="freeze"/></rect>', text(x,1390,kind,9,MUTED,600,"mono")]

parts += [text(600, 1500, "Data → Verified Facts → Decisions → Controlled Automation", 15, LAV, 700, "sans", "middle"), text(600, 1528, "CLICKABLE COMMAND SYSTEMS BELOW", 10, VIOLET, 700, "mono", "middle", 1.2), '</svg>']

Path("assets/royal-terminal.svg").write_text("".join(parts), encoding="utf-8")


def project_card(number: str, title: str, description: str, evidence: str, tags: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="190" viewBox="0 0 560 190" role="img" aria-label="{esc(title)} — open repository">
<defs><linearGradient id="bg" x1="0" x2="1"><stop stop-color="#10071f"/><stop offset="1" stop-color="#1d0b37"/></linearGradient><linearGradient id="accent" x1="0" x2="1"><stop stop-color="#6d28d9"/><stop offset=".55" stop-color="#a78bfa"/><stop offset="1" stop-color="#f0abfc"/></linearGradient></defs>
<rect width="560" height="190" rx="18" fill="url(#bg)" stroke="#7c3aed"/>
<rect width="560" height="38" rx="18" fill="#ffffff" fill-opacity=".025"/><path d="M0 38H560" stroke="#a78bfa" stroke-opacity=".22"/>
<circle cx="20" cy="19" r="5" fill="#7c3aed"/><circle cx="37" cy="19" r="5" fill="#a78bfa"/><circle cx="54" cy="19" r="5" fill="#f0abfc"/>
{text(280,24,'COMMAND SYSTEM / '+number,10,LAV,600,'mono','middle',1)}
{text(528,24,'OPEN ↗',9,PINK,700,'mono','end',1)}
{text(24,78,title,20,TEXT,800,'sans')}
{text(24,106,description,11,MUTED,500,'mono')}
{text(24,133,evidence,10,LAV,600,'mono')}
<rect x="24" y="151" width="{max(108, len(tags)*7)}" height="24" rx="12" fill="#2b1050" stroke="#a78bfa" stroke-opacity=".55"/>
{text(36,167,tags,9,VIOLET,700,'mono',spacing=.8)}
<rect x="0" y="187" width="0" height="3" fill="url(#accent)"><animate attributeName="width" values="0;560;560" keyTimes="0;.55;1" dur="3.8s" repeatCount="indefinite"/></rect>
</svg>'''


project_cards = [
    ("assets/project-applied-agentic-systems.svg", "01", "Applied Agentic Systems", "Business-process agents with state, SLA handling, and recovery", "Deterministic validation · Docker paths · explicit maturity", "AGENTS / RELIABILITY"),
    ("assets/project-data-to-text-agent.svg", "02", "Evidence-First Data-to-Text Agent", "Local CSV and JSON reporting with deterministic KPI calculation", "24 tests · Python 3.11–3.13 CI · optional Ollama", "PYTHON / CI"),
    ("assets/project-agentic-automation-lab.svg", "03", "Agentic Automation Lab", "Progressive RAG, multi-agent, data, and n8n systems", "Importable artifacts · project docs · maturity labels", "AUTOMATION / RAG"),
    ("assets/project-supply-chain-analytics.svg", "04", "Supply Chain Inventory Analytics", "Defensible SKU prioritization using real UCI logistics data", "Strict schema checks · 12 tests · live-source validation", "DATA / TESTS"),
]
for path, number, title, description, evidence, tags in project_cards:
    Path(path).write_text(project_card(number, title, description, evidence, tags), encoding="utf-8")
