"""Builds veri/ay_maria.json: near-side lunar maria outlines as (lat, lon) polylines.

Each mare is modelled as a union of spherical caps placed at its IAU centre
(selenographic lat/lon, angular radius from its diameter, 1 deg ~ 30.3 km);
irregular maria get several caps. A low-amplitude smooth noise roughens the
shorelines, then marching squares traces the outline. Run once; needs numpy +
scikit-image. The page scripts only read the JSON."""
import json, math
import numpy as np
from skimage import measure

# (lat, lon, angular radius in degrees)
CAPS = {
    'Imbrium': [(33, -16, 17)],
    'Iridum': [(44.5, -31.5, 5)],
    'Serenitatis': [(28, 17.5, 10.5)],
    'Somniorum': [(38, 29, 4)],
    'Tranquillitatis': [(8.5, 31.4, 11), (15, 25, 6), (3, 40, 7), (-2, 26, 4)],
    'Crisium': [(17, 59, 8)],
    'Fecunditatis': [(-8, 52, 9.5), (-2, 47, 6), (-15, 53, 5)],
    'Nectaris': [(-15.2, 35.5, 5.2)],
    'Vaporum': [(13.3, 3.6, 4)],
    'Medii': [(2.4, 1.7, 3)],
    'Aestuum': [(11, -8.5, 3.5)],
    'Insularum': [(7.5, -30.9, 8)],
    'Cognitum': [(-10, -23.1, 6)],
    'Nubium': [(-21.3, -16.6, 10.5)],
    'Humorum': [(-24.4, -38.6, 6.3)],
    'Procellarum': [(-2, -50, 7), (8, -55, 9), (20, -58, 10), (30, -56, 9), (40, -50, 7),
                    (15, -45, 8), (27, -45, 7), (45, -42, 5), (-8, -42, 5),
                    (36, -36, 6), (5, -38, 5), (-5, -31, 4)],
    'Frigoris': [(57, -40, 4), (57, -27, 4.5), (56, -14, 4), (56, 0, 4), (57, 14, 4), (58, 28, 3.5), (58, 40, 3)],
    'Undarum': [(7, 69, 3)], 'Spumans': [(1, 65, 2.2)],
    'Marginis': [(13.3, 86.1, 4)], 'Smythii': [(1.3, 87.5, 5)],
    'Australe': [(-39, 93, 9)], 'Orientale': [(-19.4, -92.8, 5)],
}


def ang(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    d = np.sin(p1)*np.sin(p2) + np.cos(p1)*np.cos(p2)*np.cos(np.radians(lon1-lon2))
    return np.degrees(np.arccos(np.clip(d, -1, 1)))


step = 0.25
lats = np.arange(-89, 89 + step, step)
lons = np.arange(-110, 110 + step, step)
LON, LAT = np.meshgrid(lons, lats)
# metaball field: each cap is a Gaussian equal to 0.5 at its radius, so
# neighbouring caps merge into one organic shoreline instead of a chain of circles
# (caps of the same mare are summed; different maria are combined with max,
# so separate maria only join where they really touch)
field = np.zeros(LAT.shape)
for caps in CAPS.values():
    mare = np.zeros(LAT.shape)
    for la, lo, r in caps:
        mare += np.exp(-np.log(2) * (ang(LAT, LON, la, lo) / r) ** 4)
    field = np.maximum(field, mare)
field = np.minimum(field, 1.2) - 0.5
# fractal noise roughens the shorelines (larger scales first)
rng = np.random.default_rng(11)
noise = np.zeros_like(field)
for octave in range(5):
    freq, amp = 0.08 * 2 ** octave, 0.5 ** octave
    for _ in range(4):
        th, ph = rng.uniform(0, np.pi), rng.uniform(0, 2*np.pi)
        noise += amp * np.sin(freq * (LON*np.cos(th) + LAT*np.sin(th)) + ph)
field += 0.07 * noise
lines = []
for c in measure.find_contours(field, 0.0):
    if len(c) < 12:
        continue
    pts = [(round(float(lats[0] + r*step), 2), round(float(lons[0] + q*step), 2)) for r, q in c[::3]]
    pts.append(pts[0])
    lines.append(pts)
json.dump(lines, open('veri/ay_maria.json', 'w'))
print(len(lines), 'outlines')
