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
        bw = 24 + 10.5 * len(badge)
        a(f'<rect x="40" y="28" width="{bw:.0f}" height="36" rx="18" fill="#fff" {S} stroke-width="3"/>')
        a(f'<text x="{40+bw/2:.0f}" y="52" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="18" fill="#000">{badge}</text>')
    assert y < H - 38, f'story too long ({y})'


def save(o, path):
    o.append('</svg>')
    open(path, 'w').write('\n'.join(o))
