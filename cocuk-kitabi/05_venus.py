"""Stop 5 — Venus: crushing air, the hottest surface, a backward spin."""
import math, random
from kitap import S, W, star, dot, shuttle_side, rock, svg_open, story_block, save


def poly(a, pts, w=3, fill='#fff', extra=''):
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" {S} stroke-width="{w}" {extra}/>')


def cloud_puffs(a, x0, x1, y, r, rnd, w=4):
    """A row of cumulus-like bumps along a cloud deck top edge."""
    d = f'M {x0},{y}'
    x = x0
    while x < x1:
        rr = r * rnd.uniform(0.6, 1.2)
        d += f' a {rr:.1f},{rr*0.8:.1f} 0 0 1 {2*rr:.1f},0'
        x += 2*rr
    return d


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
CX, CY, R = 470, 365, 255
a(f'<defs><clipPath id="vd"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath></defs>')
a(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#fff" {S} stroke-width="5"/>')
a('<g clip-path="url(#vd)">')
# the sideways "Y" seen in ultraviolet: two dark arms meeting near the equator
# on the morning side, with a dark equatorial stem; streaky bands follow them
def arm(sign):
    top, bot = [], []
    for k in range(41):
        t = k / 40
        x = CX + R*0.42 - t*R*1.6
        y = CY + sign*(14 + (t ** 1.5) * R * 0.8)
        th = 18 + 34*t + 6*math.sin(t*11 + sign)
        top.append((x, y - th/2)); bot.append((x, y + th/2))
    return top + bot[::-1]
poly(a, arm(-1), 3)
poly(a, arm(1), 3)
stem_top = [(CX + R*0.38 + t*R*0.8, CY - 16 - 10*t + 4*math.sin(t*12)) for t in (k/20 for k in range(21))]
stem_bot = [(CX + R*0.38 + t*R*0.8, CY + 16 + 10*t + 4*math.sin(t*12 + 1)) for t in (k/20 for k in range(21))]
poly(a, [(CX + R*0.3, CY)] + stem_top + stem_bot[::-1], 3)
for sign in (-1, 1):
    for off in (60, 120, 185):
        pts = []
        for k in range(31):
            t = k / 30
            x = CX + R*0.75 - t*R*1.9
            y = CY + sign*(off*0.7 + (t ** 1.3) * R * 0.7 + off*0.3)
            pts.append(f'{x:.1f},{y + 5*math.sin(t*9 + off):.1f}')
        a(f'<polyline points="{" ".join(pts)}" fill="none" {S} stroke-width="2"/>')
# cold polar collars
for sign in (-1, 1):
    a(f'<ellipse cx="{CX}" cy="{CY + sign*R*0.86:.1f}" rx="{R*0.48:.1f}" ry="{R*0.12:.1f}" fill="none" {S} stroke-width="2.5" stroke-dasharray="10 7"/>')
a('</g>')
a(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" {S} stroke-width="5"/>')
# spin arrow: Venus turns the "wrong" way (east to west)
a(f'<path d="M {CX+120},{CY-R-24} Q {CX},{CY-R-56} {CX-120},{CY-R-24}" fill="none" {S} stroke-width="4"/>')
a(f'<path d="M {CX-102},{CY-R-40} L {CX-122},{CY-R-23} L {CX-96},{CY-R-18}" fill="none" {S} stroke-width="4"/>')
shuttle_side(a, 'translate(60,640) rotate(-10) scale(0.24)', uid='r')
for sx, sy, r in ((80, 140, 14), (100, 430, 12), (810, 660, 14), (800, 40, 0)):
    if r: star(a, sx, sy, r)
story_block(a, "Venus, the Upside-Down Oven", [
    "Venus hides under thick clouds of sulfuric acid, and its air is so heavy that standing there would feel like being 900 meters deep in the sea.",
    "Its carbon dioxide air traps heat, so the ground is about 465°C — hotter than Mercury!",
    "Venus also spins backward, and one slow turn takes 243 Earth days, longer than its 225-day year."],
    badge="108 million km from the Sun")
save(o, 'sayfalar/05-venus-sag.svg')

# ------------------------------------------------------------- left page ----
# Cross-section: clear sky above the cloud tops, the cloud deck, and the
# surface photographed by Venera 13 in 1982.
o = svg_open(); a = o.append
rnd = random.Random(21)
shuttle_side(a, 'translate(230,105) rotate(-4) scale(0.55)', uid='l')
# cloud deck: puffy top edge, a few layered bands, ragged base
a(f'<path d="{cloud_puffs(a, -20, 880, 330, 38, rnd)} L 880,470 L -20,470 Z" fill="#fff" {S} stroke-width="4"/>')
for y in (370, 410):
    a(f'<path d="{cloud_puffs(a, -20, 880, y, 30, rnd)}" fill="none" {S} stroke-width="2.5"/>')
base = 'M -20,470 ' + ' '.join(f'L {x},{470 + rnd.uniform(-8, 14):.0f}' for x in range(0, 881, 40))
a(f'<path d="{base}" fill="none" {S} stroke-width="3"/>')
# haze lines below the clouds
for y in (520, 560):
    a(f'<path d="M -10,{y} ' + ' '.join(f'Q {x+25},{y-6} {x+50},{y}' for x in range(-10, 860, 50)) + '" fill="none" stroke="#000" stroke-width="1.4" stroke-dasharray="6 10"/>')
# horizon and Maat Mons, a giant shield volcano about 8 km high
HY = 640
a(f'<path d="M -10,{HY} L 300,{HY-6} C 380,{HY-12} 440,{HY-85} 520,{HY-92} C 600,{HY-88} 650,{HY-14} 720,{HY-8} L 860,{HY-4} L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4.5"/>')
a(f'<path d="M 505,{HY-90} L 498,{HY-60} M 535,{HY-90} L 548,{HY-55}" fill="none" {S} stroke-width="2"/>')
# flat slabs of basalt, cracked into plates (as in the Venera 13 photos)
for k, (sx, sy, sw_, sh) in enumerate(((40, 760, 250, 50), (320, 800, 260, 55), (690, 760, 160, 40),
                                        (60, 900, 330, 65), (420, 950, 360, 70), (130, 1040, 280, 50), (560, 1060, 260, 40))):
    n = 9
    pts = []
    for j in range(n):
        t = 2*math.pi*j/n
        pts.append((sx + sw_/2 + sw_/2*math.cos(t)*rnd.uniform(0.8, 1.05),
                    sy + sh/2*math.sin(t)*rnd.uniform(0.7, 1.1)))
    poly(a, pts, 3.2)
    for _ in range(2):   # cracks across the slab
        x0 = sx + sw_*rnd.uniform(0.2, 0.8)
        a(f'<path d="M {x0:.0f},{sy - sh*0.4:.0f} L {x0 + rnd.uniform(-20, 20):.0f},{sy:.0f} L {x0 + rnd.uniform(-25, 25):.0f},{sy + sh*0.4:.0f}" fill="none" {S} stroke-width="1.8"/>')
for _ in range(40):      # pebbles and grit between the slabs
    px, py = rnd.uniform(20, 830), rnd.uniform(700, 1070)
    a(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#fff" {S} stroke-width="1.8"/>')
# Venera 13 lander: toothed landing ring, pressure sphere, aerobrake disk, antenna
VX, VY = 620, 880
a(f'<ellipse cx="{VX}" cy="{VY}" rx="120" ry="28" fill="#fff" {S} stroke-width="4"/>')
for k in range(15):
    t = math.pi * k / 14
    tx, ty = VX - 118*math.cos(t), VY + 26*math.sin(t)
    a(f'<rect x="{tx-6:.1f}" y="{ty-4:.1f}" width="12" height="14" fill="#fff" {S} stroke-width="2"/>')
a(f'<path d="M {VX-70},{VY-12} L {VX-55},{VY-60} L {VX+55},{VY-60} L {VX+70},{VY-12} Z" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<circle cx="{VX}" cy="{VY-115}" r="70" fill="#fff" {S} stroke-width="4.5"/>')
a(f'<path d="M {VX-70},{VY-115} Q {VX},{VY-95} {VX+70},{VY-115}" fill="none" {S} stroke-width="2.5"/>')
a(f'<rect x="{VX-58}" y="{VY-88}" width="20" height="16" rx="3" fill="#fff" {S} stroke-width="2.5"/>')   # camera port
a(f'<ellipse cx="{VX}" cy="{VY-185}" rx="110" ry="18" fill="#fff" {S} stroke-width="4"/>')
a(f'<rect x="{VX-14}" y="{VY-255}" width="28" height="66" rx="5" fill="#fff" {S} stroke-width="3.5"/>')
for y in range(int(VY-250), int(VY-192), 10):
    a(f'<line x1="{VX-14}" y1="{y}" x2="{VX+14}" y2="{y+6}" {S} stroke-width="1.8"/>')
# the ejected camera lens cap, lying on the ground in the real photos
a(f'<ellipse cx="{VX-170}" cy="{VY+40}" rx="22" ry="9" fill="#fff" {S} stroke-width="3"/>')
a(f'<path d="M {VX-192},{VY+40} Q {VX-170},{VY+14} {VX-148},{VY+40}" fill="#fff" {S} stroke-width="3"/>')
save(o, 'sayfalar/05-venus-sol.svg')
