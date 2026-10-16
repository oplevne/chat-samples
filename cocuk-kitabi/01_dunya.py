"""Stop 1 — Earth: magnetic shield, solar wind and auroras."""
import math
from kitap import S, W, star, dot, earth, projected_line, shuttle_side, svg_open, story_block, save


def aurora(a, pr, cx, cy, R, lat=66, sw=1.0, lon0=0, tall=0.06):
    """Projected auroral oval: curtain ribbons rising from `lat`, back side first."""
    py = pr(90, 0)[1]
    segs = []
    for start in range(0, 360, 60):
        lons = [start + k for k in range(0, 52, 2)]
        depth = sum(pr(lat, lo)[2] for lo in lons)
        segs.append((depth, lons))
    for _, lons in sorted(segs, key=lambda s: s[0]):
        bot, top = [], []
        for lo in lons:
            x0, y0, _ = pr(lat, lo)
            # tall curtains on the far side of the oval, where they rise into view;
            # a low ribbon on the near side so the land below stays readable
            w = 0.22 + 0.78 * min(1, max(0, (py - y0) / 0.08))
            h = 1.0 + tall * w * (1 + 0.45 * math.sin(math.radians(lo * 9)))
            x1, y1, _ = pr(lat, lo, h)
            bot.append((cx + R*x0, cy + R*y0)); top.append((cx + R*x1, cy + R*y1))
        poly = bot + top[::-1]
        a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in poly)}" fill="#fff" {S} stroke-width="{3*sw:.2f}"/>')
        for (xb, yb), (xt, yt) in list(zip(bot, top))[2:-1:3]:
            a(f'<line x1="{xb:.1f}" y1="{yb:.1f}" x2="{xt:.1f}" y2="{yt:.1f}" {S} stroke-width="{1.8*sw:.2f}"/>')


def swirl(a, x, y, r, sw=2.5):
    d = f'M {x+r},{y} A {r} {r*0.6} 0 1 0 {x},{y+r*0.6} A {r*0.6} {r*0.36} 0 1 0 {x+r*0.4},{y}'
    a(f'<path d="{d}" fill="none" {S} stroke-width="{sw}"/>')


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
a('<defs><clipPath id="scene"><rect x="0" y="0" width="850" height="690"/></clipPath></defs>')
a('<g transform="translate(21,12) scale(0.95)" clip-path="url(#scene)">')
CX, CY, R = 520, 350, 95
# Sun on the left edge
a(f'<circle cx="-70" cy="{CY}" r="160" fill="#fff" {S} stroke-width="5"/>')
for ang in range(-60, 61, 15):
    t = math.radians(ang)
    a(f'<line x1="{-70+180*math.cos(t):.1f}" y1="{CY+180*math.sin(t):.1f}" x2="{-70+215*math.cos(t):.1f}" y2="{CY+215*math.sin(t):.1f}" {S} stroke-width="4"/>')
# bow shock (quadratic) and solar-wind arrows that stop just before it
B0, B1, B2 = (780, 20), (-140, CY), (780, 680)
def bow(t):
    return ((1-t)**2*B0[0] + 2*t*(1-t)*B1[0] + t*t*B2[0], (1-t)**2*B0[1] + 2*t*(1-t)*B1[1] + t*t*B2[1])
a(f'<path d="M {B0[0]},{B0[1]} Q {B1[0]},{B1[1]} {B2[0]},{B2[1]}" fill="none" {S} stroke-width="3.5" stroke-dasharray="14 10"/>')
for yy in (150, 250, 350, 450, 550):
    t = min((k/400 for k in range(401)), key=lambda t: abs(bow(t)[1]-yy))
    xe = bow(t)[0] - 28
    xs = 165 if abs(yy-CY) < 150 else 130
    d = f'M {xs},{yy}'
    n = 4; step = (xe - xs) / n
    for i in range(n):
        d += f' q {step/2:.1f},{-10 if i%2 else 10} {step:.1f},0'
    a(f'<path d="{d}" fill="none" {S} stroke-width="3.5"/>')
    a(f'<path d="M {xe-14},{yy-9} L {xe+2},{yy} L {xe-14},{yy+9}" fill="none" {S} stroke-width="3.5"/>')
