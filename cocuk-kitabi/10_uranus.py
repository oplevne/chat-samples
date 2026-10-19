"""Stop 10 — Uranus: tipped on its side, 42-year days and nights, Miranda's giant cliff."""
import math, random
from kitap import S, W, star, dot, shuttle_side, zeytin_body, rock, svg_open, story_block, save

RU = 25559.0
# narrow main rings (km from centre), innermost to outermost; epsilon is the widest
RINGS = (41837, 42234, 42571, 44718, 45661, 47176, 47627, 48300, 50023, 51149)


def uranus_edge_on(a, cx, cy, R, tilt=-62, sw=1.0):
    """Uranus as seen from one of its moons: they orbit in the ring plane, so the
    rings are a thin line; the pole (with its hood) is off to one side."""
    t = math.radians(tilt)
    ux, uy = math.cos(t), math.sin(t)          # ring-plane direction
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    # polar hood toward the pole, perpendicular to the rings
    hx, hy = cx - uy*R*0.62, cy + ux*R*0.62
    a(f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{R*0.36:.1f}" ry="{R*0.2:.1f}" transform="rotate({tilt} {hx:.1f} {hy:.1f})" fill="#fff" {S} stroke-width="{2.6*sw:.2f}"/>')
    for f in (-0.3, 0.05, 0.4):  # faint bands parallel to the equator
        bx, by = cx - uy*R*f, cy + ux*R*f
        half = R*math.sqrt(max(0, 1 - f*f))*0.95
        a(f'<line x1="{bx - ux*half:.1f}" y1="{by - uy*half:.1f}" x2="{bx + ux*half:.1f}" y2="{by + uy*half:.1f}" {S} stroke-width="{1.5*sw:.2f}" stroke-dasharray="8 6"/>')
    L = 51149/RU*R
    a(f'<line x1="{cx - ux*L:.1f}" y1="{cy - uy*L:.1f}" x2="{cx + ux*L:.1f}" y2="{cy + uy*L:.1f}" {S} stroke-width="{3.2*sw:.2f}"/>')


def uranus(a, cx, cy, R, view=0.86, sw=1.0):
    """Uranus with its pole facing us: polar hood, faint bands, rings around the disk."""
    k = view   # ring ellipse ratio (1 = face-on)
    def rings(back):
        for r in RINGS + (67300,):
            rx, ry = r/RU*R, r/RU*R*k
            d0, d1 = (180, 360) if back else (0, 180)
            pts = [(cx + rx*math.cos(math.radians(d0 + (d1 - d0)*j/60)), cy + ry*math.sin(math.radians(d0 + (d1 - d0)*j/60))) for j in range(61)]
            dash = 'stroke-dasharray="6 6"' if r > 60000 else ''
            w = 3.2 if r == 51149 else (1.4 if r > 60000 else 1.8)
            a(f'<path d="M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" fill="none" {S} stroke-width="{w*sw:.2f}" {dash}/>')
    rings(True)
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    # bright polar hood around the sunward pole, slightly off centre, ringed by a darker collar
    px, py = cx - R*0.12, cy - R*0.1
    rnd = random.Random(2)
    hood = [(px + R*0.42*rnd.uniform(0.95, 1.05)*math.cos(2*math.pi*j/24), py + R*0.4*rnd.uniform(0.95, 1.05)*math.sin(2*math.pi*j/24)) for j in range(24)]
    a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in hood)}" fill="#fff" {S} stroke-width="{2.6*sw:.2f}"/>')
    a(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{R*0.72:.1f}" ry="{R*0.68:.1f}" fill="none" {S} stroke-width="{1.6*sw:.2f}" stroke-dasharray="8 6"/>')
    for j in range(3):   # small bright storms
        a(f'<ellipse cx="{cx + R*(0.45 - j*0.2):.1f}" cy="{cy + R*(0.5 - j*0.08):.1f}" rx="{R*0.05:.1f}" ry="{R*0.03:.1f}" fill="#fff" {S} stroke-width="{1.8*sw:.2f}"/>')
    rings(False)


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
uranus(a, 470, 310, 112)
# the five big moons (not to orbital scale)
for name, mx, my, mr in (('Miranda', 210, 180, 9), ('Ariel', 760, 120, 14), ('Umbriel', 795, 470, 14), ('Titania', 160, 470, 17), ('Oberon', 690, 590, 16)):
    a(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#fff" {S} stroke-width="3"/>')
    a(f'<text x="{mx}" y="{my + mr + 20}" text-anchor="middle" font-family="DejaVu Sans" font-size="15" fill="#000">{name}</text>')
# inset: Uranus rolls around the Sun on its side; its axis keeps pointing the same way
IX, IY = 160, 610
a(f'<ellipse cx="{IX}" cy="{IY}" rx="120" ry="38" fill="none" {S} stroke-width="1.8" stroke-dasharray="5 5"/>')
a(f'<circle cx="{IX}" cy="{IY}" r="9" fill="#fff" {S} stroke-width="2.5"/>')
for ang in (0, 90, 180, 270):
    x, y = IX + 120*math.cos(math.radians(ang)), IY + 38*math.sin(math.radians(ang))
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#fff" {S} stroke-width="2.5"/>')
    a(f'<line x1="{x - 20:.1f}" y1="{y - 3:.1f}" x2="{x + 20:.1f}" y2="{y + 3:.1f}" {S} stroke-width="2.2"/>')
shuttle_side(a, 'translate(600,48) rotate(4) scale(0.22)', uid='r')
for sx, sy, r in ((380, 60, 13), (60, 340, 12), (800, 300, 12)):
    star(a, sx, sy, r)
story_block(a, "Uranus, the Sideways Planet", [
    "Uranus is tipped over on its side, so it rolls around the Sun like a ball.",
    "Because of this, each pole gets about 42 years of sunshine, followed by 42 years of darkness.",
    "Methane gas makes it blue-green, and it holds the record for the coldest air of any planet: about −224°C."],
    badge="2.9 billion km from the Sun")
save(o, 'sayfalar/10-uranus-sag.svg')

# ------------------------------------------------------------- left page ----
# Verona Rupes on Miranda: the tallest known cliff in the Solar System,
# perhaps 20 km high; Uranus hangs in the sky with its rings around it.
o = svg_open(); a = o.append
uranus_edge_on(a, 590, 230, 140, sw=1.1)
# plateau on the left, the cliff face, and the valley floor far below
a(f'<path d="M -10,430 L 330,420 L 360,470 L 340,560 L 372,650 L 350,760 L 390,860 L 380,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="5"/>')
for y0 in range(470, 1080, 55):     # layering on the cliff face
    a(f'<path d="M {335 + (y0 % 3)*10},{y0} l 22,{18 + (y0 % 4)*4}" fill="none" {S} stroke-width="2"/>')
for k in range(5):                   # grooved "corona" terrain on the plateau
    y = 450 + k*45
    a(f'<path d="M 10,{y} Q 150,{y - 12} 300,{y + 4}" fill="none" {S} stroke-width="1.8"/>')
# valley floor and distant ridges
a(f'<path d="M 380,880 Q 600,860 860,875" fill="none" {S} stroke-width="3.5"/>')
a(f'<path d="M 420,800 L 520,770 L 600,790 L 700,760 L 860,780" fill="none" {S} stroke-width="2.5"/>')
rnd = random.Random(3)
for k in range(12):
    cx_, cy_ = rnd.uniform(430, 820), rnd.uniform(920, 1060)
    r_ = rnd.uniform(10, 30)
    a(f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{r_:.0f}" ry="{r_*0.3:.0f}" fill="#fff" {S} stroke-width="2.2"/>')
zeytin_body(a, 'mi', 'translate(230,425) scale(0.5)')
shuttle_side(a, 'translate(470,610) rotate(-12) scale(0.36)', uid='l')
for sx, sy, r in ((80, 90, 16), (260, 200, 12), (90, 330, 12), (800, 520, 14)):
    star(a, sx, sy, r)
save(o, 'sayfalar/10-uranus-sol.svg')
