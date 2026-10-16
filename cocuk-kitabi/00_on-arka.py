"""Front and back matter: title page, owner page, and 'design your own planet'."""
import math
from kitap import S, W, star, dot, shuttle_side, zeytin_body, svg_open, save

# ------------------------------------------------------------ title page ----
o = svg_open(); a = o.append
for sx, sy, r in ((90, 90, 22), (760, 80, 18), (420, 50, 14), (70, 470, 16), (790, 440, 20), (120, 980, 18), (740, 1000, 22), (420, 1040, 14)):
    star(a, sx, sy, r)
for sx, sy in ((180, 600), (680, 620), (300, 1000), (560, 980)):
    dot(a, sx, sy, 5)
a(f'<text x="{W/2}" y="220" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="92" fill="#fff" stroke="#000" stroke-width="3.2" stroke-linejoin="round">ZEYTIN</text>')
a(f'<text x="{W/2}" y="310" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="60" fill="#fff" stroke="#000" stroke-width="2.6" stroke-linejoin="round">IN SPACE</text>')
a(f'<text x="{W/2}" y="370" text-anchor="middle" font-family="DejaVu Sans" font-size="26" fill="#000">A Coloring Journey Through the Solar System</text>')
a(f'<text x="{W/2}" y="420" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="28" fill="#000">by Olcay Plevne</text>')
zeytin_body(a, 'title', 'translate(440,850) scale(1.2)')
shuttle_side(a, 'translate(130,930) rotate(-6) scale(0.55)', uid='title')
save(o, 'sayfalar/00a-baslik.svg')

# ------------------------------------------------------------ owner page ----
o = svg_open(); a = o.append
a(f'<rect x="120" y="230" width="610" height="420" rx="30" fill="#fff" {S} stroke-width="5"/>')
a(f'<text x="{W/2}" y="330" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="46" fill="#fff" stroke="#000" stroke-width="2.2" stroke-linejoin="round">This book belongs to</text>')
a(f'<line x1="190" y1="480" x2="660" y2="480" {S} stroke-width="3"/>')
a(f'<text x="{W/2}" y="560" text-anchor="middle" font-family="DejaVu Sans" font-size="22" fill="#000">Space cadet, age</text>')
a(f'<line x1="355" y1="600" x2="495" y2="600" {S} stroke-width="3"/>')
for sx, sy, r in ((150, 150, 20), (700, 140, 24), (420, 110, 14), (170, 760, 16), (690, 780, 20)):
    star(a, sx, sy, r)
note = ["Tip: colored pencils and crayons work best;", "markers may show through the paper."]
for i, line in enumerate(note):
    a(f'<text x="{W/2}" y="{880 + i*30}" text-anchor="middle" font-family="DejaVu Sans" font-size="19" fill="#000">{line}</text>')
a(f'<text x="{W/2}" y="1030" text-anchor="middle" font-family="DejaVu Sans" font-size="16" fill="#000">Text and illustrations \u00a9 2026 Olcay Plevne. All rights reserved.</text>')
save(o, 'sayfalar/00b-sahip.svg')

# ------------------------------------------------------ design a planet ----
o = svg_open(); a = o.append
a(f'<text x="{W/2}" y="110" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="48" fill="#fff" stroke="#000" stroke-width="2.4" stroke-linejoin="round">Design Your Own Planet!</text>')
a(f'<circle cx="{W/2}" cy="440" r="260" fill="#fff" {S} stroke-width="5" stroke-dasharray="18 12"/>')
for i, q in enumerate(("My planet is called", "Is it hot or cold?", "How many moons does it have?", "Who lives there?")):
    y = 790 + i*70
    a(f'<text x="110" y="{y}" font-family="DejaVu Sans" font-size="22" fill="#000">{q}</text>')
    a(f'<line x1="{110 + len(q)*12.8:.0f}" y1="{y + 4}" x2="740" y2="{y + 4}" {S} stroke-width="2.5"/>')
shuttle_side(a, 'translate(40,190) rotate(-8) scale(0.2)', uid='own')
save(o, 'sayfalar/99-gezegenini-tasarla.svg')
