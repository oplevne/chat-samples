"""Stop 2 — the Moon: maria, craters, Apollo 11 footprints."""
import math
from kitap import (S, W, star, dot, earth, moon, APOLLO11, shuttle_side, zeytin_body, paw_print,
                   boot_print, rock, svg_open, story_block, save)

# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
pe = earth(a, 'r', 130, 165, 55, 20, 30, sw=0.6)
MX, MY, MR = 525, 375, 250
# Earth -> Moon trajectory (about three days)
a(f'<path d="M 172,205 C 230,300 230,420 {MX-MR+8},{MY+40}" fill="none" {S} stroke-width="3" stroke-dasharray="10 9"/>')
pm = moon(a, 'r', MX, MY, MR, sw=0.8)
x, y, _ = pm(*APOLLO11); fx, fy = MX + MR*x, MY + MR*y
a(f'<line x1="{fx:.1f}" y1="{fy:.1f}" x2="{fx:.1f}" y2="{fy-30:.1f}" {S} stroke-width="3"/>')
a(f'<path d="M {fx:.1f},{fy-30:.1f} L {fx+22:.1f},{fy-30:.1f} L {fx+22:.1f},{fy-16:.1f} L {fx:.1f},{fy-16:.1f}" fill="#fff" {S} stroke-width="2.5"/>')
shuttle_side(a, 'translate(150,318) rotate(58) scale(0.22)', uid='r', head_rot=-58)
for sx, sy, r in ((330, 70, 16), (60, 330, 14), (800, 90, 18), (90, 620, 16), (810, 640, 14), (280, 660, 12)):
    star(a, sx, sy, r)
story_block(a, "Footprints on the Moon", [
    "Next stop: the Moon, about 384,000 kilometers away — a three-day trip, just like the Apollo astronauts made.",
    "Its dark patches are called seas, but they hold no water: they are plains of old lava that cooled more than three billion years ago.",
    "With no wind or rain to wipe them away, the footprints astronauts left in 1969 can stay in the dust for millions of years!"],
    badge="384,400 km from Earth")
save(o, 'sayfalar/02-ay-sag.svg')

# ------------------------------------------------------------- left page ----
# Tranquility Base, July 1969: no stars in the sky, just as in the real photographs
o = svg_open(); a = o.append
earth(a, 'l', 655, 175, 92, 15, 20, sw=0.85)
# horizon with low hills
a(f'<path d="M -10,560 C 120,540 200,555 300,548 C 420,538 520,530 620,540 C 720,550 790,535 860,540 L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4.5"/>')
# ZEYTIN-1 parked far away on the horizon
shuttle_side(a, 'translate(718,526) scale(0.19)', uid='p')
# distant craters (flattened by perspective)
for cx, cy, rx in ((150, 590, 60), (520, 580, 45), (760, 600, 40), (420, 615, 26), (60, 650, 30)):
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.22:.1f}" fill="#fff" {S} stroke-width="3"/>')
    a(f'<path d="M {cx-rx*0.8:.1f},{cy+rx*0.05:.1f} Q {cx},{cy+rx*0.2:.1f} {cx+rx*0.8:.1f},{cy+rx*0.05:.1f}" fill="none" {S} stroke-width="2"/>')
# --- Lunar Module "Eagle" ---
LX = 290
# rear legs (behind)
for sg in (-1, 1):
    a(f'<path d="M {LX+sg*95},590 L {LX+sg*190},705 M {LX+sg*110},560 L {LX+sg*185},700 M {LX+sg*80},600 L {LX+sg*170},700" fill="none" {S} stroke-width="5"/>')
    a(f'<line x1="{LX+sg*190}" y1="705" x2="{LX+sg*190}" y2="725" {S} stroke-width="3"/>')
    a(f'<ellipse cx="{LX+sg*190}" cy="712" rx="34" ry="10" fill="#fff" {S} stroke-width="4"/>')
# descent stage: octagonal box wrapped in crinkled foil
a(f'<path d="M {LX-100},470 L {LX+100},470 L {LX+122},492 L {LX+122},580 L {LX+100},602 L {LX-100},602 L {LX-122},580 L {LX-122},492 Z" fill="#fff" {S} stroke-width="5"/>')
for xx in (LX-60, LX+60):
    a(f'<line x1="{xx}" y1="472" x2="{xx}" y2="600" {S} stroke-width="3"/>')
for k, (x0, x1) in enumerate(((LX-118, LX-62), (LX-58, LX+58), (LX+62, LX+118))):
    for yy in (505, 545, 580):
        d = f'M {x0+6},{yy}'
        for i in range(6):
            d += f' l {(x1-x0-12)/6:.1f},{(-5 if i % 2 else 5)}'
        a(f'<path d="{d}" fill="none" {S} stroke-width="1.8"/>')
