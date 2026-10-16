"""Shared drawing helpers for the Zeytin space-cat book (SVG line art)."""
import math

S = 'stroke="#000" stroke-linejoin="round" stroke-linecap="round"'


def star(a, cx, cy, r, sw=3.5):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f'{cx+rr*math.cos(ang):.1f},{cy+rr*math.sin(ang):.1f}')
    a(f'<polygon points="{" ".join(pts)}" fill="#fff" {S} stroke-width="{sw}"/>')


def dot(a, cx, cy, r, sw=3):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" {S} stroke-width="{sw}"/>')


def _fluffy_head_path(rx=125, ry=105, tufts=22):
    """Head outline: smooth on top, long-haired spiky tufts on cheeks and chin."""
    pts = []
    n = 360
    for i in range(n):
        t = 2 * math.pi * i / n
        w = min(1, max(0, (math.sin(t) + 0.3) / 0.6))  # 0 on top, 1 on cheeks/chin
        frac = (tufts * t / (2 * math.pi)) % 1
        k = 1 + 0.16 * w * (1 - frac) ** 2
        pts.append(f'{rx*k*math.cos(t):.1f},{ry*k*math.sin(t):.1f}')
    return 'M ' + ' L '.join(pts) + ' Z'


def zeytin_head(a, uid, transform, sw=1.0):
    """Zeytin, after the real cat: long-haired, white face/chest/ruff, black ears and
    black cap that wraps around both eyes (down to the cheek on the viewer's left),
    white blaze between the eyes, pink nose, one big round pale-blue eye, and a
    pirate patch over the closed eye. Drawn around (0,0); sw scales strokes."""
    st = lambda w: f'{S} stroke-width="{w*sw:.2f}"'
    head = _fluffy_head_path(rx=130, ry=108, tufts=24)
    a(f'<g transform="{transform}">')
    a(f'<defs><clipPath id="hc{uid}"><path d="{head}"/></clipPath></defs>')
    # big pointed black ears with white inner tufts
    for sg in (-1, 1):
        a(f'<path d="M {sg*128},-30 Q {sg*130},-140 {sg*112},-195 Q {sg*65},-160 {sg*25},-100 Z" fill="#000" {st(4.5)}/>')
        for x0, y0, x1, y1 in ((92, -70, 100, -130), (80, -80, 92, -145), (68, -88, 82, -125)):
            a(f'<path d="M {sg*x0},{y0} Q {sg*(x0+10)},{(y0+y1)/2} {sg*x1},{y1}" fill="none" stroke="#fff" stroke-linecap="round" stroke-width="{2.5*sw:.2f}"/>')
    a(f'<path d="{head}" fill="#fff" {st(4.5)}/>')
    a(f'<g clip-path="url(#hc{uid})">')
    # black cap: over the head, around both eyes, down to the cheek on the viewer's left,
    # leaving a white blaze that narrows to a point on the forehead
    a('<path d="M -160,60 L -160,-160 L 160,-160 L 160,22 '
      'C 130,30 100,44 76,42 C 48,40 26,30 20,4 '
      'C 16,-30 12,-62 0,-92 '
      'C -12,-62 -16,-30 -20,4 '
      'C -24,30 -40,50 -74,56 C -104,62 -140,60 -160,58 Z" fill="#000"/>')
    a('</g>')
    # white chest/cheek fur strokes
    for sg in (1,):
        a(f'<path d="M {sg*116},48 q {sg*-12},10 {sg*-6},26" fill="none" {st(2.5)}/>')
    a(f'<path d="M -100,82 q 12,6 10,22 M 100,82 q -12,6 -10,22" fill="none" {st(2.5)}/>')
    a(f'<path d="M -14,112 q 6,-12 0,-22 M 14,112 q -6,-12 0,-22" fill="none" {st(2.5)}/>')
    # pirate patch over the closed eye (viewer's left), white-rimmed so it reads on black fur
    a(f'<path d="M -150,-30 L -78,-6 M -30,-14 L 50,-150" fill="none" stroke="#fff" stroke-linecap="round" stroke-width="{13*sw:.2f}"/>')
    a(f'<path d="M -150,-30 L -78,-6 M -30,-14 L 50,-150" fill="none" stroke="#000" stroke-linecap="round" stroke-width="{7*sw:.2f}"/>')
    a(f'<ellipse cx="-55" cy="6" rx="36" ry="31" fill="#000" stroke="#fff" stroke-width="{3*sw:.2f}"/>')
    # big round open eye (viewer's right): pale blue in the colour version
    a(f'<circle cx="55" cy="4" r="33" fill="#fff" {st(4)}/>')
    a(f'<circle cx="55" cy="6" r="21" fill="none" {st(2.5)}/>')
    a(f'<circle cx="65" cy="-6" r="8" fill="#fff" {st(2.5)}/>')
    a(f'<circle cx="45" cy="17" r="4" fill="#fff" {st(2)}/>')
    # pink nose, small mouth
    a(f'<path d="M -12,46 Q 0,40 12,46 L 0,58 Z" fill="#fff" {st(3.5)}/>')
    a(f'<path d="M 0,58 L 0,66 M -16,70 Q -8,77 0,66 Q 8,77 16,70" fill="none" {st(3.5)}/>')
    # long whiskers, white-haloed so they show over black fur too
    for sg in (-1, 1):
        for y0, y1 in ((56, 34), (63, 64), (70, 94)):
            d = f'M {sg*36},{y0} Q {sg*95},{(y0+y1)/2-4} {sg*155},{y1}'
            a(f'<path d="{d}" fill="none" stroke="#fff" stroke-linecap="round" stroke-width="{5.5*sw:.2f}"/>')
            a(f'<path d="{d}" fill="none" {st(2.5)}/>')
    a('</g>')


