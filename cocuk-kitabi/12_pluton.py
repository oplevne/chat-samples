"""Stop 12 — Pluto: the heart, a five-hour sunbeam, Charon's dance."""
import math, random
import numpy as np
from scipy.spatial import Voronoi
from kitap import S, W, star, dot, ortho, _dest, shuttle_side, zeytin_body, paw_print, svg_open, story_block, save

PLUTO_KM = 1188
KPD = 2*math.pi*PLUTO_KM/360


def poly(a, pts, w=3, fill='#fff', extra=''):
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" {S} stroke-width="{w}" {extra}/>')


def local(lat0, lon0, u_km, v_km):
    """Point u km east and v km north of (lat0, lon0) on Pluto."""
    d = math.hypot(u_km, v_km) / KPD
    b = math.degrees(math.atan2(u_km, v_km))
    return _dest(lat0, lon0, d, b)


def heart_pts(n=80):
    """Classic heart curve, scaled to ~1600 km wide; point at the bottom."""
    out = []
    for k in range(n):
        t = 2*math.pi*k/n
        x = 16*math.sin(t)**3
        y = 13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
        out.append((x*50, y*50 - 100))
    return out


def pluto(a, cx, cy, R, sw=1.0):
    pr = ortho(15, 180)
    P = lambda la, lo: (cx + R*pr(la, lo)[0], cy + R*pr(la, lo)[1])
    a(f'<defs><clipPath id="pl{cx}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    a(f'<g clip-path="url(#pl{cx})">')
    # Cthulhu Macula: the long dark region along the equator, west of the heart
    rnd = random.Random(3)
    cth = []
    for k in range(30):
        lo = 70 + 85*k/29
        cth.append((-5 + 14*math.sin(k/4) + rnd.uniform(-2, 2), lo))
    for k in range(30):
        lo = 155 - 85*k/29
        cth.append((-30 + 6*math.sin(k/3) + rnd.uniform(-2, 2), lo))
    poly(a, [P(la, lo) for la, lo in cth], 3*sw)
    # Tombaugh Regio, the heart, centred near 20 N, 180 E, tilted a little
    hc = (22, 180)
    hp = [local(*hc, x*math.cos(0.3) - y*math.sin(0.3), x*math.sin(0.3) + y*math.cos(0.3)) for x, y in heart_pts()]
    poly(a, [P(la, lo) for la, lo in hp], 3.5*sw)
    # Sputnik Planitia: the smooth nitrogen-ice western lobe, with convection cells
    sp_c = local(*hc, -380, 80)
    sp = [local(*sp_c, 330*math.cos(t)*(1 + 0.06*math.sin(5*t)), 470*math.sin(t)*(1 + 0.05*math.cos(4*t))) for t in (2*math.pi*k/40 for k in range(40))]
    sp_xy = [P(la, lo) for la, lo in sp]
    poly(a, sp_xy, 2.8*sw)
    a(f'<defs><clipPath id="sp{cx}"><polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in sp_xy)}"/></clipPath></defs>')
    a(f'<g clip-path="url(#sp{cx})">')
    pts = np.array([P(*local(*sp_c, rnd.uniform(-360, 360), rnd.uniform(-500, 500))) for _ in range(70)])
    vor = Voronoi(pts)
    for i, reg in enumerate(vor.point_region):
        region = vor.regions[reg]
        if -1 in region or not region:
            continue
        cell = [vor.vertices[k] for k in region]
        a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in cell)}" fill="none" {S} stroke-width="{1.3*sw:.2f}"/>')
    a('</g>')
    # water-ice mountains along the heart's western edge, and a few craters elsewhere
    for k in range(6):
        la, lo = local(*sp_c, -360 + rnd.uniform(-40, 10), -350 + k*130)
        x, y = P(la, lo)
        a(f'<path d="M {x - 9*sw:.1f},{y + 5*sw:.1f} L {x:.1f},{y - 9*sw:.1f} L {x + 9*sw:.1f},{y + 5*sw:.1f} Z" fill="#fff" {S} stroke-width="{2*sw:.2f}"/>')
    for _ in range(20):
        la, lo = rnd.uniform(-50, 60), rnd.uniform(100, 260)
        if abs(la - 22) < 25 and abs(lo - 180) < 30:
            continue
        x, y, v = pr(la, lo)
        if v:
            r = rnd.uniform(4, 11)*sw
            a(f'<ellipse cx="{cx + R*x:.1f}" cy="{cy + R*y:.1f}" rx="{r:.1f}" ry="{r*0.8:.1f}" fill="#fff" {S} stroke-width="{1.6*sw:.2f}"/>')
    a('</g>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" {S} stroke-width="{5*sw:.2f}"/>')