# ascent stage
a(f'<path d="M {LX-95},470 L {LX-92},405 L {LX-62},362 L {LX},350 L {LX+62},362 L {LX+90},400 L {LX+92},470 Z" fill="#fff" {S} stroke-width="5"/>')
a(f'<path d="M {LX-55},385 L {LX-18},380 L {LX-30},412 Z M {LX+55},385 L {LX+18},380 L {LX+30},412 Z" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<rect x="{LX-24}" y="420" width="48" height="44" rx="4" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<circle cx="{LX}" cy="442" r="10" fill="#fff" {S} stroke-width="2.5"/>')
for sg in (-1, 1):  # RCS thruster quads
    a(f'<rect x="{LX+sg*105-9}" y="392" width="18" height="18" fill="#fff" {S} stroke-width="3"/>')
    a(f'<path d="M {LX+sg*105},392 l -5,-14 l 10,0 Z M {LX+sg*114 if sg>0 else LX+sg*114},401 l {sg*14},-5 l 0,10 Z" fill="#fff" {S} stroke-width="2.5"/>')
# rendezvous antenna dish + VHF antennas
a(f'<line x1="{LX+40}" y1="358" x2="{LX+55}" y2="318" {S} stroke-width="3"/>')
a(f'<ellipse cx="{LX+58}" cy="312" rx="20" ry="9" transform="rotate(-20 {LX+58} 312)" fill="#fff" {S} stroke-width="3"/>')
a(f'<path d="M {LX-50},365 L {LX-80},322 M {LX+80},375 L {LX+112},340" fill="none" {S} stroke-width="2.5"/>')
# porch, ladder and front leg
a(f'<rect x="{LX-30}" y="600" width="60" height="10" fill="#fff" {S} stroke-width="3"/>')
a(f'<path d="M {LX},610 L {LX},752" fill="none" {S} stroke-width="6"/>')
for xx in (LX-16, LX+16):
    a(f'<line x1="{xx}" y1="610" x2="{xx}" y2="742" {S} stroke-width="3"/>')
for yy in range(626, 742, 18):
    a(f'<line x1="{LX-16}" y1="{yy}" x2="{LX+16}" y2="{yy}" {S} stroke-width="3"/>')
a(f'<ellipse cx="{LX}" cy="756" rx="42" ry="12" fill="#fff" {S} stroke-width="4"/>')
# flag on its horizontal rod, still wrinkled from being folded
FX, FY = 560, 420
a(f'<line x1="{FX}" y1="{FY}" x2="{FX}" y2="{FY+290}" {S} stroke-width="5"/>')
a(f'<line x1="{FX}" y1="{FY+4}" x2="{FX+140}" y2="{FY+4}" {S} stroke-width="4"/>')
a(f'<path d="M {FX},{FY+4} L {FX+140},{FY+4} L {FX+140},{FY+88} Q {FX+120},{FY+80} {FX+100},{FY+92} Q {FX+70},{FY+100} {FX+40},{FY+86} Q {FX+20},{FY+80} {FX},{FY+90} Z" fill="#fff" {S} stroke-width="3.5"/>')
for k in range(1, 6):
    y0 = FY + 4 + k * 14.5
    x0 = FX + 62 if k < 3 else FX
    a(f'<path d="M {x0},{y0:.1f} Q {(x0+FX+140)/2:.0f},{y0+(4 if k%2 else -4):.1f} {FX+140},{y0:.1f}" fill="none" {S} stroke-width="2"/>')
a(f'<rect x="{FX}" y="{FY+4}" width="62" height="42" fill="#fff" {S} stroke-width="3"/>')
for i in range(5):
    for j in range(3):
        a(f'<circle cx="{FX+9+i*11}" cy="{FY+13+j*12}" r="2" fill="#fff" {S} stroke-width="1.5"/>')
# trail of boot prints from the ladder to the flag
for k, (bx, by) in enumerate(((330, 790), (365, 772), (395, 795), (430, 776), (462, 800), (495, 780), (525, 760), (552, 738))):
    boot_print(a, bx, by, 0.36, rot=60 + (8 if k % 2 else -8))
# Zeytin and the paw prints
zeytin_body(a, 'z', 'translate(712,815) scale(0.76)')
for k, (px, py) in enumerate(((645, 852), (617, 872), (589, 855), (561, 876), (533, 860))):
    paw_print(a, px, py, 0.9, rot=-70)
# Buzz Aldrin's famous boot print, close up in the foreground
a('<g transform="translate(215,965) scale(1, 0.62)">')
boot_print(a, 0, 0, 2.6, rot=-75, ribs=14)
a('</g>')
# rocks and a small foreground crater
for k, (rx, ry, rr) in enumerate(((90, 860, 26), (470, 925, 16), (770, 955, 30), (640, 1030, 16), (400, 1040, 20), (800, 860, 14))):
    rock(a, rx, ry, rr, seed=k)
a(f'<ellipse cx="560" cy="950" rx="95" ry="26" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<path d="M 475,955 Q 560,985 645,955" fill="none" {S} stroke-width="2.5"/>')
save(o, 'sayfalar/02-ay-sol.svg')