def shuttle_side(a, transform, uid='s', head_rot=0):
    """Side view of Zeytin's shuttle with a big round window, nose to the right."""
    a(f'<g transform="{transform}">')
    for y0, s in ((-22, 1), (0, 1.3), (22, 1)):
        a(f'<path d="M -10,{y0-9} Q {-50*s},{y0-16} {-80*s},{y0} Q {-50*s},{y0+16} -10,{y0+9} Z" fill="#fff" {S} stroke-width="3.5"/>')
    a(f'<path d="M 30,-50 L 70,-140 L 120,-140 L 150,-50 Z" fill="#fff" {S} stroke-width="4.5"/>')
    a(f'<path d="M 80,-125 L 110,-125" fill="none" {S} stroke-width="3"/>')
    for y0 in (-22, 0, 22):
        a(f'<rect x="-14" y="{y0-9}" width="26" height="18" rx="3" fill="#fff" {S} stroke-width="3.5"/>')
    a(f'<path d="M 10,-60 L 420,-60 Q 560,-58 600,0 Q 560,58 420,60 L 10,60 Z" fill="#fff" {S} stroke-width="5"/>')
    a(f'<path d="M 140,40 L 330,40 L 200,110 L 120,110 Z" fill="#fff" {S} stroke-width="4.5"/>')
    a(f'<path d="M 40,-30 L 330,-30 M 40,30 L 120,30" fill="none" {S} stroke-width="3"/>')
    for x in (70, 120, 170):
        a(f'<circle cx="{x}" cy="-45" r="5" fill="#fff" {S} stroke-width="2.5"/>')
    a(f'<text x="230" y="14" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="#fff" stroke="#000" stroke-width="2" stroke-linejoin="round">ZEYTIN-1</text>')
    # window with Zeytin
    a(f'<defs><clipPath id="w{uid}"><circle cx="450" cy="-5" r="46"/></clipPath></defs>')
    a(f'<circle cx="450" cy="-5" r="54" fill="#fff" {S} stroke-width="5"/>')
    a(f'<g clip-path="url(#w{uid})">')
    zeytin_head(a, uid, f'translate(450,-5) rotate({head_rot}) translate(0,15) scale(0.27)', sw=2.2)
    a('</g>')
    a(f'<circle cx="450" cy="-5" r="46" fill="none" {S} stroke-width="3.5"/>')
    a('</g>')