def charon(a, cx, cy, R, sw=1.0):
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{4*sw:.2f}"/>')
    # Mordor Macula: the dark reddish cap at Charon's north pole
    a(f'<path d="M {cx - R*0.6:.1f},{cy - R*0.78:.1f} Q {cx:.1f},{cy - R*0.45:.1f} {cx + R*0.62:.1f},{cy - R*0.76:.1f}" fill="none" {S} stroke-width="{2.4*sw:.2f}"/>')
    a(f'<path d="M {cx - R*0.95:.1f},{cy + R*0.1:.1f} Q {cx:.1f},{cy + R*0.25:.1f} {cx + R*0.95:.1f},{cy + R*0.05:.1f}" fill="none" {S} stroke-width="{1.6*sw:.2f}" stroke-dasharray="6 5"/>')
    for dx, dy, r in ((-0.3, 0.5, 0.1), (0.35, 0.35, 0.07), (0.1, -0.1, 0.06)):
        a(f'<circle cx="{cx + R*dx:.1f}" cy="{cy + R*dy:.1f}" r="{R*r:.1f}" fill="#fff" {S} stroke-width="{1.6*sw:.2f}"/>')


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
pluto(a, 390, 360, 240)
charon(a, 735, 175, 58)
# Pluto and Charon both circle a point in empty space between them
a(f'<path d="M 640,300 Q 700,270 720,250" fill="none" {S} stroke-width="2" stroke-dasharray="6 6"/>')
a(f'<circle cx="660" cy="285" r="5" fill="#fff" {S} stroke-width="2.5"/>')
shuttle_side(a, 'translate(600,620) rotate(-8) scale(0.24)', uid='r')
for sx, sy, r in ((80, 130, 14), (60, 560, 12), (800, 420, 12), (420, 60, 12)):
    star(a, sx, sy, r)
story_block(a, "Pluto Has a Heart", [
    "Pluto is a dwarf planet so far away that sunlight takes about five and a half hours to reach it.",
    "In 2015, the New Horizons spacecraft found a giant heart on Pluto: its left half is a plain of frozen nitrogen.",
    "Its moon Charon is half as wide as Pluto, so the two spin around a point in space between them, like dancers holding hands."],
    badge="5.9 billion km from the Sun")
save(o, 'sayfalar/12-pluton-sag.svg')

# ------------------------------------------------------------- left page ----
# On Sputnik Planitia: nitrogen-ice cells, water-ice mountains, layered blue haze,
# Charon hanging still in the sky, and the far-away Sun looking like a bright star.
o = svg_open(); a = o.append
HY = 560
for k, y in enumerate((HY - 30, HY - 70, HY - 115, HY - 165)):     # haze layers
    a(f'<path d="M -10,{y} Q 425,{y - 30 + k*4} 860,{y}" fill="none" {S} stroke-width="1.6" stroke-dasharray="{14 - k*2} {8 + k*2}"/>')
charon(a, 600, 210, 95, sw=1.1)
sx_, sy_ = 180, 150   # the Sun: just a very bright point of light
a(f'<circle cx="{sx_}" cy="{sy_}" r="7" fill="#fff" {S} stroke-width="3"/>')
for k in range(8):
    t = 2*math.pi*k/8
    L = 26 if k % 2 == 0 else 15
    a(f'<line x1="{sx_ + 11*math.cos(t):.1f}" y1="{sy_ + 11*math.sin(t):.1f}" x2="{sx_ + L*math.cos(t):.1f}" y2="{sy_ + L*math.sin(t):.1f}" {S} stroke-width="2.2"/>')
# blocky water-ice mountains on the horizon
mts = [(-10, HY), (40, HY - 60), (90, HY - 150), (150, HY - 120), (200, HY - 190), (260, HY - 70), (300, HY - 20), (360, HY - 5), (860, HY - 2), (860, HY + 5), (-10, HY + 5)]
poly(a, mts, 4)
for x0, y0, x1, y1 in ((90, HY - 150, 110, HY - 40), (200, HY - 190, 230, HY - 60), (150, HY - 120, 160, HY - 40)):
    a(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" {S} stroke-width="2"/>')
# nitrogen-ice plain: convection cells in perspective, divided by troughs
a(f'<rect x="-10" y="{HY}" width="870" height="{1110 - HY}" fill="#fff" {S} stroke-width="4"/>')
def to_screen(u, v):
    v = max(v, 0.0)
    s = 0.3 + 0.7 * v
    return 425 + (u - 0.5) * 1500 * s, HY + 540 * v ** 1.25
rng = np.random.default_rng(4)
pts = rng.uniform([-0.15, -0.02], [1.15, 1.05], size=(130, 2))
vor = Voronoi(pts)
a(f'<defs><clipPath id="plain"><rect x="0" y="{HY}" width="850" height="{1100 - HY}"/></clipPath></defs>')
a('<g clip-path="url(#plain)">')
for i, reg in enumerate(vor.point_region):
    region = vor.regions[reg]
    if -1 in region or not region:
        continue
    cell = [vor.vertices[k] for k in region]
    cu, cv = np.mean(cell, axis=0)
    cell = [(cu + (x - cu)*0.9, cv + (y - cv)*0.9) for x, y in cell]   # leave a trough between cells
    scr = [to_screen(x, y) for x, y in cell]
    if max(y for _, y in scr) - min(y for _, y in scr) < 8:
        continue
    poly(a, scr, 2.4)
a('</g>')
zeytin_body(a, 'pl', 'translate(640,1000) scale(0.6)')
for k, (px, py) in enumerate(((560, 1050), (530, 1030), (500, 1055), (470, 1035))):
    paw_print(a, px, py, 0.8, rot=-80)
shuttle_side(a, 'translate(330,360) rotate(-6) scale(0.32)', uid='l')
save(o, 'sayfalar/12-pluton-sol.svg')
