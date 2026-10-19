"""Stop 4 — Mercury: Caloris basin, scorching days, icy polar craters."""
import math, random
from kitap import (S, W, star, dot, ortho, _dest, cratered_globe, shuttle_side, zeytin_body, rock,
                   svg_open, story_block, save)

MERCURY_KM = 2440
CAL = (31.5, 162.7, 1550)      # Caloris basin (MESSENGER): centre lat, lon E, diameter km
APOLLODORUS = (30.7, 163.0)    # small crater at the hub of Pantheon Fossae

# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
CX, CY, R = 400, 350, 265
# the Sun just off the right edge, lighting Mercury from that side
a(f'<circle cx="1010" cy="{CY}" r="230" fill="#fff" {S} stroke-width="5"/>')
for ang in range(140, 221, 16):
    t = math.radians(ang)
    a(f'<line x1="{1010+250*math.cos(t):.1f}" y1="{CY+250*math.sin(t):.1f}" x2="{1010+285*math.cos(t):.1f}" y2="{CY+285*math.sin(t):.1f}" {S} stroke-width="4"/>')
named = [(27.3, 119.1, 263, True, False), (30.7, 163.0, 41, False, False)]
pr = cratered_globe(a, 'r', CX, CY, R, 20, 160, MERCURY_KM, named=named, n=1400, seed=4, sw=0.85,
                    sun=(0, 160 + 75), basins=[CAL], min_px=5, min_km=45, max_km=300,
                    smooth=[(CAL[0], CAL[1], CAL[2] / 2 / (2*math.pi*MERCURY_KM/360))])
# Pantheon Fossae: radial troughs around Apollodorus, inside Caloris
for b in range(0, 360, 12):
    p0 = pr(*_dest(*APOLLODORUS, 0.9, b)); p1 = pr(*_dest(*APOLLODORUS, 0.9 + 4.5 * (0.6 + 0.4 * ((b * 7) % 5) / 4), b))
    a(f'<line x1="{CX+R*p0[0]:.1f}" y1="{CY+R*p0[1]:.1f}" x2="{CX+R*p1[0]:.1f}" y2="{CY+R*p1[1]:.1f}" {S} stroke-width="1.6"/>')
shuttle_side(a, 'translate(70,640) rotate(-10) scale(0.24)', uid='r')
for sx, sy, r in ((60, 120, 14), (120, 420, 12), (690, 660, 14), (720, 80, 12)):
    star(a, sx, sy, r)
story_block(a, "Mercury, Hot and Cold", [
    "Mercury is the closest planet to the Sun, and one year there lasts only 88 Earth days.",
    "In the daytime its ground heats up to about 430°C, hot enough to melt lead, but at night it drops to about −180°C.",
    "Yet inside craters near its poles, where sunlight never reaches, scientists have found ice!"],
    badge="58 million km from the Sun")
save(o, 'sayfalar/04-merkur-sag.svg')

# ------------------------------------------------------------- left page ----
# On the rim of a north-polar crater: the Sun sits on the horizon, about
# three times wider than it looks from Earth, and never shines into the crater.
o = svg_open(); a = o.append
HY = 430
a(f'<circle cx="150" cy="{HY+20}" r="125" fill="#fff" {S} stroke-width="5"/>')
for ang in range(185, 356, 17):
    t = math.radians(ang)
    a(f'<line x1="{150+140*math.cos(t):.1f}" y1="{HY+20+140*math.sin(t):.1f}" x2="{150+175*math.cos(t):.1f}" y2="{HY+20+175*math.sin(t):.1f}" {S} stroke-width="4"/>')
# horizon with distant crater rims
a(f'<path d="M -10,{HY} L 90,{HY-6} Q 130,{HY-30} 175,{HY-8} L 330,{HY-4} Q 380,{HY-40} 450,{HY-36} Q 520,{HY-42} 560,{HY-6} L 700,{HY-2} Q 760,{HY-24} 860,{HY-12} L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4.5"/>')
# the polar crater: rim, terraced inner wall, permanently shadowed floor
CXc, CYc, RX, RY = 430, 690, 395, 175
FX, FY, FRX, FRY = 430, 735, 285, 105          # crater floor
a(f'<defs><clipPath id="bowl"><ellipse cx="{CXc}" cy="{CYc}" rx="{RX}" ry="{RY}"/></clipPath>'
  f'<pattern id="shade" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
  f'<line x1="0" y1="0" x2="0" y2="10" stroke="#000" stroke-width="1.8"/></pattern></defs>')
# raised, lumpy outer rim
rnd = random.Random(8)
rim = [(CXc + (RX + 24 + rnd.uniform(-6, 10))*math.cos(2*math.pi*k/48), CYc + (RY + 16 + rnd.uniform(-4, 6))*math.sin(2*math.pi*k/48)) for k in range(48)]
a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in rim)}" fill="#fff" {S} stroke-width="3"/>')
# the whole bowl lies in permanent shadow ...
a(f'<ellipse cx="{CXc}" cy="{CYc}" rx="{RX}" ry="{RY}" fill="url(#shade)" {S} stroke-width="5"/>')
a('<g clip-path="url(#bowl)">')
# ... except the upper part of the far wall, facing the low Sun
E = lambda cx, cy, rx, ry, t: (cx + rx*math.cos(t), cy + ry*math.sin(t))
ts = [math.radians(d) for d in range(-170, -9, 4)]
upper = [E(CXc, CYc, RX, RY, t) for t in ts]
lower = [E(CXc, CYc - 20, RX*0.86, RY*0.62, t) for t in ts]
a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in upper + lower[::-1])}" fill="#fff" {S} stroke-width="2.5"/>')
for (x0, y0), (x1, y1) in list(zip(upper, lower))[1::2]:   # gullies down the wall
    a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{(x0+x1)/2:.1f}" y2="{(y0+y1)/2+4:.1f}" {S} stroke-width="1.6"/>')
a('</g>')
# crater floor and its water-ice deposits
a(f'<ellipse cx="{FX}" cy="{FY}" rx="{FRX}" ry="{FRY}" fill="none" {S} stroke-width="3"/>')
def snowflake(x, y, r):
    d = ' '.join(f'M {x - r*math.cos(t):.1f},{y - r*math.sin(t):.1f} L {x + r*math.cos(t):.1f},{y + r*math.sin(t):.1f}' for t in (0, math.pi/3, 2*math.pi/3))
    a(f'<path d="{d}" fill="none" {S} stroke-width="2"/>')
for ix, iy, ir in ((330, 740, 75), (500, 765, 80), (250, 790, 40), (560, 710, 42), (420, 700, 38)):
    pts = [(ix + ir*rnd.uniform(0.8, 1.1)*math.cos(2*math.pi*k/14), iy + ir*0.38*rnd.uniform(0.8, 1.1)*math.sin(2*math.pi*k/14)) for k in range(14)]
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="2.8"/>')
    for k in range(2 if ir > 50 else 1):
        snowflake(ix + (k - 0.5) * ir * 0.8 if ir > 50 else ix, iy, 8)
# foreground rim, rocks, Zeytin pointing at the ice
for k, (rx, ry, rr) in enumerate(((70, 960, 30), (300, 1000, 22), (520, 975, 18), (800, 1030, 28), (170, 1060, 16))):
    rock(a, rx, ry, rr, seed=20 + k)
zeytin_body(a, 'm', 'translate(690,1000) scale(0.72)')
shuttle_side(a, 'translate(470,150) rotate(-6) scale(0.5)', uid='l')
save(o, 'sayfalar/04-merkur-sol.svg')