# ---------------------------------------------------------------- globes ----

_LAND = None


def _land():
    global _LAND
    if _LAND is None:
        import json, os
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'veri', 'ne_110m_land.geojson')
        rings = []
        for f in json.load(open(path))['features']:
            g = f['geometry']
            polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for poly in polys:
                rings.append(poly[0])
        _LAND = rings
    return _LAND


def ortho(lat0, lon0):
    """Orthographic projection; returns f(lat, lon, alt=1) -> (x, y, visible) on a unit disk, y down."""
    p0, l0 = math.radians(lat0), math.radians(lon0)
    def f(lat, lon, alt=1.0):
        p, l = math.radians(lat), math.radians(lon)
        cosc = math.sin(p0)*math.sin(p) + math.cos(p0)*math.cos(p)*math.cos(l-l0)
        x = math.cos(p)*math.sin(l-l0)
        y = math.cos(p0)*math.sin(p) - math.sin(p0)*math.cos(p)*math.cos(l-l0)
        return alt*x, -alt*y, cosc > 0
    return f


def earth(a, uid, cx, cy, R, lat0, lon0, sw=1.0):
    """Earth with real (Natural Earth 1:110m) coastlines. Returns the projection."""
    pr = ortho(lat0, lon0)
    a(f'<defs><clipPath id="e{uid}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    a(f'<g clip-path="url(#e{uid})">')
    for ring in _land():
        pts, vis = [], 0
        for lon, lat in ring:
            x, y, v = pr(lat, lon)
            if not v:  # push hidden points onto the limb
                n = math.hypot(x, y) or 1
                x, y = x/n, y/n
            vis += v
            pts.append(f'{cx+R*x:.1f},{cy+R*y:.1f}')
        if vis:
            a(f'<polygon points="{" ".join(pts)}" fill="#fff" {S} stroke-width="{3*sw:.2f}"/>')
    a('</g>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" {S} stroke-width="{5*sw:.2f}"/>')
    return pr


def projected_line(pr, cx, cy, R, pts, alt=1.0):
    """Polyline of (lat, lon) points on the globe, only the visible runs."""
    runs, cur = [], []
    for lat, lon in pts:
        x, y, v = pr(lat, lon, alt)
        if v:
            cur.append(f'{cx+R*x:.1f},{cy+R*y:.1f}')
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    return runs


# ----------------------------------------------------------------- pages ----

W, H = 850, 1100


def svg_open():
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    o.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
    return o


def story_block(a, title, story, badge=None, top=705):
    """Outlined (colourable) title plus the readable story text under a scene."""
    import textwrap
    a(f'<text x="{W/2}" y="{top}" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#fff" stroke="#000" stroke-width="2.2" stroke-linejoin="round">{title}</text>')
    y = top + 52
    for para in story:
        for line in textwrap.wrap(para, 60):
            a(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="DejaVu Sans" font-size="23" fill="#000">{line}</text>')
            y += 31
        y += 8
    if badge:  # mission tag in the top-left corner
        bw = 30 + 11.2 * len(badge)
        a(f'<rect x="40" y="28" width="{bw:.0f}" height="36" rx="18" fill="#fff" {S} stroke-width="3"/>')
        a(f'<text x="{40+bw/2:.0f}" y="52" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="18" fill="#000">{badge}</text>')
    assert y < H - 38, f'story too long ({y})'


def save(o, path):
    o.append('</svg>')
    open(path, 'w').write('\n'.join(o))


# ------------------------------------------------------------------ moon ----

# Major near-side craters: (name, selenographic lat, lon, diameter km)
MOON_CRATERS = [
    ('Tycho', -43.3, -11.2, 85), ('Copernicus', 9.6, -20.1, 93), ('Kepler', 8.1, -38.0, 31),
    ('Aristarchus', 23.7, -47.4, 40), ('Plato', 51.6, -9.4, 101), ('Clavius', -58.8, -14.1, 225),
    ('Grimaldi', -5.2, -68.6, 173), ('Langrenus', -8.9, 61.0, 132), ('Petavius', -25.1, 60.4, 177),
    ('Theophilus', -11.4, 26.4, 100), ('Cyrillus', -13.2, 24.0, 98), ('Catharina', -18.1, 23.6, 99),
    ('Ptolemaeus', -9.2, -1.8, 154), ('Alphonsus', -13.4, -2.8, 111), ('Arzachel', -18.2, -1.9, 97),
    ('Archimedes', 29.7, -4.0, 82), ('Eratosthenes', 14.5, -11.3, 58), ('Posidonius', 31.8, 29.9, 95),
    ('Schickard', -44.4, -54.6, 206), ('Maginus', -50.0, -6.2, 194), ('Longomontanus', -49.6, -21.7, 145),
    ('Hipparchus', -5.1, 5.2, 138), ('Albategnius', -11.2, 4.0, 136), ('Endymion', 53.6, 56.5, 123),
    ('Atlas', 46.7, 44.4, 87), ('Hercules', 46.7, 39.1, 69), ('Gassendi', -17.6, -40.1, 110),
    ('Bullialdus', -20.7, -22.2, 61), ('Proclus', 16.1, 46.8, 28), ('Aristoteles', 50.2, 17.4, 87),
    ('Eudoxus', 44.3, 16.3, 67), ('Pythagoras', 63.7, -63.0, 145), ('Furnerius', -36.0, 60.6, 125),
    ('Stevinus', -32.5, 54.2, 74), ('Piccolomini', -29.7, 32.2, 88), ('Walter', -33.1, 0.7, 128),
]
DARK_FLOOR = {'Plato', 'Grimaldi'}
COMPLEX = {'Tycho', 'Copernicus', 'Theophilus', 'Langrenus', 'Petavius', 'Eratosthenes', 'Aristoteles', 'Bullialdus', 'Gassendi'}
APOLLO11 = (0.674, 23.473)

_MARIA = None
_TEX = None


def _maria():
    global _MARIA
    if _MARIA is None:
        import json, os
        _MARIA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'veri', 'ay_maria.json')))
    return _MARIA


