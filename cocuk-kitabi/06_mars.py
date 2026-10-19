"""Stop 6 — Mars: Olympus Mons, Valles Marineris, blue sunsets."""
import math, random
from kitap import (S, W, star, dot, ortho, _dest, cratered_globe, shuttle_side, zeytin_body, rock,
                   svg_open, story_block, save)

MARS_KM = 3390
KPD = 2 * math.pi * MARS_KM / 360

# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
CX, CY, R = 425, 350, 270
LAT0, LON0 = 22, -95
pr = cratered_globe(a, 'r', CX, CY, R, LAT0, LON0, MARS_KM, n=1600, seed=6, sw=0.85, min_px=4, min_km=60, max_km=260,
                    smooth=[(5, -110, 28), (55, -100, 38), (-8, -65, 10)])
P = lambda la, lo: (CX + R*pr(la, lo)[0], CY + R*pr(la, lo)[1])
def ring(lat, lon, km, jitter=0.0, seed=0, step=10):
    rnd = random.Random(seed)
    return [P(*_dest(lat, lon, km/2/KPD*(1 + rnd.uniform(-jitter, jitter)), b)) for b in range(0, 360, step)]
def poly(pts, w=3, extra=''):
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="{w}" {extra}/>')
a(f'<defs><clipPath id="md"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath></defs>')
a('<g clip-path="url(#md)">')
# north polar cap with its spiral troughs
cap = [P(*_dest(90, 0, 8 + 1.5*math.sin(math.radians(b*3)), b)) for b in range(0, 360, 6)]
poly(cap, 3)
for b0 in range(0, 360, 72):
    pts = [P(*_dest(90, 0, 1 + 6*t, b0 + 160*t)) for t in (k/12 for k in range(13))]
    a(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" {S} stroke-width="1.8"/>')
# Tharsis shield volcanoes: base scarp/flank outline plus nested calderas
for name, lat, lon, base_km, cal_km in (('Olympus Mons', 18.65, -133.8, 620, 85), ('Ascraeus Mons', 11.8, -104.5, 460, 55),
                                         ('Pavonis Mons', 1.5, -112.9, 375, 47), ('Arsia Mons', -8.3, -120.1, 435, 110),
                                         ('Alba Mons', 40.5, -109.6, 900, 60)):
    if name == 'Alba Mons':
        a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ring(lat, lon, base_km, 0.08, 1))}" fill="none" {S} stroke-width="2" stroke-dasharray="8 6"/>')
    else:
        poly(ring(lat, lon, base_km, 0.06, hash(name) % 100), 3.2)
        poly(ring(lat, lon, base_km*0.55, 0.05, 7), 1.6)
    if name != 'Alba Mons':   # radial lava-flow ridges on the flanks
        for b in range(0, 360, 20):
            p0 = P(*_dest(lat, lon, base_km*0.3/KPD, b)); p1 = P(*_dest(lat, lon, base_km*0.48/KPD, b + 4))
            a(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" {S} stroke-width="1.3"/>')
    poly(ring(lat, lon, cal_km, 0.1, 3, step=20), 2.4)
    poly(ring(lat + 0.3, lon + 0.3, cal_km*0.5, 0.1, 4, step=30), 1.8)
# Valles Marineris: main chasma + a parallel branch, Noctis Labyrinthus maze at the west end
def canyon(cl, widths):
    north = [P(*_dest(la, lo, w, 0)) for (la, lo), w in zip(cl, widths)]
    south = [P(*_dest(la, lo, w, 180)) for (la, lo), w in zip(cl, widths)]
    poly(north + south[::-1], 3)
    for (la, lo), w in list(zip(cl, widths))[1:-1]:  # wall gullies
        x0, y0 = P(*_dest(la, lo, w, 0)); x1, y1 = P(*_dest(la, lo, w*0.4, 0))
        a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" {S} stroke-width="1.4"/>')
canyon([(-6.5, -88), (-7, -82), (-8.5, -76), (-10, -70), (-12, -64), (-13, -58), (-12, -52), (-9, -47), (-6, -42), (-3, -38)],
       [0.6, 1.0, 1.6, 2.3, 2.6, 2.4, 2.0, 1.6, 1.2, 0.8])
canyon([(-4, -78), (-4.5, -72), (-5.5, -66), (-6, -61)], [0.4, 0.8, 0.9, 0.5])
rnd = random.Random(2)
for _ in range(18):
    la, lo = rnd.uniform(-10, -4), rnd.uniform(-104, -90)
    p0 = P(la, lo); p1 = P(*_dest(la, lo, rnd.uniform(0.8, 1.8), rnd.choice((0, 60, 120, 90))))
    a(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" {S} stroke-width="1.8"/>')
a('</g>')
a(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" {S} stroke-width="5"/>')
# Mars' two tiny moons
for mx, my, rx, ry, rot in ((745, 120, 26, 18, 20), (90, 560, 16, 11, -15)):
    a(f'<ellipse cx="{mx}" cy="{my}" rx="{rx}" ry="{ry}" transform="rotate({rot} {mx} {my})" fill="#fff" {S} stroke-width="3.5"/>')
    a(f'<circle cx="{mx-rx*0.3:.0f}" cy="{my-ry*0.1:.0f}" r="{ry*0.35:.0f}" fill="#fff" {S} stroke-width="2"/>')
shuttle_side(a, 'translate(640,650) rotate(-8) scale(0.24)', uid='r')
for sx, sy, r in ((70, 110, 14), (790, 380, 12), (60, 360, 12)):
    star(a, sx, sy, r)
story_block(a, "Mars, the Red Planet", [
    "On Mars, Zeytin finds Olympus Mons, the tallest volcano in the Solar System: about 22 kilometers high, more than twice the height of Mount Everest.",
    "The canyon Valles Marineris is about 4,000 kilometers long, nearly ten times longer than the Grand Canyon.",
    "Rusty iron makes the dust red — and at sunset, the sky around the Sun turns blue!"],
    badge="228 million km from the Sun")
save(o, 'sayfalar/06-mars-sag.svg')

# ------------------------------------------------------------- left page ----
# Sunset in Gale crater: Curiosity, Mount Sharp's layers, and a blue glow
# around a Sun that looks only about two-thirds as wide as from Earth.
o = svg_open(); a = o.append
HY = 560
SX, SY = 600, 380
for r_, dash in ((200, '3 12'), (140, '6 10'), (90, '10 8')):   # the blue glow around the setting Sun
    a(f'<circle cx="{SX}" cy="{SY}" r="{r_}" fill="none" {S} stroke-width="2" stroke-dasharray="{dash}"/>')
a(f'<circle cx="{SX}" cy="{SY}" r="22" fill="#fff" {S} stroke-width="4"/>')
# Mount Sharp (Aeolis Mons) with its sedimentary layers
# a broad layered mound: gentle lower slopes, steeper terraced upper part, lumpy top
prof = [(-10, HY), (40, HY-20), (110, HY-45), (170, HY-80), (215, HY-120), (240, HY-160), (262, HY-185),
        (285, HY-196), (305, HY-188), (322, HY-200), (342, HY-192), (365, HY-165), (395, HY-130),
        (430, HY-95), (480, HY-60), (540, HY-35), (620, HY-18), (860, HY-8), (860, HY+5), (-10, HY+5)]
a(f'<polygon points="{" ".join(f"{x},{y}" for x, y in prof)}" fill="#fff" {S} stroke-width="4"/>')
def mx(yy, side):    # x of the mountain profile at height yy on the left/right flank
    pts = prof[:9] if side < 0 else prof[10:18]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if min(y0, y1) <= yy <= max(y0, y1) and y0 != y1:
            return x0 + (yy - y0) * (x1 - x0) / (y1 - y0)
    return None
for yy in range(HY - 175, HY - 8, 17):
    xl, xr = mx(yy, -1), mx(yy, 1)
    if xl is not None and xr is not None:
        a(f'<path d="M {xl + 6:.0f},{yy} Q {(xl + xr)/2:.0f},{yy - 5} {xr - 6:.0f},{yy}" fill="none" {S} stroke-width="1.6"/>')
# ground
a(f'<path d="M -10,{HY} C 200,{HY+10} 500,{HY-8} 860,{HY+6} L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4"/>')
# wheel track behind the rover; the tread holes spell "J P L" in Morse code
TY = 930
a(f'<rect x="-10" y="{TY - 16}" width="{420 - 230 + 10}" height="30" fill="#fff" {S} stroke-width="2.5"/>')
morse = '.---  .--.  .-..  '   # J P L
x = 0
for ch in morse * 3:
    if x > 170:
        break
    if ch == '.':
        a(f'<rect x="{x}" y="{TY - 5}" width="7" height="7" fill="#fff" {S} stroke-width="1.6"/>'); x += 13
    elif ch == '-':
        a(f'<rect x="{x}" y="{TY - 5}" width="18" height="7" fill="#fff" {S} stroke-width="1.6"/>'); x += 24
    else:
        x += 6
for xx in range(4, 185, 9):
    a(f'<line x1="{xx}" y1="{TY - 15}" x2="{xx + 4}" y2="{TY - 9}" {S} stroke-width="1.2"/>')
# Curiosity, side view
CXr, GY = 420, 930
for wx in (CXr - 190, CXr - 40, CXr + 110):
    a(f'<circle cx="{wx}" cy="{GY - 40}" r="42" fill="#fff" {S} stroke-width="5"/>')
    a(f'<circle cx="{wx}" cy="{GY - 40}" r="16" fill="#fff" {S} stroke-width="3"/>')
    for k in range(8):
        t = 2*math.pi*k/8
        a(f'<line x1="{wx + 30*math.cos(t):.1f}" y1="{GY - 40 + 30*math.sin(t):.1f}" x2="{wx + 40*math.cos(t):.1f}" y2="{GY - 40 + 40*math.sin(t):.1f}" {S} stroke-width="2.5"/>')
# rocker-bogie suspension
a(f'<path d="M {CXr-190},{GY-40} L {CXr-120},{GY-110} L {CXr-40},{GY-40} M {CXr-120},{GY-110} L {CXr+20},{GY-130} L {CXr+110},{GY-40}" fill="none" {S} stroke-width="7"/>')
a(f'<path d="M {CXr-190},{GY-40} L {CXr-120},{GY-110} L {CXr-40},{GY-40} M {CXr-120},{GY-110} L {CXr+20},{GY-130} L {CXr+110},{GY-40}" fill="none" stroke="#fff" stroke-width="2.5"/>')
# body
a(f'<path d="M {CXr-200},{GY-215} L {CXr+140},{GY-215} L {CXr+150},{GY-150} L {CXr-190},{GY-150} Z" fill="#fff" {S} stroke-width="5"/>')
a(f'<line x1="{CXr-195}" y1="{GY-175}" x2="{CXr+145}" y2="{GY-175}" {S} stroke-width="2.5"/>')
# RTG power source with cooling fins at the back
a(f'<path d="M {CXr-200},{GY-200} L {CXr-275},{GY-235} L {CXr-290},{GY-205} L {CXr-215},{GY-170} Z" fill="#fff" {S} stroke-width="4"/>')
for k in range(5):
    x = CXr - 215 - k*15
    a(f'<line x1="{x}" y1="{GY-172-k*7}" x2="{x+10}" y2="{GY-198-k*7}" {S} stroke-width="2"/>')
# high-gain antenna disk and remote-sensing mast with its camera head
a(f'<ellipse cx="{CXr-60}" cy="{GY-232}" rx="42" ry="10" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<line x1="{CXr-60}" y1="{GY-222}" x2="{CXr-60}" y2="{GY-215}" {S} stroke-width="4"/>')
a(f'<rect x="{CXr+95}" y="{GY-385}" width="16" height="172" fill="#fff" {S} stroke-width="4"/>')
a(f'<rect x="{CXr+65}" y="{GY-435}" width="80" height="52" rx="6" fill="#fff" {S} stroke-width="4.5"/>')
a(f'<circle cx="{CXr+135}" cy="{GY-409}" r="12" fill="#fff" {S} stroke-width="3"/>')
for k in range(2):
    a(f'<rect x="{CXr+78+k*24}" y="{GY-405}" width="14" height="14" rx="2" fill="#fff" {S} stroke-width="2.5"/>')
# robotic arm folded at the front
a(f'<path d="M {CXr+150},{GY-170} L {CXr+215},{GY-150} L {CXr+190},{GY-95}" fill="none" {S} stroke-width="11"/>')
a(f'<path d="M {CXr+150},{GY-170} L {CXr+215},{GY-150} L {CXr+190},{GY-95}" fill="none" stroke="#fff" stroke-width="5"/>')
a(f'<rect x="{CXr+168}" y="{GY-100}" width="44" height="34" rx="5" fill="#fff" {S} stroke-width="3.5"/>')
# Zeytin watching the sunset, plus rocks
zeytin_body(a, 'm', 'translate(735,1015) scale(0.62)', wave=False)
for k, (rx, ry, rr) in enumerate(((60, 1000, 30), (210, 1060, 18), (560, 1050, 22), (90, 720, 16), (700, 690, 20), (800, 790, 14))):
    rock(a, rx, ry, rr, seed=40 + k)
shuttle_side(a, 'translate(80,120) rotate(-6) scale(0.38)', uid='l')
save(o, 'sayfalar/06-mars-sol.svg')
