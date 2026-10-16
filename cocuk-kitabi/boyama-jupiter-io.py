import math, sys
W,H=850,1100
JX,JY,JR=300,620,230
IX,IY,IR=720,620,55
S='stroke="#000" stroke-linejoin="round" stroke-linecap="round"'
o=[]
a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a(f'<defs><clipPath id="jc"><circle cx="{JX}" cy="{JY}" r="{JR-2}"/></clipPath></defs>')
# illustration area is scaled up to leave room for the story text below
SC=0.7
a(f'<g transform="translate({W*(1-SC)/2:.1f},0) scale({SC})">')

def star(cx,cy,r,sw=3.5):
    pts=[]
    for i in range(10):
        ang=-math.pi/2+i*math.pi/5
        rr=r if i%2==0 else r*0.45
        pts.append(f'{cx+rr*math.cos(ang):.1f},{cy+rr*math.sin(ang):.1f}')
    a(f'<polygon points="{" ".join(pts)}" fill="#fff" {S} stroke-width="{sw}"/>')

# stars and dots
for cx,cy,r in [x for x in [(80,90,26),(250,70,18),(410,150,30),(120,280,20),(330,300,14),(780,410,22),(70,880,22),(790,880,20),(560,1070,0),(60,560,16),(810,760,18),(470,880,14),(190,920,14)] if x[2]]:
    star(cx,cy,r)
for cx,cy,r in [(180,170,6),(470,60,5),(40,400,5),(560,380,6),(800,560,5),(620,880,6),(330,1075,0),(700,1075,0),(40,740,5),(250,880,0)]:
    if r: a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" {S} stroke-width="3"/>')

# dipole field lines Jupiter<->Io (flux tube)
def fl(L):
    lam0=math.acos(math.sqrt(JR/L))
    for sgn in (1,-1):
        pts=[]
        n=80
        for i in range(n+1):
            lam=sgn*lam0*(1-i/n)
            r=L*math.cos(lam)**2
            pts.append(f'{JX+r*math.cos(lam):.1f},{JY-r*math.sin(lam):.1f}')
        a(f'<polyline points="{" ".join(pts)}" fill="none" {S} stroke-width="4"/>')
for L in (385,420,455): fl(L)

def bolt(cx,cy,s,rot):
    a(f'<path transform="translate({cx},{cy}) rotate({rot}) scale({s})" d="M -6,-36 L 14,-36 L 4,-8 L 16,-8 L -8,36 L -2,4 L -14,4 Z" fill="#fff" {S} stroke-width="{3.5/s:.2f}"/>')
bolt(555,468,1.15,15); bolt(555,772,1.15,165); bolt(650,525,0.85,35); bolt(650,715,0.85,145)
# little sparks
def spark(cx,cy,r):
    for k in range(4):
        ang=k*math.pi/4*2+math.pi/4
        a(f'<line x1="{cx+r*0.35*math.cos(ang):.1f}" y1="{cy+r*0.35*math.sin(ang):.1f}" x2="{cx+r*math.cos(ang):.1f}" y2="{cy+r*math.sin(ang):.1f}" {S} stroke-width="3"/>')
for cx,cy in [(500,430),(500,810),(610,590),(605,655)]: spark(cx,cy,14)

# Jupiter
a(f'<circle cx="{JX}" cy="{JY}" r="{JR}" fill="#fff" {S} stroke-width="6"/>')
a('<g clip-path="url(#jc)">')
for lat in (32,20,8,-6,-14,-32):
    y=JY-JR*math.sin(math.radians(lat)); w=JR*math.cos(math.radians(lat))+10
    # wavy band edge
    d=f'M {JX-w:.1f},{y:.1f}'
    n=8
    for i in range(n):
        x1=JX-w+(i+0.5)*2*w/n; x2=JX-w+(i+1)*2*w/n
        d+=f' Q {x1:.1f},{y+(7 if i%2 else -7)+10*math.sin(math.pi*(i+0.5)/n):.1f} {x2:.1f},{y+10*math.sin(math.pi*(i+1)/n):.1f}'
    a(f'<path d="{d}" fill="none" {S} stroke-width="4"/>')
# aurora rings at the flux-tube footprints
lam=math.degrees(math.acos(math.sqrt(JR/420)))
for sgn in (1,-1):
    y=JY-sgn*JR*math.sin(math.radians(lam)); rx=JR*math.cos(math.radians(lam))
    a(f'<ellipse cx="{JX}" cy="{y:.1f}" rx="{rx+6:.1f}" ry="30" fill="none" {S} stroke-width="4"/>')
    a(f'<ellipse cx="{JX}" cy="{y:.1f}" rx="{rx-14:.1f}" ry="16" fill="none" {S} stroke-width="4"/>')