def _dest(lat, lon, dist, bearing):
    """Point at angular distance `dist` (deg) along `bearing` (deg) from (lat, lon)."""
    p1, l1, d, b = map(math.radians, (lat, lon, dist, bearing))
    p2 = math.asin(math.sin(p1)*math.cos(d) + math.cos(p1)*math.sin(d)*math.cos(b))
    l2 = l1 + math.atan2(math.sin(b)*math.sin(d)*math.cos(p1), math.cos(d) - math.sin(p1)*math.sin(p2))
    return math.degrees(p2), math.degrees(l2)


def _in_maria(lat, lon):
    inside = False
    for ring in _maria():
        for (y1, x1), (y2, x2) in zip(ring, ring[1:]):
            if (y1 > lat) != (y2 > lat) and lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def _texture_craters(seed=3, n=900):
    """Representative small craters (not named features): power-law sizes, about
    twenty times denser on the old highlands than on the younger maria."""
    import random
    rnd = random.Random(seed); out = []
    while len(out) < n:
        lat = math.degrees(math.asin(rnd.uniform(-1, 1))); lon = rnd.uniform(-95, 95)
        km = 12 * (1 - rnd.random()) ** (-1 / 1.6)
        if km > 70:
            continue
        if _in_maria(lat, lon) and rnd.random() > 0.05:
            continue
        out.append((lat, lon, km))
    return out


