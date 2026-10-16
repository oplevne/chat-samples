"""Assemble the KDP interior PDF (8.5 x 11 in, no bleed).

Every page's artwork is scaled to 92% and nudged away from the binding, so all
content sits inside KDP's margins: >= 0.375 in on the gutter side and >= 0.25 in
on the outside, top and bottom. Odd pages are right-hand pages (gutter on the left)."""
import os, subprocess, sys

stops = ['01-dunya', '02-ay', '03-gunes', '04-merkur', '05-venus', '06-mars', '07-asteroit',
         '08-jupiter', '09-saturn', '10-uranus', '11-neptun', '12-pluton', '13-eve-donus']
pages = ['sayfalar/00a-baslik.svg', 'sayfalar/00b-sahip.svg', 'karakter-zeytin.svg']
for s in stops:
    pages += [f'sayfalar/{s}-sol.svg', f'sayfalar/{s}-sag.svg']
pages.append('sayfalar/99-gezegenini-tasarla.svg')
for p in pages:
    assert os.path.exists(p), p

SC = 0.92
w, h = 8.5*SC, 11*SC
inner, outer = 0.40, 8.5 - w - 0.40     # gutter and outside margins, inches
top = (11 - h) / 2
html = ['<!doctype html><html><head><meta charset="utf-8"><style>',
        '@page { size: 8.5in 11in; margin: 0 } html, body { margin: 0 }',
        '.p { width: 8.5in; height: 11in; position: relative; page-break-after: always; overflow: hidden }',
        f'.p img {{ position: absolute; top: {top:.3f}in; width: {w:.3f}in; height: {h:.3f}in }}',
        '</style></head><body>']
for i, p in enumerate(pages, start=1):
    left = inner if i % 2 == 1 else outer
    html.append(f'<div class="p"><img style="left:{left:.3f}in" src="{p}"></div>')
html.append('</body></html>')
os.makedirs('cikti', exist_ok=True)
open('cikti/ic-sayfalar.html', 'w').write('\n'.join(html))
print(len(pages), 'pages; margins (in): gutter', inner, 'outside', round(outer, 3), 'top/bottom', round(top, 3))