a('</g>')
# Great Red Spot
a(f'<ellipse cx="370" cy="709" rx="52" ry="23" fill="#fff" {S} stroke-width="4.5"/>')
a(f'<ellipse cx="370" cy="709" rx="30" ry="11" fill="none" {S} stroke-width="3.5"/>')
# small storm ovals
a(f'<ellipse cx="200" cy="640" rx="22" ry="9" fill="#fff" {S} stroke-width="3.5"/>')
a(f'<ellipse cx="250" cy="577" rx="16" ry="7" fill="#fff" {S} stroke-width="3.5"/>')

# Io volcanic plume (umbrella, normal to surface)
vx,vy=IX+IR*math.cos(math.radians(-55)),IY+IR*math.sin(math.radians(-55))
a(f'<g transform="translate({vx:.1f},{vy:.1f}) rotate(35)">')
a(f'<path d="M -62,6 C -66,-70 66,-70 62,6 C 50,-28 -50,-28 -62,6 Z" fill="#fff" {S} stroke-width="4"/>')
for d in ['M 0,6 C -6,-20 -20,-36 -34,-40','M 0,6 C 0,-20 0,-36 0,-44','M 0,6 C 6,-20 20,-36 34,-40']:
    a(f'<path d="{d}" fill="none" {S} stroke-width="3"/>')
for px,py in [(-70,22),(70,22),(-58,32),(58,32)]:
    a(f'<circle cx="{px}" cy="{py}" r="3.5" fill="#fff" {S} stroke-width="2.5"/>')
a('</g>')
# Io
a(f'<circle cx="{IX}" cy="{IY}" r="{IR}" fill="#fff" {S} stroke-width="5"/>')
import random; random.seed(4)
for cx,cy,r in [(698,598,13),(738,640,10),(700,650,8),(745,600,7)]:
    pts=[]
    for k in range(9):
        ang=k*2*math.pi/9; rr=r*(0.75+0.5*random.random())
        pts.append(f'{cx+rr*math.cos(ang):.1f},{cy+rr*math.sin(ang):.1f}')
    a(f'<polygon points="{" ".join(pts)}" fill="#fff" {S} stroke-width="3"/>')

# Space shuttle (top view), nose toward the scene
a('<g transform="translate(615,215) rotate(150) scale(1.05)">')
# flames
for y0,s in [(-12,1),(0,1.25),(12,1)]:
    a(f'<path d="M -104,{y0-6} Q {-130*s},{y0-12} {-150*s},{y0} Q {-130*s},{y0+12} -104,{y0+6} Z" fill="#fff" {S} stroke-width="3"/>')
for sg in (1,-1):
    a(f'<path d="M 25,{22*sg} L -62,{88*sg} L -96,{88*sg} L -92,{22*sg} Z" fill="#fff" {S} stroke-width="4.5"/>')
    a(f'<path d="M -55,{70*sg} L -88,{70*sg}" fill="none" {S} stroke-width="3"/>')
    a(f'<circle cx="-40" cy="{48*sg}" r="10" fill="#fff" {S} stroke-width="3"/>')
for y0 in (-12,0,12):
    a(f'<rect x="-108" y="{y0-5}" width="16" height="10" rx="2" fill="#fff" {S} stroke-width="3"/>')
a(f'<path d="M -94,-22 L 60,-22 Q 112,-20 128,0 Q 112,20 60,22 L -94,22 Z" fill="#fff" {S} stroke-width="5"/>')
a(f'<rect x="-78" y="-13" width="118" height="26" rx="3" fill="none" {S} stroke-width="3"/>')
a(f'<line x1="-78" y1="0" x2="40" y2="0" {S} stroke-width="3"/>')
a(f'<path d="M 70,-12 L 92,-9 L 92,9 L 70,12 Z" fill="#fff" {S} stroke-width="3"/>')
a(f'<line x1="81" y1="-10.5" x2="81" y2="10.5" {S} stroke-width="2.5"/>')
a('</g>')

a('</g>')

# title (outlined, colorable) and story
a(f'<text x="{W/2}" y="712" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#fff" stroke="#000" stroke-width="2.2" stroke-linejoin="round">The Magnetic Dance</text>')
import textwrap
story=["Every 42 hours, little Io dances once around giant Jupiter, always facing its partner and holding hands through an invisible magnetic bond.",
       "As Jupiter spins, its magnetic field sweeps past Io, and an electric current of about a million amperes flows along their bond like a sparkling ribbon.",
       "Where the ribbon touches Jupiter's poles, glowing auroras light up — the shining footprints of Io's dance!"]
y=768
for para in story:
    for line in textwrap.wrap(para,60):
        a(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="DejaVu Sans" font-size="23" fill="#000">{line}</text>')
        y+=31
    y+=8
a('</svg>')
open(sys.argv[1],'w').write('\n'.join(o))
