"""Stop 9 — Saturn: a planet that would float, thin icy rings, Enceladus' geysers."""
import math, random
from kitap import S, W, star, dot, shuttle_side, zeytin_body, svg_open, story_block, save

RS = 60268.0   # Saturn equatorial radius, km
RINGS = {'C_in': 74658, 'B_in': 92000, 'B_out': 117580, 'A_in': 122170, 'Encke': 133590, 'A_out': 136775, 'F': 140180}


def ellipse_arc(cx, cy, rx, ry, a0, a1, n=60):
    return [(cx + rx*math.cos(math.radians(a0 + (a1 - a0)*k/n)), cy + ry*math.sin(math.radians(a0 + (a1 - a0)*k/n))) for k in range(n + 1)]


def path(pts):
    return 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def saturn(a, cx, cy, Rp, tilt=22, sw=1.0, hexagon=True):
    """Saturn seen from slightly above the ring plane (north face of the rings)."""
    k = math.sin(math.radians(tilt))
    sc = Rp / RS
    def ring_band(r_in, r_out, back, extra=''):
        if back:
            outer = ellipse_arc(cx, cy, r_out*sc, r_out*sc*k, 180, 360); inner = ellipse_arc(cx, cy, r_in*sc, r_in*sc*k, 360, 180)
        else:
            outer = ellipse_arc(cx, cy, r_out*sc, r_out*sc*k, 0, 180); inner = ellipse_arc(cx, cy, r_in*sc, r_in*sc*k, 180, 0)
        a(f'<path d="{path(outer + inner)} Z" fill="#fff" {S} stroke-width="{2.4*sw:.2f}" {extra}/>')
    def all_rings(back):
        ring_band(RINGS['C_in'], RINGS['B_in'], back, f'stroke-dasharray="0"')
        ring_band(RINGS['B_in'], RINGS['B_out'], back)
        ring_band(RINGS['A_in'], RINGS['A_out'], back)
        # Encke gap and F ring as single lines
        for r in (RINGS['Encke'], RINGS['F']):
            pts = ellipse_arc(cx, cy, r*sc, r*sc*k, 180 if back else 0, 360 if back else 180)
            a(f'<path d="{path(pts)}" fill="none" {S} stroke-width="{(1.4 if r == RINGS["Encke"] else 1.8)*sw:.2f}" {"stroke-dasharray=" + chr(34) + "6 4" + chr(34) if r == RINGS["F"] else ""}/>')
        # a few ringlets inside the B ring
        for r in (98000, 104000, 110000):
            pts = ellipse_arc(cx, cy, r*sc, r*sc*k, 180 if back else 0, 360 if back else 180)
            a(f'<path d="{path(pts)}" fill="none" {S} stroke-width="{1.2*sw:.2f}"/>')
    all_rings(back=True)
    # the planet: 10% flatter at the poles
    Rpol = Rp * 54364 / RS
    a(f'<defs><clipPath id="sat{cx}"><ellipse cx="{cx}" cy="{cy}" rx="{Rp}" ry="{Rpol:.1f}"/></clipPath></defs>')
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="{Rp}" ry="{Rpol:.1f}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    a(f'<g clip-path="url(#sat{cx})">')
    for lat in (-50, -35, -20, -8, 12, 28, 45):    # soft cloud bands, tilted with the view
        y = cy - Rpol*math.sin(math.radians(lat))*math.cos(math.radians(tilt)) - 0
        w = Rp*math.cos(math.radians(lat)) + 10
        a(f'<path d="M {cx - w:.1f},{y:.1f} Q {cx:.1f},{y + Rpol*k*0.9:.1f} {cx + w:.1f},{y:.1f}" fill="none" {S} stroke-width="{2*sw:.2f}"/>')
    # shadow of the rings on the planet (a thin band just south of the equator)
    a(f'<path d="M {cx - Rp:.1f},{cy + 12*sw:.1f} Q {cx:.1f},{cy + Rpol*k*1.6:.1f} {cx + Rp:.1f},{cy + 12*sw:.1f} L {cx + Rp:.1f},{cy + 24*sw:.1f} Q {cx:.1f},{cy + Rpol*k*1.6 + 12*sw:.1f} {cx - Rp:.1f},{cy + 24*sw:.1f} Z" fill="#fff" {S} stroke-width="{1.8*sw:.2f}" stroke-dasharray="{5*sw:.1f} {4*sw:.1f}"/>')
    if hexagon:   # the north-polar hexagon, foreshortened
        hy = cy - Rpol*math.cos(math.radians(tilt))*0.93
        hr = Rp*0.28
        pts = [(cx + hr*math.cos(math.radians(30 + 60*j)), hy + hr*k*math.sin(math.radians(30 + 60*j))) for j in range(6)]
        a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="{2.4*sw:.2f}"/>')
        a(f'<ellipse cx="{cx}" cy="{hy:.1f}" rx="{hr*0.25:.1f}" ry="{hr*0.25*k:.1f}" fill="#fff" {S} stroke-width="{2*sw:.2f}"/>')
    a('</g>')
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="{Rp}" ry="{Rpol:.1f}" fill="none" {S} stroke-width="{5*sw:.2f}"/>')
    all_rings(back=False)


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
saturn(a, 425, 365, 132, tilt=24)
# Titan (big, hazy) and Enceladus (small, with its south-pole plume)
a(f'<circle cx="110" cy="590" r="30" fill="#fff" {S} stroke-width="4"/>')
a(f'<circle cx="110" cy="590" r="36" fill="none" {S} stroke-width="1.8" stroke-dasharray="4 5"/>')
a(f'<text x="110" y="650" text-anchor="middle" font-family="DejaVu Sans" font-size="16" fill="#000">Titan</text>')
ex, ey = 700, 110
a(f'<circle cx="{ex}" cy="{ey}" r="13" fill="#fff" {S} stroke-width="3"/>')
for k in range(-2, 3):
    a(f'<path d="M {ex + k*3},{ey + 12} q {k*8},20 {k*14},44" fill="none" {S} stroke-width="1.6" stroke-dasharray="3 4"/>')
a(f'<text x="{ex + 22}" y="{ey + 6}" font-family="DejaVu Sans" font-size="16" fill="#000">Enceladus</text>')
shuttle_side(a, 'translate(560,630) rotate(-8) scale(0.24)', uid='r')
for sx, sy, r in ((70, 140, 14), (790, 420, 12), (400, 60, 14), (60, 380, 12)):
    star(a, sx, sy, r)
story_block(a, "Saturn, the Floating Giant", [
    "Saturn is so light for its size that, in a bathtub big enough, it would float!",
    "Its rings are made of countless pieces of ice, from tiny grains to chunks as big as a house, yet in most places they are only about ten meters thick.",
    "Its little moon Enceladus shoots fountains of water into space from an ocean hidden under its icy shell."],
    badge="1.4 billion km from the Sun")
save(o, 'sayfalar/09-saturn-sag.svg')

# ------------------------------------------------------------- left page ----
# The south pole of Enceladus: "tiger stripe" fissures and their geysers.
# Enceladus orbits in the ring plane, so the rings look like a thin line.
o = svg_open(); a = o.append
# Saturn huge in the sky, rings edge-on
a(f'<line x1="-10" y1="250" x2="860" y2="250" {S} stroke-width="3"/>')
a(f'<line x1="-10" y1="256" x2="860" y2="256" {S} stroke-width="1.5"/>')
a(f'<defs><clipPath id="sk"><rect x="0" y="0" width="850" height="250"/></clipPath></defs>')
a(f'<ellipse cx="300" cy="250" rx="230" ry="207" fill="#fff" {S} stroke-width="5"/>')
for lat in (12, 25, 38, 52, 66):
    y = 250 - 207*math.sin(math.radians(lat)); w = 230*math.cos(math.radians(lat))
    a(f'<path d="M {300 - w:.1f},{y:.1f} Q 300,{y + 6:.1f} {300 + w:.1f},{y:.1f}" fill="none" {S} stroke-width="2"/>')
for lat in (-12, -25):
    y = 250 - 207*math.sin(math.radians(lat)); w = 230*math.cos(math.radians(lat))
    a(f'<path d="M {300 - w:.1f},{y:.1f} Q 300,{y + 6:.1f} {300 + w:.1f},{y:.1f}" fill="none" {S} stroke-width="2"/>')
a(f'<line x1="70" y1="250" x2="530" y2="250" {S} stroke-width="3.5"/>')
# icy ground with four parallel "tiger stripes" in perspective
HY = 470
a(f'<path d="M -10,{HY} Q 425,{HY - 25} 860,{HY} L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4.5"/>')
rnd = random.Random(5)
# each stripe: a fissure flanked by raised ridges, a few km wide, about 130 km long
for j, (base_y, x0, x1) in enumerate(((535, 120, 640), (625, 30, 560), (770, 230, 860), (950, -20, 600))):
    amp, half = 5 + j*4, 4 + j*3
    xs = list(range(int(x0), int(x1) + 1, 20))
    mid = [(x, base_y + amp*math.sin(x/80 + j)) for x in xs]
    for off, w in ((-half*3, 1.6), (half*3, 1.6)):           # ridges
        a(f'<path d="{path([(x, y + off) for x, y in mid])}" fill="none" {S} stroke-width="{w + j*0.3:.1f}"/>')
    top = [(x, y - half) for x, y in mid]; bot = [(x, y + half) for x, y in mid][::-1]
    a(f'<path d="{path(top + bot)} Z" fill="#000"/>')        # the dark fissure
    for gx in [x0 + (x1 - x0)*f for f in ((0.3, 0.75) if j < 2 else (0.25, 0.6))]:
        gy = base_y + amp*math.sin(gx/80 + j) - half
        h = 110 + j*80
        for kk in range(-2, 3):
            a(f'<path d="M {gx:.0f},{gy:.0f} Q {gx + kk*5:.0f},{gy - h*0.6:.0f} {gx + kk*(14 + j*9):.0f},{gy - h:.0f}" fill="none" {S} stroke-width="{1.3 + j*0.35:.1f}" stroke-dasharray="{3 + j},{4 + j}"/>')
# ice blocks along the ridges
for k, (bx, by, bw) in enumerate(((700, 560, 40), (640, 700, 50), (120, 860, 60), (380, 1060, 60))):
    a(f'<path d="M {bx},{by} l {bw*0.2:.0f},{-bw*0.5:.0f} l {bw*0.6:.0f},{-bw*0.1:.0f} l {bw*0.2:.0f},{bw*0.6:.0f} Z" fill="#fff" {S} stroke-width="3"/>')
zeytin_body(a, 'en', 'translate(700,1060) scale(0.6)')
# like Cassini did, ZEYTIN-1 flies right through a plume to taste the water
shuttle_side(a, 'translate(560,380) rotate(-5) scale(0.42)', uid='l')
save(o, 'sayfalar/09-saturn-sol.svg')
