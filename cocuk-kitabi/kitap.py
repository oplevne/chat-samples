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
    """Zeytin: long-haired, mostly white, black ear + head patch, pirate eye patch.
    Drawn around (0,0); sw scales stroke widths for small sizes."""
    st = lambda w: f'{S} stroke-width="{w*sw:.2f}"'
    head = _fluffy_head_path()
    a(f'<g transform="{transform}">')
    a(f'<defs><clipPath id="hc{uid}"><path d="{head}"/></clipPath></defs>')
    # ears (behind head): left white, right black
    for sg, fill in ((-1, '#fff'), (1, '#000')):
        a(f'<path d="M {sg*118},-40 Q {sg*118},-130 {sg*100},-182 Q {sg*60},-150 {sg*30},-98 Z" fill="{fill}" {st(4.5)}/>')
        a(f'<path d="M {sg*100},-62 Q {sg*102},-120 {sg*96},-152 Q {sg*70},-128 {sg*55},-95 Z" fill="#fff" {st(3)}/>')
        for dx, dy in ((88, -110), (78, -95)):
            a(f'<path d="M {sg*dx},{dy} q {sg*-6},-14 {sg*-2},-26" fill="none" {st(2.5)}/>')
    a(f'<path d="{head}" fill="#fff" {st(4.5)}/>')
    a(f'<g clip-path="url(#hc{uid})">')
    # black fur patch over the right side of the forehead
    a('<path d="M 10,-120 C 30,-60 70,-35 115,-40 C 150,-45 150,-120 120,-140 Z" fill="#000"/>')
    # pirate patch strap
    a(f'<path d="M -130,-22 L -70,-2" fill="none" {st(8)}/>')
    a(f'<path d="M -32,-12 L 40,-130" fill="none" {st(8)}/>')
    a('</g>')
    # cheek fur strokes
    for sg in (-1, 1):
        a(f'<path d="M {sg*112},20 q {sg*-12},10 {sg*-6},26" fill="none" {st(2.5)}/>')
        a(f'<path d="M {sg*100},55 q {sg*-12},8 {sg*-8},22" fill="none" {st(2.5)}/>')
    a(f'<path d="M -12,108 q 6,-12 0,-22 M 12,108 q -6,-12 0,-22" fill="none" {st(2.5)}/>')
    # pirate eye patch (cat's right eye, viewer's left)
    a(f'<ellipse cx="-50" cy="12" rx="34" ry="30" fill="#000" {st(3)}/>')
    # open eye (viewer's right) — olive green in the colour version
    a(f'<ellipse cx="50" cy="12" rx="26" ry="31" fill="#fff" {st(4)}/>')
    a('<ellipse cx="52" cy="15" rx="13" ry="22" fill="#000"/>')
    a('<circle cx="58" cy="2" r="6" fill="#fff"/>')
    # nose, mouth, whiskers
    a(f'<path d="M -11,38 L 11,38 L 0,50 Z" fill="#fff" {st(3.5)}/>')
    a(f'<path d="M 0,50 L 0,58 M -17,61 Q -8,70 0,58 Q 8,70 17,61" fill="none" {st(3.5)}/>')
    for sg in (-1, 1):
        for y0, y1 in ((48, 30), (56, 58), (64, 86)):
            a(f'<path d="M {sg*38},{y0} Q {sg*90},{(y0+y1)/2-4} {sg*140},{y1}" fill="none" {st(2.5)}/>')
    a('</g>')


def shuttle_side(a, transform, uid='s'):
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
    zeytin_head(a, uid, 'translate(450,10) scale(0.27)', sw=2.2)
    a('</g>')
    a(f'<circle cx="450" cy="-5" r="46" fill="none" {S} stroke-width="3.5"/>')
    a('</g>')
