"""Full-wrap colour cover for KDP: back + spine + front, with 0.125 in bleed.

8.5 x 11 in trim, 30 white pages -> spine 30 x 0.002252 = 0.0676 in (too thin
for spine text). Units: 100 per inch. The line-art helpers draw white fills;
the CSS below recolours them (CSS rules override SVG presentation attributes)."""
import importlib.util, math, random, sys, textwrap
from kitap import S, star, earth, shuttle_side, zeytin_body

PAGES = 30
BLEED, TRIM_W, TRIM_H = 12.5, 850.0, 1100.0
SPINE = PAGES * 0.2252
CW, CH = 2*BLEED + 2*TRIM_W + SPINE, TRIM_H + 2*BLEED
BACK_X0, SPINE_X0 = BLEED, BLEED + TRIM_W
FRONT_X0 = SPINE_X0 + SPINE
FX = FRONT_X0 + TRIM_W/2          # centre of the front cover trim

# Saturn's drawing comes from its page script
spec = importlib.util.spec_from_file_location('saturn_page', '09_saturn.py')
sat_mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(sat_mod)

o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW:.2f} {CH:.2f}" width="{CW:.2f}" height="{CH:.2f}">')
a('''<style>
.suit > g > [fill="#fff"] { fill: #eef3fb }
.suit > g > circle[r="66"] { fill: #bfe3ff }
.suit > g > path[d*="Q"][d*="Z"] { fill: #ff8a3d }
.ship > g > path:nth-child(-n+3) { fill: #ffb12e }
.ship > g > path:nth-child(4) { fill: #e5484d }
.ship > g > path[d^="M 10,-60"] { fill: #f4f6fa }
.ship > g > path[d^="M 140,40"] { fill: #e5484d }
.ship > g > rect { fill: #9aa3b5 }
.ship circle[r="54"] { fill: #9fd3ff }
.ship text { fill: #e5484d }
.earth > circle[fill="#fff"] { fill: #2f6fd0 }
.earth polygon { fill: #5fb86a; stroke: #1d4d2b }
.sat ellipse[fill="#fff"] { fill: #f0d28e }
.sat path[fill="#fff"] { fill: #e2c48a }
.sat polygon { fill: #d9b46a }
.starfield polygon { fill: #ffe36e; stroke: #b88a00 }
</style>''')
a('''<defs>
<radialGradient id="sky" cx="0.7" cy="0.35" r="0.9">
  <stop offset="0" stop-color="#2a1f6b"/><stop offset="0.55" stop-color="#121848"/><stop offset="1" stop-color="#070a24"/>
</radialGradient>
<radialGradient id="neb1" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#b04fd6" stop-opacity="0.55"/><stop offset="1" stop-color="#b04fd6" stop-opacity="0"/></radialGradient>
<radialGradient id="neb2" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#2fb8c9" stop-opacity="0.45"/><stop offset="1" stop-color="#2fb8c9" stop-opacity="0"/></radialGradient>
<radialGradient id="moonfill" cx="0.4" cy="0.4" r="0.7"><stop offset="0" stop-color="#e9e9ee"/><stop offset="1" stop-color="#9c9cab"/></radialGradient>
</defs>''')
a(f'<rect width="{CW:.2f}" height="{CH:.2f}" fill="url(#sky)"/>')
for cx, cy, r, g in ((FX + 250, 420, 420, 'neb1'), (FX - 300, 760, 380, 'neb2'), (300, 300, 380, 'neb1'), (520, 900, 360, 'neb2')):
    a(f'<ellipse cx="{cx:.0f}" cy="{cy}" rx="{r}" ry="{r*0.7:.0f}" fill="url(#{g})"/>')
rnd = random.Random(7)
for _ in range(420):   # background stars
    x, y = rnd.uniform(0, CW), rnd.uniform(0, CH)
    r = rnd.choice((0.8, 1.0, 1.3, 1.8, 2.4))
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity="{rnd.uniform(0.5, 1):.2f}"/>')

# ------------------------------------------------------------------ front ----
a('<g class="starfield">')
for x, y, r in ((FX - 330, 470, 20), (FX + 360, 760, 16), (FX - 120, 470, 12), (FX + 330, 240, 0)):
    if r: star(a, x, y, r, sw=2.5)
a('</g>')
a('<g class="sat">'); sat_mod.saturn(a, FX + 215, 560, 68, tilt=24, sw=0.8); a('</g>')
a('<g class="earth">'); earth(a, 'cov', FX - 185, 1060, 220, 30, 25, sw=1.0); a('</g>')
a('<g class="ship">'); shuttle_side(a, f'translate({FX - 400:.0f},640) rotate(-14) scale(0.48)', uid='cov'); a('</g>')
a('<g class="suit">'); zeytin_body(a, 'cov', f'translate({FX + 70:.0f},1030) scale(1.3)'); a('</g>')
T = 'font-family="DejaVu Sans" font-weight="bold" text-anchor="middle" stroke-linejoin="round" paint-order="stroke"'
a(f'<text x="{FX:.1f}" y="215" font-size="150" fill="#ffd23f" stroke="#3a1b00" stroke-width="12" {T}>ZEYTIN</text>')
a(f'<text x="{FX:.1f}" y="315" font-size="82" fill="#ffffff" stroke="#3a1b00" stroke-width="9" {T}>IN SPACE</text>')
a(f'<text x="{FX:.1f}" y="375" font-size="31" fill="#bfe3ff" {T.replace("font-weight=\"bold\" ", "")}>A Coloring Journey Through the Solar System</text>')

# ------------------------------------------------------------------- back ----
BX = BACK_X0 + TRIM_W/2
a(f'<circle cx="{BACK_X0 + 170}" cy="190" r="85" fill="url(#moonfill)" stroke="#555" stroke-width="3"/>')
for dx, dy, r in ((-25, -20, 14), (20, 25, 10), (-5, 40, 7), (35, -30, 8)):
    a(f'<circle cx="{BACK_X0 + 170 + dx}" cy="{190 + dy}" r="{r}" fill="#a8a8b6" stroke="#777" stroke-width="1.5"/>')
a('<g class="ship">'); shuttle_side(a, f'translate({BACK_X0 + 430:.0f},210) rotate(-8) scale(0.38)', uid='back'); a('</g>')
blurb = [
    "Blast off with Zeytin, a fluffy black-and-white space cat with a pirate eye patch, on a journey from Earth all the way to Pluto — and back home again!",
    "Color real science on every page: glowing auroras, footprints on the Moon, sunspots, Olympus Mons, Saturn’s icy rings, the geysers of Triton and Pluto’s giant heart.",
    "At each stop, a big detailed coloring page sits next to a short, true story packed with amazing facts.",
]
y = 380
for para in blurb:
    for line in textwrap.wrap(para, 46):
        a(f'<text x="{BX:.1f}" y="{y}" text-anchor="middle" font-family="DejaVu Sans" font-size="27" fill="#ffffff">{line}</text>')
        y += 38
    y += 18
a(f'<text x="{BX:.1f}" y="{y + 20}" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="25" fill="#ffd23f">Best with colored pencils or crayons.</text>')
# bottom-right of the back cover is left empty for KDP's barcode (2 x 1.2 in)
a('</svg>')
open('cikti/kapak.svg', 'w').write('\n'.join(o))
print(f'cover {CW/100:.4f} x {CH/100:.4f} in, spine {SPINE/100:.4f} in, text bottom y={y + 20}')