# magnetopause
a(f'<path d="M 860,105 C 560,105 372,220 372,{CY} C 372,480 560,595 860,595" fill="none" {S} stroke-width="4.5"/>')
# day-side closed field lines
for L in (1.28, 1.48):
    lam0 = math.acos(math.sqrt(1/L)); pts = []
    for i in range(61):
        lam = lam0 - 2*lam0*i/60; r = R*L*math.cos(lam)**2
        pts.append(f'{CX - r*math.cos(lam):.1f},{CY - r*math.sin(lam):.1f}')
    a(f'<polyline points="{" ".join(pts)}" fill="none" {S} stroke-width="3"/>')
# night-side lines stretched into the tail
for lamf, h in ((58, 55), (66, 115), (74, 175)):
    for sg in (1, -1):
        x0, y0 = CX + R*math.cos(math.radians(lamf))*0.9, CY - sg*R*math.sin(math.radians(lamf))
        a(f'<path d="M {x0:.1f},{y0:.1f} C {CX+R*0.7:.1f},{CY-sg*h*1.35:.1f} {CX+220},{CY-sg*h} 870,{CY-sg*h}" fill="none" {S} stroke-width="3"/>')
pr = earth(a, 'r', CX, CY, R, 25, 30, sw=0.8)
aurora(a, pr, CX, CY, R, sw=0.7)
x, y, _ = pr(41.0, 29.0); star(a, CX+R*x, CY+R*y, 8, sw=2.5)
shuttle_side(a, 'translate(668,352) scale(0.26)', uid='r')
for sx, sy, r in ((330, 60, 14), (150, 660, 14), (430, 668, 12), (300, 40, 0)):
    if r: star(a, sx, sy, r)
a('</g>')
story_block(a, "Earth’s Invisible Shield", [
    "Zeytin’s journey begins at home, on Earth, where a giant invisible magnetic shield surrounds our planet.",
    "The shield pushes away the solar wind — a stream of tiny charged particles that rushes from the Sun at about 400 kilometers every second.",
    "Near the North and South Poles, some particles slip in and make the air glow green and pink: the beautiful auroras!"],
    badge="Mission start: Earth")
save(o, 'sayfalar/01-dunya-sag.svg')

# ------------------------------------------------------------- left page ----
o = svg_open(); a = o.append
CX, CY, R = 425, 735, 305
# field lines leaving the polar regions
for sg in (-1, 1):
    for k, (dx, top) in enumerate(((150, 330), (240, 250), (330, 170))):
        x0 = CX + sg*(40 + 25*k); y0 = CY - R*0.78
        a(f'<path d="M {x0},{y0:.0f} C {x0+sg*dx*0.3:.0f},{top-60} {CX+sg*(dx+120)},{top-40} {CX+sg*(dx+260)},{top+120}" fill="none" {S} stroke-width="3.5"/>')
pr = earth(a, 'l', CX, CY, R, 45, 30, sw=1.0)
aurora(a, pr, CX, CY, R, sw=1.0, tall=0.11)
x, y, _ = pr(41.0, 29.0); star(a, CX+R*x, CY+R*y, 14)
# Moon, next stop
a(f'<circle cx="725" cy="115" r="55" fill="#fff" {S} stroke-width="4.5"/>')
for mx, my, mr in ((705, 95, 12), (745, 130, 9), (720, 140, 6), (750, 92, 7)):
    a(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#fff" {S} stroke-width="3"/>')
shuttle_side(a, 'translate(120,232) rotate(-8) scale(0.9)', uid='l')
for sx, sy, r in ((80, 70, 22), (300, 60, 16), (560, 60, 20), (790, 300, 18), (60, 400, 18), (620, 30, 0), (800, 520, 16), (50, 560, 14)):
    if r: star(a, sx, sy, r)
for sx, sy in ((200, 140), (440, 40), (600, 200), (700, 380), (140, 480)):
    dot(a, sx, sy, 5)
save(o, 'sayfalar/01-dunya-sol.svg')
