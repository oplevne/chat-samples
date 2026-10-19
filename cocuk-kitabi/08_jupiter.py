"""Stop 8 — Jupiter and Io: the magnetic dance (flux tube), Io's volcanoes."""
import math, random
from kitap import S, W, star, dot, shuttle_side, zeytin_body, rock, svg_open, story_block, save

# Jupiter's belts (dark) between these planetographic latitudes
BELTS = ((7, 17, 'NEB'), (-20, -7, 'SEB'), (23, 28, 'NTB'), (-30, -26, 'STB'), (34, 38, 'NNTB'), (-40, -36, 'SSTB'))


def jupiter(a, uid, cx, cy, R, sw=1.0, grs=True, seed=1):
    """Jupiter with its main belts and zones, festoons, the Great Red Spot and white ovals."""
    rnd = random.Random(seed)
    a(f'<defs><clipPath id="j{uid}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5.5*sw:.2f}"/>')
    a(f'<g clip-path="url(#j{uid})">')
    Y = lambda lat: cy - R*math.sin(math.radians(lat))
    def edge(lat, amp, ph):
        y0 = Y(lat); w = R*math.cos(math.radians(lat)) + 20
        pts = []
        for k in range(41):
            x = cx - w + 2*w*k/40
            pts.append((x, y0 + amp*math.sin(k*0.9 + ph) + 0.18*R*(1 - ((x - cx)/(R + 1))**2)**0.5 * 0.08))
        return pts
    for lo, hi, name in BELTS:
        top, bot = edge(hi, 3*sw, rnd.uniform(0, 6)), edge(lo, 3*sw, rnd.uniform(0, 6))
        pts = top + bot[::-1]
        a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="{2.8*sw:.2f}"/>')
        # internal streaks give the belts texture
        for f in (0.35, 0.7):
            lat = lo + (hi - lo)*f
            ys = Y(lat); w = R*math.cos(math.radians(lat))
            x0 = cx - w*rnd.uniform(0.2, 0.9); x1 = x0 + w*rnd.uniform(0.3, 0.7)
            a(f'<path d="M {x0:.1f},{ys:.1f} Q {(x0+x1)/2:.1f},{ys + 4*sw:.1f} {x1:.1f},{ys:.1f}" fill="none" {S} stroke-width="{1.5*sw:.2f}"/>')
    # festoons: dark plumes hanging from the NEB's southern edge into the Equatorial Zone
    for k in range(6):
        x = cx - R*0.75 + k*R*0.3
        y = Y(7)
        a(f'<path d="M {x:.1f},{y:.1f} q {14*sw:.1f},{18*sw:.1f} {40*sw:.1f},{26*sw:.1f} q {-18*sw:.1f},{-4*sw:.1f} {-26*sw:.1f},{-26*sw:.1f}" fill="#fff" {S} stroke-width="{2*sw:.2f}"/>')
    # polar regions: mottled
    for sgn in (1, -1):
        for k in range(6):
            lat = sgn*rnd.uniform(48, 66); w = R*math.cos(math.radians(lat))
            x = cx + rnd.uniform(-0.8, 0.8)*w; y = Y(lat)
            a(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rnd.uniform(10, 22)*sw:.1f}" ry="{rnd.uniform(3, 5)*sw:.1f}" fill="#fff" {S} stroke-width="{1.5*sw:.2f}"/>')
    if grs:   # Great Red Spot in its "hollow" on the SEB's southern edge, ~22 S
        gx, gy = cx + R*0.25, Y(-22)
        a(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{R*0.2:.1f}" ry="{R*0.085:.1f}" fill="#fff" {S} stroke-width="{4*sw:.2f}"/>')
        a(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{R*0.12:.1f}" ry="{R*0.045:.1f}" fill="none" {S} stroke-width="{2.5*sw:.2f}"/>')
        a(f'<path d="M {gx - R*0.25:.1f},{gy - R*0.02:.1f} Q {gx:.1f},{gy - R*0.13:.1f} {gx + R*0.27:.1f},{gy - R*0.01:.1f}" fill="none" {S} stroke-width="{2*sw:.2f}"/>')
        for k in range(3):   # white ovals in the South Temperate Belt
            ox, oy = cx - R*0.5 + k*R*0.3, Y(-28)
            a(f'<ellipse cx="{ox:.1f}" cy="{oy:.1f}" rx="{R*0.05:.1f}" ry="{R*0.025:.1f}" fill="#fff" {S} stroke-width="{2.5*sw:.2f}"/>')
    a('</g>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" {S} stroke-width="{5.5*sw:.2f}"/>')


def io_disk(a, cx, cy, R, seed=4, sw=1.0):
    """Io: volcanic paterae, Pele's red ring, sulfur plains."""
    rnd = random.Random(seed)
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    # Pele's ring of red sulfur deposits (open ellipse) with the dark vent inside
    px, py = cx - R*0.25, cy + R*0.25
    a(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{R*0.42:.1f}" ry="{R*0.36:.1f}" fill="none" {S} stroke-width="{2.5*sw:.2f}" stroke-dasharray="{6*sw:.1f} {4*sw:.1f}"/>')
    for (fx, fy, fr) in ((px, py, 0.08), (cx + R*0.35, cy - R*0.3, 0.12), (cx - R*0.45, cy - R*0.4, 0.07), (cx + R*0.45, cy + R*0.35, 0.06), (cx + R*0.05, cy - R*0.55, 0.05)):
        pts = []
        for k in range(10):
            t = 2*math.pi*k/10
            rr = R*fr*rnd.uniform(0.7, 1.25)
            pts.append((fx + rr*math.cos(t), fy + rr*math.sin(t)))
        a(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="#fff" {S} stroke-width="{2.8*sw:.2f}"/>')
        a(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{R*fr*0.3:.1f}" fill="#000"/>')


# ------------------------------------------------------------ right page ----
o = svg_open(); a = o.append
a('<g transform="translate(127.5,0) scale(0.7)">')
JX, JY, JR = 300, 620, 230
IX, IY, IR = 720, 620, 55
for cx, cy, r in ((80, 140, 22), (560, 340, 18), (120, 280, 20), (330, 300, 14), (780, 410, 22), (70, 880, 22), (790, 880, 20), (60, 560, 16), (810, 760, 18), (470, 880, 14), (190, 920, 14)):
    star(a, cx, cy, r)
# dipole field lines Jupiter <-> Io: the Io flux tube
for L in (385, 420, 455):
    lam0 = math.acos(math.sqrt(JR / L))
    for sgn in (1, -1):
        pts = []
        for i in range(81):
            lam = sgn*lam0*(1 - i/80); r = L*math.cos(lam)**2
            pts.append(f'{JX + r*math.cos(lam):.1f},{JY - r*math.sin(lam):.1f}')
        a(f'<polyline points="{" ".join(pts)}" fill="none" {S} stroke-width="4"/>')
def bolt(cx, cy, s, rot):
    a(f'<path transform="translate({cx},{cy}) rotate({rot}) scale({s})" d="M -6,-36 L 14,-36 L 4,-8 L 16,-8 L -8,36 L -2,4 L -14,4 Z" fill="#fff" {S} stroke-width="{3.5/s:.2f}"/>')
bolt(555, 468, 1.15, 15); bolt(555, 772, 1.15, 165); bolt(650, 525, 0.85, 35); bolt(650, 715, 0.85, 145)
jupiter(a, 'r', JX, JY, JR, sw=1.0)
# auroral footprints where the flux tube meets Jupiter
lam = math.degrees(math.acos(math.sqrt(JR / 420)))
for sgn in (1, -1):
    y = JY - sgn*JR*math.sin(math.radians(lam)); x = JX + JR*math.cos(math.radians(lam))
    a(f'<circle cx="{x - 6:.1f}" cy="{y:.1f}" r="11" fill="#fff" {S} stroke-width="3.5"/>')
    for k in range(6):
        t = 2*math.pi*k/6
        a(f'<line x1="{x - 6 + 15*math.cos(t):.1f}" y1="{y + 15*math.sin(t):.1f}" x2="{x - 6 + 24*math.cos(t):.1f}" y2="{y + 24*math.sin(t):.1f}" {S} stroke-width="3"/>')
# Io with an umbrella plume on its limb
vx, vy = IX + IR*math.cos(math.radians(-55)), IY + IR*math.sin(math.radians(-55))
a(f'<g transform="translate({vx:.1f},{vy:.1f}) rotate(35)">')
a(f'<path d="M -62,6 C -66,-70 66,-70 62,6 C 50,-28 -50,-28 -62,6 Z" fill="#fff" {S} stroke-width="4"/>')
for d in ('M 0,6 C -6,-20 -20,-36 -34,-40', 'M 0,6 C 0,-20 0,-36 0,-44', 'M 0,6 C 6,-20 20,-36 34,-40'):
    a(f'<path d="{d}" fill="none" {S} stroke-width="3"/>')
a('</g>')
io_disk(a, IX, IY, IR, sw=0.9)
shuttle_side(a, 'translate(470,215) rotate(12) scale(0.48)', uid='r')
a('</g>')
story_block(a, "The Magnetic Dance", [
    "Every 42 hours, little Io dances once around giant Jupiter, always facing its partner and holding hands through an invisible magnetic bond.",
    "As Jupiter spins, its magnetic field sweeps past Io, and an electric current of about a million amperes flows along their bond like a sparkling ribbon.",
    "Where the ribbon touches Jupiter's poles, glowing auroras light up — the shining footprints of Io's dance!"],
    badge="778 million km from the Sun", top=712)
save(o, 'sayfalar/08-jupiter-sag.svg')

# ------------------------------------------------------------- left page ----
# Standing on Io: Jupiter fills the sky and never moves; a giant plume rises
# from the horizon and a lava lake glows in the foreground.
o = svg_open(); a = o.append
HY = 690
jupiter(a, 'l', 425, 330, 300, sw=1.3)
# the flux tube rising from Io toward Jupiter
for dx in (-30, 0, 30):
    a(f'<path d="M {700 + dx},{HY} C {760 + dx},{520} {760 + dx},{300} {640 + dx*0.6},{120}" fill="none" {S} stroke-width="3.5" stroke-dasharray="14 8"/>')
# horizon with blocky, steep mountains (Io's mountains reach 17 km)
a(f'<path d="M -10,{HY} L 60,{HY} L 90,{HY-120} L 200,{HY-150} L 230,{HY-20} L 300,{HY-10} L 520,{HY} L 860,{HY-4} L 860,1110 L -10,1110 Z" fill="#fff" {S} stroke-width="4.5"/>')
for x0, x1 in ((95, 130), (140, 170), (180, 210)):
    a(f'<path d="M {x0},{HY-118} L {x1},{HY-20}" fill="none" {S} stroke-width="2"/>')
# Tvashtar-like plume: gas and dust shoot from the vent in a fan of filaments
# and fall back in a wide umbrella hundreds of kilometres high
PX = 560
a(f'<path d="M {PX-250},{HY-6} C {PX-240},{HY-250} {PX+240},{HY-250} {PX+250},{HY-6}" fill="none" {S} stroke-width="3" stroke-dasharray="10 7"/>')
for k in range(-6, 7):
    t = k / 6
    ex, ey = PX + 245*math.sin(t*1.25), HY - 6 - 190*math.cos(t*1.25)
    a(f'<path d="M {PX},{HY-4} Q {PX + 60*t:.0f},{HY - 210:.0f} {ex:.0f},{ey:.0f}" fill="none" {S} stroke-width="{2.6 if k % 2 == 0 else 1.5}"/>')
for k in (-1, 1):   # material raining back down at the edge of the umbrella
    for j in range(4):
        x0 = PX + k*(150 + j*25)
        a(f'<path d="M {x0},{HY - 150 + j*28} q {k*8},40 {k*4},{110 - j*25}" fill="none" {S} stroke-width="1.5" stroke-dasharray="4 6"/>')
a(f'<path d="M {PX-14},{HY} L {PX},{HY-14} L {PX+14},{HY} Z" fill="#000"/>')
# lava lake (like Loki Patera): a dark crust with glowing cracks and an island
a(f'<ellipse cx="300" cy="900" rx="260" ry="80" fill="#fff" {S} stroke-width="4.5"/>')
rnd = random.Random(2)
for _ in range(9):
    x0 = rnd.uniform(90, 480); y0 = 900 + rnd.uniform(-45, 45)
    a(f'<path d="M {x0:.0f},{y0:.0f} l {rnd.uniform(15, 35):.0f},{rnd.uniform(-10, 10):.0f} l {rnd.uniform(15, 35):.0f},{rnd.uniform(-10, 10):.0f} l {rnd.uniform(10, 25):.0f},{rnd.uniform(-8, 8):.0f}" fill="none" {S} stroke-width="2.5"/>')
a(f'<ellipse cx="330" cy="895" rx="70" ry="22" fill="#fff" {S} stroke-width="3.5"/>')
# sulfur frost patches and rocks
for fx, fy, fr in ((640, 1000, 50), (120, 1040, 40), (760, 820, 35)):
    a(f'<ellipse cx="{fx}" cy="{fy}" rx="{fr}" ry="{fr*0.3:.0f}" fill="#fff" {S} stroke-width="2" stroke-dasharray="6 5"/>')
for k, (rx, ry, rr) in enumerate(((560, 820, 22), (820, 950, 18), (480, 1060, 16))):
    rock(a, rx, ry, rr, seed=60 + k)
zeytin_body(a, 'io', 'translate(700,1000) scale(0.6)')
shuttle_side(a, 'translate(40,770) rotate(-3) scale(0.3)', uid='l')
save(o, 'sayfalar/08-jupiter-sol.svg')