def _crater(a, pr, P, lat, lon, km, sw, dark=False, peak=False, w=2.6, kpd=30.3):
    rho = km / 2 / kpd
    ring = [pr(*_dest(lat, lon, rho, b)) for b in range(0, 360, 12)]
    a(f'<polygon points="{" ".join(P(x, y) for x, y, _ in ring)}" fill="#fff" {S} stroke-width="{w*sw:.2f}"/>')
    inner = [pr(*_dest(lat, lon, rho*0.75, b)) for b in range(190, 351, 16)]
    a(f'<polyline points="{" ".join(P(x, y) for x, y, _ in inner)}" fill="none" {S} stroke-width="{w*0.65*sw:.2f}"/>')
    if dark:
        fl = [pr(*_dest(lat, lon, rho*0.7, b)) for b in range(0, 360, 15)]
        a(f'<polygon points="{" ".join(P(x, y) for x, y, _ in fl)}" fill="#fff" {S} stroke-width="{1.6*sw:.2f}" stroke-dasharray="{4*sw:.1f} {4*sw:.1f}"/>')
    if peak:
        pk = [pr(*_dest(lat, lon, rho*0.14, b)) for b in range(0, 360, 60)]
        a(f'<polygon points="{" ".join(P(x, y) for x, y, _ in pk)}" fill="#fff" {S} stroke-width="{1.5*sw:.2f}"/>')


