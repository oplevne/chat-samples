"""Stop 7 — the asteroid belt: Kirkwood gaps, Trojans, Ceres."""
import math, random
from kitap import S, W, star, dot, ortho, _dest, cratered_globe, shuttle_side, svg_open, story_block, save


def potato(a, x, y, r, seed, w=3, craters=2):
    """Irregular rocky asteroid."""
    rnd = random.Random(seed)
    pts = []
    for k in range(14):
        t = 2*math.pi*k/14
        rr = r * (0.75 + 0.35*rnd.random()) * (1.25 if k in (0, 7) else 1)
        pts.append((x + rr*math.cos(t), y + rr*0.75*math.sin(t)))
    a(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="#fff" {S} stroke-width="{w}"/>')
    for _ in range(craters):
        cx, cy, cr = x + rnd.uniform(-0.4, 0.4)*r, y + rnd.uniform(-0.3, 0.3)*r, r*rnd.uniform(0.1, 0.22)
        a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cr:.1f}" fill="#fff" {S} stroke-width="{w*0.6:.1f}"/>')


# ------------------------------------------------------------ right page ----
# The inner Solar System seen from above, to scale (1 AU = 57 px).
o = svg_open(); a = o.append
CX, CY, AU = 425, 372, 56.0
rnd = random.Random(1)
JUP_ANG = math.radians(-35)
for name, au, pr_, lab_ang in (('Mercury', 0.387, 3, 200), ('Venus', 0.723, 4, 160), ('Earth', 1.0, 4.5, 120), ('Mars', 1.524, 4, 70), ('Jupiter', 5.203, 15, -35)):
    a(f'<circle cx="{CX}" cy="{CY}" r="{au*AU:.1f}" fill="none" {S} stroke-width="1.8"/>')
    t = math.radians(lab_ang)
    px, py = CX + au*AU*math.cos(t), CY + au*AU*math.sin(t)
    a(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{pr_}" fill="#fff" {S} stroke-width="2.5"/>')
    if name in ('Earth', 'Mars', 'Jupiter'):
        a(f'<text x="{px + pr_ + 6:.1f}" y="{py + (24 if name == "Jupiter" else 5):.1f}" font-family="DejaVu Sans" font-size="16" fill="#000">{name}</text>')
# main belt, with Kirkwood gaps at the 3:1, 5:2 and 7:3 resonances with Jupiter
gaps = ((2.50, 0.035), (2.82, 0.03), (2.95, 0.022))
n = 0
while n < 1700:
    au = rnd.uniform(2.1, 3.3)
    if any(abs(au - g) < w for g, w in gaps) or (au > 3.0 and rnd.random() < 0.5):
        continue
    t = rnd.uniform(0, 2*math.pi)
    r = au * AU * (1 + rnd.gauss(0, 0.01))
    a(f'<circle cx="{CX + r*math.cos(t):.1f}" cy="{CY + r*math.sin(t):.1f}" r="1.3" fill="#000"/>'); n += 1
# Trojans, 60 degrees ahead of and behind Jupiter
for sgn in (1, -1):
    for _ in range(220):
        t = JUP_ANG + sgn*math.radians(60) + rnd.gauss(0, 0.2)
        r = 5.2 * AU * (1 + rnd.gauss(0, 0.04))
        a(f'<circle cx="{CX + r*math.cos(t):.1f}" cy="{CY + r*math.sin(t):.1f}" r="1.3" fill="#000"/>')
# the Sun
a(f'<circle cx="{CX}" cy="{CY}" r="11" fill="#fff" {S} stroke-width="3"/>')
for k in range(8):
    t = 2*math.pi*k/8
    a(f'<line x1="{CX + 15*math.cos(t):.1f}" y1="{CY + 15*math.sin(t):.1f}" x2="{CX + 22*math.cos(t):.1f}" y2="{CY + 22*math.sin(t):.1f}" {S} stroke-width="2.5"/>')
# Ceres on its orbit, and ZEYTIN-1 cruising through the belt
ct = math.radians(150)
cx_, cy_ = CX + 2.77*AU*math.cos(ct), CY + 2.77*AU*math.sin(ct)
a(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="5" fill="#fff" {S} stroke-width="2.5"/>')
a(f'<text x="{cx_ - 60:.1f}" y="{cy_ - 12:.1f}" font-family="DejaVu Sans" font-size="16" fill="#000">Ceres</text>')
for lbl, x, y in (('Trojans', CX + 5.2*AU*math.cos(JUP_ANG - 1.05) + 40, CY + 5.2*AU*math.sin(JUP_ANG - 1.05) + 30),
                  ('Trojans', CX + 5.2*AU*math.cos(JUP_ANG + 1.05) + 6, CY + 5.2*AU*math.sin(JUP_ANG + 1.05) + 30)):
    a(f'<text x="{x:.1f}" y="{y:.1f}" font-family="DejaVu Sans" font-size="16" fill="#000">{lbl}</text>')
shuttle_side(a, 'translate(140,650) rotate(-20) scale(0.2)', uid='r')
story_block(a, "The Asteroid Belt", [
    "Between Mars and Jupiter lies the asteroid belt: millions of rocks left over from when the planets were born.",
    "In movies they crowd together, but in real life they are so far apart that spacecraft fly through without hitting a single one.",
    "The biggest, Ceres, is a dwarf planet about 940 kilometers wide, with bright salty spots in a crater called Occator."],
    badge="330–480 million km from the Sun")
save(o, 'sayfalar/07-asteroit-sag.svg')

# ------------------------------------------------------------- left page ----
o = svg_open(); a = o.append
CERES_KM = 470
CX, CY, R = 440, 660, 360
OCC = (19.8, 239.3)       # Occator crater, 92 km
AHUNA = (-10.5, 316.2)    # Ahuna Mons, ~17 km wide, ~4 km tall
pr = cratered_globe(a, 'l', CX, CY, R, 10, 275, CERES_KM, named=[(OCC[0], OCC[1], 92, False, False)],
                    n=420, seed=9, sw=1.0, min_px=7, min_km=18, max_km=150)
P = lambda la, lo: (CX + R*pr(la, lo)[0], CY + R*pr(la, lo)[1])
kpd = 2*math.pi*CERES_KM/360
# Cerealia Facula (central dome) and Vinalia Faculae: bright salt deposits
def patch(lat, lon, km, seed, w=2.5):
    r = random.Random(seed)
    pts = [P(*_dest(lat, lon, km/2/kpd*r.uniform(0.7, 1.2), b)) for b in range(0, 360, 30)]
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="{w}" stroke-dasharray="4 3"/>')
patch(OCC[0], OCC[1], 16, 1, 3)
for d, b in ((24, 60), (28, 95), (22, 120)):
    la, lo = _dest(OCC[0], OCC[1], d/kpd, b)
    patch(la, lo, 7, b)
# Ahuna Mons: a lonely ice volcano with bright streaks down its flanks
ax, ay = P(*AHUNA)
a(f'<ellipse cx="{ax:.1f}" cy="{ay:.1f}" rx="26" ry="18" fill="#fff" {S} stroke-width="3"/>')
a(f'<ellipse cx="{ax:.1f}" cy="{ay - 2:.1f}" rx="14" ry="8" fill="#fff" {S} stroke-width="2"/>')
for k in range(8):
    t = 2*math.pi*k/8
    a(f'<line x1="{ax + 14*math.cos(t):.1f}" y1="{ay - 2 + 8*math.sin(t):.1f}" x2="{ax + 25*math.cos(t):.1f}" y2="{ay + 17*math.sin(t):.1f}" {S} stroke-width="1.5"/>')
# far-away neighbours: only a few, and very far apart
potato(a, 110, 150, 34, 3); potato(a, 760, 250, 18, 4, craters=1); potato(a, 70, 420, 12, 5, w=2.5, craters=1)
shuttle_side(a, 'translate(300,130) rotate(-5) scale(0.55)', uid='l')
save(o, 'sayfalar/07-asteroit-sol.svg')
