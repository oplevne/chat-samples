"""Stop 3 — the Sun: sunspots, magnetic loops, granulation."""
import math, random
import numpy as np
from scipy.spatial import Voronoi
from kitap import S, W, star, dot, ortho, _dest, shuttle_side, svg_open, story_block, save


def blob(cx, cy, r, rnd, n=14, jit=0.25):
    return [(cx + r*(1+rnd.uniform(-jit, jit))*math.cos(2*math.pi*k/n),
             cy + r*(1+rnd.uniform(-jit, jit))*math.sin(2*math.pi*k/n)) for k in range(n)]


def poly(a, pts, w=3, fill='#fff', extra=''):
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" {S} stroke-width="{w}" {extra}/>')


def tube(a, d, w_out, w_in):
    """A plasma loop drawn as an outlined tube (colourable inside)."""
    a(f'<path d="{d}" fill="none" {S} stroke-width="{w_out}"/>')
    a(f'<path d="{d}" fill="none" stroke="#fff" stroke-linecap="round" stroke-width="{w_in}"/>')


def disk_spot(a, pr, cx, cy, R, lat, lon, size, rnd):
    """Sunspot on the projected disk: irregular penumbra with radial filaments + umbra."""
    P = lambda la, lo: (cx + R*pr(la, lo)[0], cy + R*pr(la, lo)[1])
    n = 18
    pen = [P(*_dest(lat, lon, size*rnd.uniform(0.85, 1.15), 360*k/n)) for k in range(n)]
    um = [P(*_dest(lat, lon, size*0.45*rnd.uniform(0.8, 1.2), 360*k/n)) for k in range(n)]
    poly(a, pen, 2.5)
    for (x0, y0), (x1, y1) in zip(um, pen):
        a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" {S} stroke-width="1.2"/>')
    poly(a, um, 2.5, fill='#000')


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
CX, CY, R = 470, 360, 285
rnd = random.Random(5)
# prominences on the limb, drawn first so the disk covers their feet
def limb(ang, extra=0):
    t = math.radians(ang)
    return CX + (R + extra)*math.cos(t), CY + (R + extra)*math.sin(t)
# limb prominences as seen in H-alpha: ragged flame-like sheets of plasma
pr_rnd = random.Random(12)
for ang, h, spread in ((-38, 62, 13), (204, 48, 15), (115, 30, 8), (-118, 26, 7)):
    n = 24
    base, outer, strands = [], [], []
    for k in range(n + 1):
        t = k / n
        th = math.radians(ang - spread + 2*spread*t)
        env = math.sin(math.pi * t) ** 0.7
        hh = h * env * pr_rnd.uniform(0.6, 1.15)
        base.append((CX + (R - 6)*math.cos(th), CY + (R - 6)*math.sin(th)))
        outer.append((CX + (R + hh)*math.cos(th), CY + (R + hh)*math.sin(th)))
        if k % 4 == 2:
            strands.append((th, hh))
    poly(a, base + outer[::-1], 3.5)
    for th, hh in strands:
        a(f'<path d="M {CX + R*math.cos(th):.1f},{CY + R*math.sin(th):.1f} Q {CX + (R + hh*0.5)*math.cos(th + 0.012):.1f},{CY + (R + hh*0.5)*math.sin(th + 0.012):.1f} {CX + (R + hh*0.85)*math.cos(th - 0.01):.1f},{CY + (R + hh*0.85)*math.sin(th - 0.01):.1f}" fill="none" {S} stroke-width="1.5"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#fff" {S} stroke-width="5"/>')
pr = ortho(7, 0)  # solar B0 angle ~7 degrees
# sunspot groups only in the two activity belts (about 10-30 degrees N and S)
for lat, lon, sizes in ((18, -30, (2.6, 1.4, 0.9)), (24, 20, (1.8, 1.0)), (-14, -5, (3.2, 1.6, 1.1, 0.8)),
                        (-22, 45, (1.6, 1.0)), (12, 58, (1.4,)), (-9, -55, (1.2, 0.8))):
    for k, sz in enumerate(sizes):
        disk_spot(a, pr, CX, CY, R, lat + rnd.uniform(-1.5, 1.5), lon + k*5.5, sz*1.4, rnd)
# faculae (bright patches near the limb) as small dotted outlines
for lat, lon in ((20, -70), (-18, 72), (26, 75), (-24, -75)):
    pts = [(CX + R*pr(*_dest(lat, lon, 3, b))[0], CY + R*pr(*_dest(lat, lon, 3, b))[1]) for b in range(0, 360, 30)]
    poly(a, pts, 1.8, extra='stroke-dasharray="3 5"')
# Earth to scale (the Sun is 109 times wider)
ex, ey = 95, 300
a(f'<circle cx="{ex}" cy="{ey}" r="{R/109:.1f}" fill="#fff" {S} stroke-width="1.5"/>')
a(f'<path d="M {ex},{ey+8} L {ex},{ey+28}" fill="none" {S} stroke-width="2"/>')
a(f'<text x="{ex}" y="{ey+48}" text-anchor="middle" font-family="DejaVu Sans" font-size="17" fill="#000">Earth,</text>')
a(f'<text x="{ex}" y="{ey+68}" text-anchor="middle" font-family="DejaVu Sans" font-size="17" fill="#000">to scale</text>')
shuttle_side(a, 'translate(70,640) rotate(-12) scale(0.24)', uid='r')
for sx, sy, r in ((60, 130, 14), (800, 680, 14), (810, 420, 12)):
    star(a, sx, sy, r)
