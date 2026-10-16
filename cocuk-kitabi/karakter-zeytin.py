"""Character page: meet Zeytin, the space cat."""
import math, sys
from kitap import S, star, dot, zeytin_head, shuttle_side

W, H = 850, 1100
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')

for cx, cy, r in [(80, 90, 24), (180, 210, 16), (760, 100, 26), (680, 230, 16), (90, 420, 20), (780, 470, 18), (130, 620, 14), (720, 640, 20), (420, 60, 0)]:
    if r: star(a, cx, cy, r)
for cx, cy in [(250, 80), (600, 70), (60, 300), (800, 330), (40, 560), (810, 590), (330, 740), (520, 750)]:
    dot(a, cx, cy, 5)

HX, HY, HR = 425, 345, 190
# spacesuit body
a(f'<path d="M 295,520 C 230,545 195,600 190,700 L 660,700 C 655,600 620,545 555,520 Z" fill="#fff" {S} stroke-width="5"/>')
a(f'<rect x="335" y="585" width="70" height="44" rx="6" fill="#fff" {S} stroke-width="3.5"/>')
for x in (352, 370, 388):
    a(f'<circle cx="{x}" cy="607" r="5" fill="#fff" {S} stroke-width="3"/>')
# olive badge
a(f'<circle cx="505" cy="605" r="30" fill="#fff" {S} stroke-width="4"/>')
a(f'<ellipse cx="498" cy="610" rx="11" ry="15" transform="rotate(-25 498 610)" fill="#fff" {S} stroke-width="3"/>')
a(f'<path d="M 506,596 Q 515,585 525,590 Q 518,600 506,596 Z" fill="#fff" {S} stroke-width="2.5"/>')
# helmet glass + head
a(f'<circle cx="{HX}" cy="{HY}" r="{HR}" fill="#fff" {S} stroke-width="5"/>')
zeytin_head(a, 'big', f'translate({HX},{HY+28}) scale(0.92)')
# glare strip
def arc(r, a0, a1):
    return (HX + r*math.cos(math.radians(a0)), HY + r*math.sin(math.radians(a0)),
            HX + r*math.cos(math.radians(a1)), HY + r*math.sin(math.radians(a1)))
x0, y0, x1, y1 = arc(175, 196, 220); x2, y2, x3, y3 = arc(162, 220, 196)
a(f'<path d="M {x0:.1f},{y0:.1f} A 175 175 0 0 1 {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f} A 162 162 0 0 0 {x3:.1f},{y3:.1f} Z" fill="#fff" {S} stroke-width="3"/>')
# antenna
a(f'<line x1="{HX}" y1="{HY-HR}" x2="{HX}" y2="{HY-HR-40}" {S} stroke-width="4"/>')
star(a, HX, HY - HR - 52, 16)
# collar ring
a(f'<ellipse cx="{HX}" cy="528" rx="140" ry="26" fill="#fff" {S} stroke-width="5"/>')
# name banner
a(f'<rect x="255" y="655" width="340" height="72" rx="14" fill="#fff" {S} stroke-width="5"/>')
a(f'<text x="{W/2}" y="711" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="54" fill="#fff" stroke="#000" stroke-width="2.4" stroke-linejoin="round">ZEYTIN</text>')

shuttle_side(a, 'translate(165,870) scale(0.92)')

for i, line in enumerate(["Hi! I'm Zeytin, a fluffy space cat.", "My name means “olive” in Turkish. Hop aboard my shuttle,",
                          "and let's explore the Solar System together!"]):
    a(f'<text x="{W/2}" y="{998+i*31}" text-anchor="middle" font-family="DejaVu Sans" font-size="23" fill="#000">{line}</text>')
a('</svg>')
open(sys.argv[1], 'w').write('\n'.join(o))
