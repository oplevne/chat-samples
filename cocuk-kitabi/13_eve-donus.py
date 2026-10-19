"""Stop 13 — home: the Pale Blue Dot, and Zeytin back in Istanbul."""
import math, random
from kitap import S, W, star, dot, moon, shuttle_side, zeytin_loaf, svg_open, story_block, save

# ------------------------------------------------------------ right page ----
# After Voyager 1's "Pale Blue Dot" (14 Feb 1990, ~6 billion km): bands of
# scattered sunlight across the frame, and Earth a tiny dot inside one of them.
o = svg_open(); a = o.append
rnd = random.Random(1)
for k, (x0, w) in enumerate(((150, 60), (300, 95), (470, 70), (600, 120), (760, 50))):
    sk = 90
    pts = [(x0, -10), (x0 + w, -10), (x0 + w + sk*0.93, 640), (x0 + sk*0.93, 640)]
    a(f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="#fff" {S} stroke-width="2.2"/>')
    for j in range(2):
        xs = x0 + w*(0.3 + 0.4*j)
        a(f'<line x1="{xs:.0f}" y1="-10" x2="{xs + sk*0.93:.0f}" y2="640" {S} stroke-width="1" stroke-dasharray="3 9"/>')
# the dot: about one pixel in Voyager's picture
EX, EY = 562, 400
a(f'<circle cx="{EX}" cy="{EY}" r="3.5" fill="#fff" {S} stroke-width="2"/>')
a(f'<circle cx="{EX}" cy="{EY}" r="24" fill="none" {S} stroke-width="2.5"/>')
a(f'<line x1="{EX + 17}" y1="{EY + 17}" x2="{EX + 60}" y2="{EY + 60}" {S} stroke-width="2.5"/>')
a(f'<text x="{EX + 64}" y="{EY + 80}" font-family="DejaVu Sans" font-weight="bold" font-size="20" fill="#000">You are here!</text>')
shuttle_side(a, 'translate(70,600) rotate(-8) scale(0.28)', uid='r')
story_block(a, "The Pale Blue Dot", [
    "Before heading home, Zeytin turns around for one last look — and Earth is just a tiny, pale blue dot.",
    "In 1990, the Voyager 1 spacecraft took a picture just like this from about 6 billion kilometers away.",
    "Everyone who has ever lived is on that little dot. Let’s take good care of it!"],
    badge="Heading home")
save(o, 'sayfalar/13-eve-donus-sag.svg')

# ------------------------------------------------------------- left page ----
o = svg_open(); a = o.append
WX0, WY0, WX1, WY1 = 90, 70, 760, 800
# night view of Istanbul through the window
a(f'<defs><clipPath id="win"><rect x="{WX0}" y="{WY0}" width="{WX1 - WX0}" height="{WY1 - WY0}"/></clipPath></defs>')
a('<g clip-path="url(#win)">')
moon(a, 'w', 590, 210, 70, sw=0.55, texture=True)
for sx, sy, r in ((180, 140, 12), (320, 230, 9), (440, 120, 14), (720, 380, 10), (150, 330, 9), (470, 300, 8)):
    star(a, sx, sy, r, sw=2.5)
WL = 640   # the Bosphorus
a(f'<line x1="{WX0}" y1="{WL}" x2="{WX1}" y2="{WL}" {S} stroke-width="3"/>')
for k in range(7):
    x = WX0 + 40 + k*95
    a(f'<path d="M {x},{WL + 30 + (k % 3)*25} q 15,-6 30,0 q 15,6 30,0" fill="none" {S} stroke-width="2"/>')
# Bosphorus Bridge: two towers, main cable, deck
for tx in (420, 700):
    a(f'<path d="M {tx - 10},{WL} L {tx - 7},{WL - 210} L {tx + 7},{WL - 210} L {tx + 10},{WL}" fill="#fff" {S} stroke-width="3"/>')
    a(f'<line x1="{tx - 8}" y1="{WL - 120}" x2="{tx + 8}" y2="{WL - 120}" {S} stroke-width="3"/>')
a(f'<path d="M 330,{WL - 40} Q 380,{WL - 120} 420,{WL - 205} Q 560,{WL - 50} 700,{WL - 205} Q 740,{WL - 120} {WX1 + 10},{WL - 60}" fill="none" {S} stroke-width="3"/>')
a(f'<line x1="330" y1="{WL - 40}" x2="{WX1 + 10}" y2="{WL - 40}" {S} stroke-width="4"/>')
for x in range(440, 700, 26):
    t = (x - 420) / 280
    yc = (1 - t)**2*(WL - 205) + 2*t*(1 - t)*(WL - 50) + t*t*(WL - 205)
    a(f'<line x1="{x}" y1="{yc:.0f}" x2="{x}" y2="{WL - 40}" {S} stroke-width="1.4"/>')
# Galata Tower: stone cylinder, arched windows, balcony, conical cap
GX = 220
a(f'<rect x="{GX - 38}" y="{WL - 250}" width="76" height="250" fill="#fff" {S} stroke-width="3.5"/>')
for y in range(WL - 225, WL - 30, 48):
    a(f'<path d="M {GX - 8},{y + 22} L {GX - 8},{y + 6} Q {GX},{y - 4} {GX + 8},{y + 6} L {GX + 8},{y + 22} Z" fill="#fff" {S} stroke-width="2"/>')
a(f'<rect x="{GX - 48}" y="{WL - 285}" width="96" height="36" fill="#fff" {S} stroke-width="3.5"/>')
for x in range(GX - 40, GX + 41, 16):
    a(f'<path d="M {x},{WL - 252} L {x},{WL - 268} Q {x + 5},{WL - 276} {x + 10},{WL - 268} L {x + 10},{WL - 252}" fill="none" {S} stroke-width="1.8"/>')
a(f'<path d="M {GX - 46},{WL - 285} L {GX},{WL - 375} L {GX + 46},{WL - 285} Z" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<line x1="{GX}" y1="{WL - 375}" x2="{GX}" y2="{WL - 395}" {S} stroke-width="2.5"/>')
# a mosque on the far shore: domes and two minarets
MX = 560
a(f'<path d="M {MX - 70},{WL - 40} L {MX - 70},{WL - 80} Q {MX},{WL - 160} {MX + 70},{WL - 80} L {MX + 70},{WL - 40}" fill="#fff" {S} stroke-width="3"/>')
for dx in (-95, 95):
    a(f'<path d="M {MX + dx - 25},{WL - 40} L {MX + dx - 25},{WL - 62} Q {MX + dx},{WL - 100} {MX + dx + 25},{WL - 62} L {MX + dx + 25},{WL - 40}" fill="#fff" {S} stroke-width="2.5"/>')
for dx in (-140, 140):
    a(f'<path d="M {MX + dx - 6},{WL - 40} L {MX + dx - 6},{WL - 230} L {MX + dx},{WL - 262} L {MX + dx + 6},{WL - 230} L {MX + dx + 6},{WL - 40}" fill="#fff" {S} stroke-width="2.5"/>')
    a(f'<line x1="{MX + dx - 10}" y1="{WL - 170}" x2="{MX + dx + 10}" y2="{WL - 170}" {S} stroke-width="2.5"/>')
a('</g>')
# window frame, mullions, curtains, sill
a(f'<rect x="{WX0}" y="{WY0}" width="{WX1 - WX0}" height="{WY1 - WY0}" fill="none" {S} stroke-width="10"/>')
a(f'<line x1="{(WX0 + WX1)/2}" y1="{WY0}" x2="{(WX0 + WX1)/2}" y2="{WY1}" {S} stroke-width="7"/>')
for side, x in ((-1, WX0), (1, WX1)):
    pts = f'M {x - side*30},{WY0 - 20} '
    pts += ' '.join(f'Q {x + side*(20 if k % 2 else -10)},{WY0 + 60 + k*90} {x + side*(5 if k % 2 else 25)},{WY0 + 100 + k*90}' for k in range(8))
    pts += f' L {x - side*40},{WY1 + 60} L {x - side*40},{WY0 - 20} Z'
    a(f'<path d="{pts}" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<rect x="40" y="{WY1}" width="770" height="40" rx="6" fill="#fff" {S} stroke-width="5"/>')
# blanket draped over the sill, Zeytin on top, the space helmet resting beside
a(f'<path d="M 230,{WY1 + 4} L 620,{WY1 + 4} L 640,{WY1 + 190} Q 600,{WY1 + 175} 560,{WY1 + 200} Q 500,{WY1 + 180} 440,{WY1 + 205} Q 370,{WY1 + 180} 310,{WY1 + 200} Q 260,{WY1 + 180} 215,{WY1 + 195} Z" fill="#fff" {S} stroke-width="4"/>')
for x in (300, 380, 460, 540):
    a(f'<path d="M {x},{WY1 + 50} q 10,60 0,130" fill="none" {S} stroke-width="2"/>')
zeytin_loaf(a, 'home', f'translate(420,{WY1 + 4}) scale(0.95)')
a(f'<circle cx="690" cy="{WY1 - 55}" r="52" fill="#fff" {S} stroke-width="4.5"/>')
a(f'<ellipse cx="690" cy="{WY1 - 6}" rx="44" ry="10" fill="#fff" {S} stroke-width="4"/>')
a(f'<path d="M 655,{WY1 - 85} A 40 40 0 0 1 690,{WY1 - 102}" fill="none" {S} stroke-width="3"/>')
save(o, 'sayfalar/13-eve-donus-sol.svg')