story_block(a, "Our Star, the Sun", [
    "Zeytin flies toward the Sun, a giant ball of glowing gas so big that about 1.3 million Earths could fit inside it.",
    "Its dark spots are sunspots: they look dark only because they are about 1,500 degrees cooler than the bright gas around them.",
    "Above the spots, magnetic loops of hot plasma arch into space, so tall that many Earths could fit beneath them!"],
    badge="150 million km from Earth")
save(o, 'sayfalar/03-gunes-sag.svg')

# ------------------------------------------------------------- left page ----
# Close-up of a sunspot near the limb: granulation in perspective, loops above
o = svg_open(); a = o.append
HY = 470                     # limb / horizon
def to_screen(u, v):         # plane (u across, v toward viewer) -> page
    v = max(v, 0.0)
    s = 0.35 + 0.65 * v
    return 425 + (u - 0.5) * 1500 * s, HY + 640 * v ** 1.35
SU, SV, SR = 0.5, 0.55, 0.14   # spot centre and penumbra radius in plane units
rng = np.random.default_rng(2)
pts = rng.uniform([-0.1, -0.02], [1.1, 1.05], size=(1100, 2))
vor = Voronoi(pts)
a('<defs><clipPath id="surf"><rect x="0" y="%d" width="850" height="%d"/></clipPath></defs>' % (HY, 1100 - HY))
a('<g clip-path="url(#surf)">')
a(f'<rect x="0" y="{HY}" width="850" height="{1100-HY}" fill="#fff"/>')
for i, reg in enumerate(vor.point_region):
    region = vor.regions[reg]
    if -1 in region or not region:
        continue
    u, v = pts[i]
    du, dv = (u - SU) / 1.0, (v - SV) / 0.75
    if math.hypot(du, dv) < SR * 1.15:
        continue
    cell = [vor.vertices[k] for k in region]
    # shrink cells a little: the dark lanes between granules
    cu, cv = np.mean(cell, axis=0)
    cell = [(cu + (x - cu) * 0.82, cv + (y - cv) * 0.82) for x, y in cell]
    scr = [to_screen(x, y) for x, y in cell]
    if max(y for _, y in scr) - min(y for _, y in scr) < 9:   # too small to colour near the limb
        continue
    poly(a, scr, 1.6)
# the sunspot (circular on the surface, foreshortened by the perspective)
r2 = random.Random(9)
pen, um = [], []
for k in range(40):
    t = 2*math.pi*k/40
    rp = SR * r2.uniform(0.92, 1.08); ru = SR * 0.45 * r2.uniform(0.85, 1.15)
    pen.append(to_screen(SU + rp*math.cos(t), SV + rp*0.75*math.sin(t)))
    um.append(to_screen(SU + ru*math.cos(t), SV + ru*0.75*math.sin(t)))
poly(a, pen, 3.5)
for (x0, y0), (x1, y1) in zip(um, pen):
    a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" {S} stroke-width="1.6"/>')
    a(f'<line x1="{(x0*2+x1)/3:.1f}" y1="{(y0*2+y1)/3:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" {S} stroke-width="1"/>')
poly(a, um, 3, fill='#000')
a('</g>')
a(f'<path d="M 0,{HY+18} Q 425,{HY-22} 850,{HY+18}" fill="none" {S} stroke-width="5"/>')
# arcade of magnetic loops rooted on both sides of the spot
# loops join the spot to opposite-polarity patches: thin strands, staggered in depth
for k, (u1, v1, u2, v2, h) in enumerate(((0.36, 0.50, 0.70, 0.60, 300), (0.38, 0.47, 0.76, 0.52, 360),
                                          (0.40, 0.44, 0.82, 0.46, 410), (0.33, 0.56, 0.64, 0.70, 250),
                                          (0.42, 0.42, 0.88, 0.40, 440))):
    x1, y1 = to_screen(u1, v1); x2, y2 = to_screen(u2, v2)
    top = min(y1, y2) - h
    tube(a, f'M {x1:.1f},{y1:.1f} C {x1 - 20:.1f},{top:.1f} {x2 + 20:.1f},{top:.1f} {x2:.1f},{y2:.1f}', 15, 8)
# a quiescent prominence arching over the limb at the left, made of twisted strands
for dx, sk in ((0, 0), (16, 18), (32, -14)):
    tube(a, f'M {30+dx},{HY+12} C {10+dx},{HY-200+sk} {120+dx},{HY-290} {170+dx},{HY-250+sk} '
            f'C {220+dx},{HY-210} {250+dx},{HY-120-sk} {260+dx},{HY+8}', 13, 7)
shuttle_side(a, 'translate(560,70) scale(0.42)', uid='l')
save(o, 'sayfalar/03-gunes-sol.svg')