def moon(a, uid, cx, cy, R, lat0=0, lon0=0, sw=1.0, min_km=0, rays=True, texture=True):
    """Near side of the Moon: maria outlines, real major craters, Tycho's rays,
    plus representative small craters for texture."""
    global _TEX
    pr = ortho(lat0, lon0)
    P = lambda x, y: f'{cx+R*x:.1f},{cy+R*y:.1f}'
    a(f'<defs><clipPath id="m{uid}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    a(f'<g clip-path="url(#m{uid})">')
    for ring in _maria():
        pts, vis = [], 0
        for lat, lon in ring:
            x, y, v = pr(lat, lon)
            if not v:
                n = math.hypot(x, y) or 1; x, y = x/n, y/n
            vis += v; pts.append(P(x, y))
        if vis:
            a(f'<polygon points="{" ".join(pts)}" fill="#fff" {S} stroke-width="{3*sw:.2f}"/>')
    if rays:  # Tycho's bright rays, as fine dashed lines
        _, tl, tn, _ = MOON_CRATERS[0]
        for bearing, length in ((15, 75), (40, 40), (75, 30), (110, 25), (160, 18), (200, 20), (250, 35), (290, 45), (330, 38)):
            pts = []
            for k in range(2, 41):
                la, lo = _dest(tl, tn, 1.6 + length*k/40, bearing)
                x, y, v = pr(la, lo)
                if v: pts.append(P(x, y))
            a(f'<polyline points="{" ".join(pts)}" fill="none" {S} stroke-width="{1.6*sw:.2f}" stroke-dasharray="{2*sw:.1f} {7*sw:.1f}"/>')
    if texture:
        if _TEX is None:
            _TEX = _texture_craters()
        for lat, lon, km in _TEX:
            if pr(lat, lon)[2] and R * km / 1737 > 2.5:
                _crater(a, pr, P, lat, lon, km, sw, w=1.8)
    for name, lat, lon, km in MOON_CRATERS:
        if km < min_km or not pr(lat, lon)[2]:
            continue
        _crater(a, pr, P, lat, lon, km, sw, dark=name in DARK_FLOOR, peak=name in COMPLEX)
    a('</g>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" {S} stroke-width="{5*sw:.2f}"/>')
    return pr


def zeytin_body(a, uid, transform, wave=True):
    """Full-body Zeytin in a spacesuit, feet at (0,0), about 300 units tall."""
    a(f'<g transform="{transform}">')
    a(f'<rect x="-62" y="-205" width="124" height="112" rx="18" fill="#fff" {S} stroke-width="4"/>')  # backpack
    for sg in (-1, 1):  # legs + boots
        a(f'<rect x="{-40 if sg < 0 else 8}" y="-100" width="32" height="88" rx="14" fill="#fff" {S} stroke-width="4"/>')
        a(f'<path d="M {sg*24-30},-4 Q {sg*24-30},-24 {sg*24},-24 Q {sg*24+30},-24 {sg*24+30},-4 Z" fill="#fff" {S} stroke-width="4"/>')
    # tail in its own suit sleeve
    a(f'<path d="M 40,-100 C 90,-100 105,-150 88,-185 C 82,-198 68,-192 72,-180 C 85,-150 70,-125 38,-122" fill="#fff" {S} stroke-width="4"/>')
    a(f'<rect x="-58" y="-180" width="116" height="96" rx="34" fill="#fff" {S} stroke-width="4.5"/>')  # torso
    a(f'<rect x="-28" y="-160" width="56" height="34" rx="6" fill="#fff" {S} stroke-width="3"/>')
    for x in (-14, 0, 14):
        a(f'<circle cx="{x}" cy="-143" r="5" fill="#fff" {S} stroke-width="2.5"/>')
    a(f'<path d="M -58,-110 L 58,-110" fill="none" {S} stroke-width="3"/>')
    # arms: left down, right waving
    a(f'<path d="M -52,-165 Q -92,-140 -88,-98" fill="none" {S} stroke-width="30"/>')
    a(f'<path d="M -52,-165 Q -92,-140 -88,-98" fill="none" stroke="#fff" stroke-linecap="round" stroke-width="22"/>')
    a(f'<circle cx="-88" cy="-92" r="15" fill="#fff" {S} stroke-width="4"/>')
    if wave:
        a(f'<path d="M 52,-165 Q 92,-185 100,-235" fill="none" {S} stroke-width="30"/>')
        a(f'<path d="M 52,-165 Q 92,-185 100,-235" fill="none" stroke="#fff" stroke-linecap="round" stroke-width="22"/>')
        a(f'<circle cx="101" cy="-242" r="15" fill="#fff" {S} stroke-width="4"/>')
    # helmet with Zeytin
    a(f'<defs><clipPath id="hb{uid}"><circle cx="0" cy="-238" r="62"/></clipPath></defs>')
    a(f'<circle cx="0" cy="-238" r="66" fill="#fff" {S} stroke-width="4.5"/>')
    a(f'<g clip-path="url(#hb{uid})">')
    zeytin_head(a, uid, 'translate(0,-225) scale(0.36)', sw=2.0)
    a('</g>')
    a(f'<circle cx="0" cy="-238" r="62" fill="none" {S} stroke-width="3"/>')
    a(f'<ellipse cx="0" cy="-178" rx="50" ry="11" fill="#fff" {S} stroke-width="4"/>')
    a('</g>')


def paw_print(a, x, y, s=1.0, rot=0):
    a(f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">')
    a(f'<ellipse cx="0" cy="4" rx="9" ry="7" fill="#fff" {S} stroke-width="2.5"/>')
    for dx, dy in ((-10, -7), (-3.5, -11), (3.5, -11), (10, -7)):
        a(f'<ellipse cx="{dx}" cy="{dy}" rx="3.2" ry="4" fill="#fff" {S} stroke-width="2"/>')
    a('</g>')


_BOOT_N = [0]


def boot_print(a, x, y, s=1.0, rot=0, ribs=9):
    """Apollo overshoe print: wide toe, narrow waist, straight cross ribs."""
    _BOOT_N[0] += 1
    cid = f'bp{_BOOT_N[0]}'
    sole = ('M 0,-40 C 19,-40 23,-24 21,-10 C 19,4 14,14 15,27 C 16,41 -16,41 -15,27 '
            'C -14,14 -19,4 -21,-10 C -23,-24 -19,-40 0,-40 Z')
    a(f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">')
    a(f'<defs><clipPath id="{cid}"><path d="{sole}"/></clipPath></defs>')
    a(f'<path d="{sole}" fill="#fff" {S} stroke-width="{2.5/max(s,0.4):.2f}"/>')
    a(f'<g clip-path="url(#{cid})">')
    for k in range(ribs):
        yy = -34 + k * 70 / (ribs - 1)
        a(f'<line x1="-25" y1="{yy:.1f}" x2="25" y2="{yy:.1f}" {S} stroke-width="{1.6/max(s,0.4):.2f}"/>')
    a('</g></g>')


def rock(a, x, y, r, seed=0, sw=3):
    """Irregular angular rock sitting on the ground at (x, y)."""
    import random
    rnd = random.Random(seed)
    pts = [(x - r, y)]
    for k in range(1, 6):
        t = math.pi * k / 6
        rr = r * rnd.uniform(0.6, 1.0)
        pts.append((x - r*math.cos(t)*rnd.uniform(0.85, 1.05), y - rr*math.sin(t)*0.75))
    pts.append((x + r, y))
    a(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="#fff" {S} stroke-width="{sw}"/>')
    a(f'<path d="M {x - r*0.2:.1f},{y - r*0.5:.1f} L {x + r*0.3:.1f},{y - r*0.15:.1f}" fill="none" {S} stroke-width="{sw*0.6:.1f}"/>')


# ------------------------------------------------------- rocky globes ----

def _ang(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    d = math.sin(p1)*math.sin(p2) + math.cos(p1)*math.cos(p2)*math.cos(math.radians(lon1 - lon2))
    return math.degrees(math.acos(max(-1, min(1, d))))


def night_side(a, uid, cx, cy, R, pr_view, sun_lat, sun_lon, sw=1.0):
    """Hatch the unlit hemisphere. The terminator is the great circle 90 deg from
    the subsolar point; we sample it plus the dark part of the limb."""
    sx, sy, _ = pr_view(sun_lat, sun_lon)
    term = []
    for b in range(0, 360, 3):
        la, lo = _dest(sun_lat, sun_lon, 90, b)
        x, y, v = pr_view(la, lo)
        term.append((x, y, v))
    # rotate the list so it starts at a hidden point, then keep the visible run
    k0 = next((i for i, t in enumerate(term) if not t[2]), 0)
    term = term[k0:] + term[:k0]
    vis = [(x, y) for x, y, v in term if v]
    if not vis:
        return
    a0 = math.atan2(vis[-1][1], vis[-1][0]); a1 = math.atan2(vis[0][1], vis[0][0])
    # walk the limb from the end of the terminator back to its start on the dark side
    sun_ang = math.atan2(sy, sx)
    def arc(d):
        span = (a1 - a0) % (2*math.pi) if d > 0 else -((a0 - a1) % (2*math.pi))
        return [(math.cos(a0 + span*k/40), math.sin(a0 + span*k/40)) for k in range(41)]
    cand = [arc(1), arc(-1)]
    mid = lambda c: c[20]
    limb = min(cand, key=lambda c: math.cos(math.atan2(mid(c)[1], mid(c)[0]) - sun_ang))
    pts = vis + limb
    a(f'<defs><pattern id="hatch{uid}" width="{9*sw:.1f}" height="{9*sw:.1f}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
      f'<line x1="0" y1="0" x2="0" y2="{9*sw:.1f}" stroke="#000" stroke-width="{1.6*sw:.2f}"/></pattern></defs>')
    a(f'<polygon points="{" ".join(f"{cx+R*x:.1f},{cy+R*y:.1f}" for x, y in pts)}" fill="url(#hatch{uid})" stroke="#000" stroke-width="{2.5*sw:.2f}"/>')


def cratered_globe(a, uid, cx, cy, R, lat0, lon0, body_km, named=(), n=700, seed=1, sw=1.0,
                   sun=None, basins=(), min_px=2.5, max_km=None, min_km=None, smooth=()):
    """A heavily cratered world: representative craters (power-law sizes) plus
    named features at their real coordinates. named: (lat, lon, km, peak, dark)."""
    import random
    kpd = 2 * math.pi * body_km / 360
    pr = ortho(lat0, lon0)
    P = lambda x, y: f'{cx+R*x:.1f},{cy+R*y:.1f}'
    a(f'<defs><clipPath id="g{uid}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fff" {S} stroke-width="{5*sw:.2f}"/>')
    a(f'<g clip-path="url(#g{uid})">')
    for lat, lon, km in basins:  # multi-ring impact basins
        for f in (1.0, 0.72, 0.45):
            ring = [pr(*_dest(lat, lon, km*f/2/kpd, b)) for b in range(0, 360, 4)]
            runs, cur = [], []
            for x, y, v in ring + ring[:1]:
                if v: cur.append(P(x, y))
                elif cur: runs.append(cur); cur = []
            if cur: runs.append(cur)
            for r_ in runs:
                a(f'<polyline points="{" ".join(r_)}" fill="none" {S} stroke-width="{(3 if f == 1 else 2)*sw:.2f}" {"" if f == 1 else f"stroke-dasharray={chr(34)}{8*sw:.0f} {6*sw:.0f}{chr(34)}"}/>')
    rnd = random.Random(seed)
    max_km = max_km or body_km * 0.06
    for _ in range(n):
        lat = math.degrees(math.asin(rnd.uniform(-1, 1))); lon = rnd.uniform(-180, 180)
        km = (min_km or body_km * 0.008) * (1 - rnd.random()) ** (-1 / 1.6)
        if km > max_km or not pr(lat, lon)[2] or R * km / (2*body_km) < min_px / 2:
            continue
        # smooth volcanic plains (e.g. basin interiors) are much less cratered
        if any(_ang(lat, lon, sl, so) < sr for sl, so, sr in smooth) and rnd.random() > 0.15:
            continue
        _crater(a, pr, P, lat, lon, km, sw, w=1.8, kpd=kpd)
    for lat, lon, km, peak, dark in named:
        if pr(lat, lon)[2]:
            _crater(a, pr, P, lat, lon, km, sw, dark=dark, peak=peak, kpd=kpd)
    a('</g>')
    if sun:
        a(f'<g clip-path="url(#g{uid})">')
        night_side(a, uid, cx, cy, R, pr, *sun, sw=sw)
        a('</g>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" {S} stroke-width="{5*sw:.2f}"/>')
    return pr


def zeytin_loaf(a, uid, transform):
    """Zeytin at home, no suit, in the 'loaf' pose from the photo: white chest and
    paws, a black patch on the back, long fur. Origin at the bottom centre."""
    body = 'M -165,0 C -175,-95 -105,-160 0,-160 C 105,-160 175,-105 165,0 Z'
    a(f'<g transform="{transform}">')
    a(f'<defs><clipPath id="lb{uid}"><path d="{body}"/></clipPath></defs>')
    a(f'<path d="{body}" fill="#fff" {S} stroke-width="4.5"/>')
    a(f'<g clip-path="url(#lb{uid})">')
    a('<path d="M -200,-170 L -60,-170 C -80,-110 -95,-40 -80,10 L -200,10 Z" fill="#000"/>')   # black patch on the back
    a('</g>')
    # fluffy white chest ruff
    d = 'M -70,-120'
    for k in range(8):
        d += f' q 9,{14 if k % 2 else 22} 18,{6 if k % 2 else 10}'
    a(f'<path d="{d}" fill="none" {S} stroke-width="2.5"/>')
    for x in (-40, -10, 20, 50):
        a(f'<path d="M {x},-70 q 6,12 0,24" fill="none" {S} stroke-width="2"/>')
    # front paws tucked in front
    for x in (-38, 38):
        a(f'<ellipse cx="{x}" cy="-12" rx="34" ry="17" fill="#fff" {S} stroke-width="4"/>')
        for t in (-12, 0, 12):
            a(f'<line x1="{x + t}" y1="-2" x2="{x + t}" y2="-10" {S} stroke-width="2"/>')
    zeytin_head(a, uid, 'translate(0,-200) scale(0.72)', sw=1.3)
    a('</g>')
