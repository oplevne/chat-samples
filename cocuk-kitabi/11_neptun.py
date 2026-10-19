"""Stop 11 — Neptune: the fastest winds, found by maths, Triton's geysers."""
import math, random
from kitap import S, W, star, dot, shuttle_side, zeytin_body, rock, svg_open, story_block, save


def arc_path(cx, cy, rx, ry, a0, a1, n=50):
    pts = [(cx + rx*math.cos(math.radians(a0 + (a1 - a0)*k/n)), cy + ry*math.sin(math.radians(a0 + (a1 - a0)*k/n))) for k in range(n + 1)]
    return 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def neptune(a, cx, cy, R, sw=1.0, rings=True, tilt=0.3):
    rnd = random.Random(7)
    RN = 24764.0
    ring_r = ((41900, 1.4, ''), (53200, 1.4, '5 5'), (62930, 2.0, ''))   # Galle, Le Verrier, Adams
    if rings:
        for r, w, dash in ring_r:
            a(f'<path d="{arc_path(cx, cy, r/RN*R, r/RN*R*tilt, 180, 360)}" fill="none" {S} stroke-width="{w*sw:.2f}" {"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>')
    a(f'<defs><clipPath id="n{cx}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    a(f'<g clip-path="url(#n{cx})">')
    Y = lambda lat: cy - R*math.sin(math.radians(lat))
    for lat in (-62, -45, 8, 30):       # faint darker bands
        w = R*math.cos(math.radians(lat)) + 10
        a(f'<path d="M {cx - w:.1f},{Y(lat):.1f} Q {cx:.1f},{Y(lat) + 8*sw:.1f} {cx + w:.1f},{Y(lat):.1f}" fill="none" {S} stroke-width="{1.6*sw:.2f}" stroke-dasharray="10 7"/>')
    for _ in range(9):                  # bright, streaky methane-ice cirrus clouds
        lat = rnd.choice((rnd.uniform(25, 45), rnd.uniform(-40, -25), rnd.uniform(-75, -60)))
        y = Y(lat); w = R*math.cos(math.radians(lat))
        x0 = cx + rnd.uniform(-0.8, 0.3)*w; L = w*rnd.uniform(0.25, 0.5)
        a(f'<path d="M {x0:.1f},{y:.1f} q {L/2:.1f},{-5*sw:.1f} {L:.1f},{2*sw:.1f} q {-L/2:.1f},{4*sw:.1f} {-L:.1f},{-2*sw:.1f} Z" fill="#fff" {S} stroke-width="{1.8*sw:.2f}"/>')
    # Great Dark Spot (~22 S) with bright companion clouds on its southern edge
    gx, gy = cx - R*0.18, Y(-22)
    a(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{R*0.2:.1f}" ry="{R*0.1:.1f}" fill="#fff" {S} stroke-width="{3.5*sw:.2f}"/>')
    a(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{R*0.11:.1f}" ry="{R*0.05:.1f}" fill="none" {S} stroke-width="{1.8*sw:.2f}"/>')
    a(f'<path d="M {gx - R*0.12:.1f},{gy + R*0.11:.1f} q {R*0.1:.1f},{-R*0.03:.1f} {R*0.24:.1f},{R*0.0:.1f} q {-R*0.1:.1f},{R*0.04:.1f} {-R*0.24:.1f},{0:.1f} Z" fill="#fff" {S} stroke-width="{2*sw:.2f}"/>')
    # "Scooter" and the small dark spot D2 with its bright core
    a(f'<path d="M {cx + R*0.1:.1f},{Y(-42):.1f} l {R*0.12:.1f},{-R*0.02:.1f} l {R*0.04:.1f},{R*0.04:.1f} Z" fill="#fff" {S} stroke-width="{2*sw:.2f}"/>')
    d2x, d2y = cx + R*0.35, Y(-55)
    a(f'<ellipse cx="{d2x:.1f}" cy="{d2y:.1f}" rx="{R*0.08:.1f}" ry="{R*0.045:.1f}" fill="#fff" {S} stroke-width="{2.5*sw:.2f}"/>')
    a(f'<ellipse cx="{d2x:.1f}" cy="{d2y:.1f}" rx="{R*0.025:.1f}" ry="{R*0.014:.1f}" fill="#fff" {S} stroke-width="{1.6*sw:.2f}"/>')
    a('</g>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" {S} stroke-width="{5*sw:.2f}"/>')
    if rings:
        for r, w, dash in ring_r:
            a(f'<path d="{arc_path(cx, cy, r/RN*R, r/RN*R*tilt, 0, 180)}" fill="none" {S} stroke-width="{w*sw:.2f}" {"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>')
        # the Adams ring arcs: Liberte, Egalite, Fraternite
        rr = 62930/RN*R
        for a0, a1 in ((35, 47), (52, 58), (63, 80)):
            a(f'<path d="{arc_path(cx, cy, rr, rr*tilt, a0, a1, 12)}" fill="none" {S} stroke-width="{6*sw:.2f}"/>')
            a(f'<path d="{arc_path(cx, cy, rr, rr*tilt, a0, a1, 12)}" fill="none" stroke="#fff" stroke-width="{2.5*sw:.2f}"/>')


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
CX, CY = 425, 345
neptune(a, CX, CY, 125)
# Triton's backward orbit, opposite to Neptune's spin
a(f'<ellipse cx="{CX}" cy="{CY}" rx="395" ry="150" fill="none" {S} stroke-width="2" stroke-dasharray="7 7"/>')
tx, ty = CX - 395*math.cos(math.radians(30)), CY + 150*math.sin(math.radians(30))
a(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="16" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<text x="{tx:.1f}" y="{ty + 38:.1f}" text-anchor="middle" font-family="DejaVu Sans" font-size="16" fill="#000">Triton</text>')
for ang0, sgn in ((60, -1),):     # Triton's arrow: clockwise as seen here
    x, y = CX + 395*math.cos(math.radians(ang0)), CY + 150*math.sin(math.radians(ang0))
    a(f'<path d="M {x + 12:.1f},{y - 14:.1f} L {x - 4:.1f},{y + 1:.1f} L {x + 18:.1f},{y + 8:.1f}" fill="none" {S} stroke-width="3.5"/>')
# Neptune's own spin arrow (counter-clockwise)
a(f'<path d="M {CX - 90},{CY - 150} Q {CX},{CY - 178} {CX + 90},{CY - 150}" fill="none" {S} stroke-width="3.5"/>')
a(f'<path d="M {CX + 72},{CY - 164} L {CX + 92},{CY - 149} L {CX + 68},{CY - 142}" fill="none" {S} stroke-width="3.5"/>')
shuttle_side(a, 'translate(600,600) rotate(-6) scale(0.24)', uid='r')
for sx, sy, r in ((80, 140, 14), (770, 120, 14), (60, 560, 12), (800, 420, 12)):
    star(a, sx, sy, r)
story_block(a, "Neptune, the Windy World", [
    "Neptune has the fastest winds in the Solar System, blowing at more than 2,000 kilometers per hour.",
    "It was the first planet found with math: in 1846, astronomers worked out where it had to be — and there it was!",
    "Its big moon Triton orbits backward, and its geysers shoot dark dust about 8 kilometers into the sky."],
    badge="4.5 billion km from the Sun")
save(o, 'sayfalar/11-neptun-sag.svg')

# ------------------------------------------------------------- left page ----
# Triton's south polar cap: nitrogen-ice geysers gushing ~8 km straight up;
# dark streaks of fallen dust lie on the ice.
o = svg_open(); a = o.append
neptune(a, 630, 200, 150, sw=1.1, rings=False)
HY = 520
a(f'<path d="M -10,{HY} Q 425,{HY - 20} 860,{HY} L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4.5"/>')
# two geysers gushing straight up: a column that widens as it rises, a billowy
# head at the top, and spray falling back on both sides
for gx, gy, top, s_ in ((230, 650, 150, 1.0), (590, 590, 405, 0.6)):
    n = 40
    left, right = [], []
    for k in range(n + 1):
        t = k / n
        y = gy - (gy - top)*t
        w = (6 + 26*t**1.4)*s_ * (1 + 0.18*abs(math.sin(k*0.9))*t)
        left.append((gx - w, y)); right.append((gx + w, y))
    wt = (6 + 26)*s_
    cap = [(gx - wt*math.cos(th)*(1 + 0.25*abs(math.sin(th*6))), top - wt*0.9*math.sin(th)*(1 + 0.25*abs(math.sin(th*6))))
           for th in (math.pi*k/14 for k in range(1, 14))]
    pts = left + cap + right[::-1]
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="2.8"/>')
    for dx in (-0.4, 0, 0.4):   # streaks rushing upward inside the jet
        a(f'<line x1="{gx + dx*8*s_:.1f}" y1="{gy - 20*s_:.1f}" x2="{gx + dx*24*s_:.1f}" y2="{top + 20*s_:.1f}" {S} stroke-width="1.5" stroke-dasharray="8 7"/>')
    for sgn in (-1, 1):         # spray falling back down
        for j in range(3):
            x0 = gx + sgn*(wt + 6*s_ + j*14*s_)
            a(f'<path d="M {x0:.0f},{top + 10*s_:.0f} q {sgn*18*s_:.0f},{40*s_:.0f} {sgn*(24 + j*10)*s_:.0f},{(120 + j*40)*s_:.0f}" fill="none" {S} stroke-width="1.5" stroke-dasharray="3 7"/>')
    a(f'<ellipse cx="{gx}" cy="{gy + 4*s_}" rx="{26*s_}" ry="{8*s_}" fill="#000"/>')
# dark wind streaks on the ice, all aligned with the wind
rnd = random.Random(4)
for _ in range(16):
    x, y = rnd.uniform(20, 800), rnd.uniform(560, 1060)
    L = rnd.uniform(60, 160) * (0.6 + (y - 520) / 900)
    w = 6 + (y - 520) / 40
    a(f'<path d="M {x:.0f},{y:.0f} q {L*0.5:.0f},{-w*0.6:.0f} {L:.0f},{-w*0.3:.0f} q {-L*0.5:.0f},{w:.0f} {-L:.0f},{w*0.3:.0f} Z" fill="#fff" {S} stroke-width="2.2"/>')
# "cantaloupe terrain" dimples near the horizon
for k in range(9):
    x = 40 + k*95 + rnd.uniform(-20, 20)
    a(f'<path d="M {x - 26:.0f},{HY + 20} q 26,{rnd.uniform(6, 10):.0f} 52,0" fill="none" {S} stroke-width="1.6"/>')
zeytin_body(a, 'tr', 'translate(690,1010) scale(0.6)')
shuttle_side(a, 'translate(335,445) rotate(-6) scale(0.25)', uid='l')
for sx, sy, r in ((380, 60, 14), (60, 360, 14), (800, 470, 12)):
    star(a, sx, sy, r)
save(o, 'sayfalar/11-neptun-sol.svg')
