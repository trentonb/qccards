"""QC Cards app icon: three upright cards in a shallow fan on the app's dark background with its red and green
corner glows. Each card carries the three measure chips (pressure blue, starch pink, solids amber), as the
real cards do.

Writes icon.svg. The PNGs (icon-512, icon-180, icon-64) are rendered from it in a browser, with the rounded
corners squared off, because iOS and Android round app icons themselves."""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BG = (20, 20, 19)
CARD = (34, 34, 32); EDGE = (74, 74, 70); FRONT_EDGE = (236, 235, 229)
CHIPS = [(55, 138, 221), (212, 83, 126), (186, 117, 23)]
INK = (246, 245, 240)

# card geometry in a 512 square; all art stays inside the central 80% so the maskable crop never cuts it
CW, CH, R = 148, 236, 24
PIVOT_Y = 1450             # far below: a shallow arc, like the app's hand of cards
FAN = [(-5.6, .78), (5.6, .78), (0, 1.0)]   # (angle, brightness); the front card is drawn last


# the same design as SVG, for browser tabs
def chip_svg(x, y, c, i):
    vw = 56 if i != 1 else 44
    return (f'<rect x="{x}" y="{y}" width="{CW - 28}" height="44" rx="11" fill="{c}"/>'
            f'<rect x="{x + 11}" y="{y + 14}" width="{vw - 11}" height="16" rx="6" fill="#f6f5f0"/>'
            f'<polyline points="{x + CW - 28 - 46},{y + 28} {x + CW - 28 - 34},{y + 20} {x + CW - 28 - 24},{y + 26} {x + CW - 28 - 12},{y + 16}" fill="none" stroke="#f6f5f0" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')

def card_svg(ang, bright, front):
    x0, y0 = 256 - CW / 2, 402 - CH
    body = (f'<rect x="{x0}" y="{y0}" width="{CW}" height="{CH}" rx="{R}" fill="#222220" stroke="{"#ecebe5" if front else "#4a4a46"}" stroke-width="{4 if front else 3}"/>'
            f'<rect x="{x0 + 14}" y="{y0 + 20}" width="78" height="14" rx="7" fill="#f6f5f0" opacity=".9"/>'
            f'<rect x="{x0 + 14}" y="{y0 + 42}" width="48" height="10" rx="5" fill="#96958e"/>'
            + ''.join(chip_svg(x0 + 14, y0 + 72 + i * 53, c, i) for i, c in enumerate(['#378ADD', '#D4537E', '#BA7517'])))
    op = '' if bright >= 1 else f' opacity="{bright + .1:.2f}"'
    rot = f' transform="rotate({ang} 256 {PIVOT_Y})"' if ang else ''
    return f'<g{rot}{op} filter="url(#sh)">{body}</g>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="4" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".55"/></filter>
    <radialGradient id="w" cx="50%" cy="112%" r="60%"><stop offset="0" stop-color="#ba7517" stop-opacity=".22"/><stop offset="1" stop-color="#ba7517" stop-opacity="0"/></radialGradient>
    <radialGradient id="r" cx="8%" cy="4%" r="70%"><stop offset="0" stop-color="#d63031" stop-opacity=".42"/><stop offset="1" stop-color="#d63031" stop-opacity="0"/></radialGradient>
    <radialGradient id="g" cx="94%" cy="8%" r="65%"><stop offset="0" stop-color="#56a840" stop-opacity=".36"/><stop offset="1" stop-color="#56a840" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="#141413"/>
  <rect width="512" height="512" rx="112" fill="url(#r)"/>
  <rect width="512" height="512" rx="112" fill="url(#g)"/>
  <rect width="512" height="512" rx="112" fill="url(#w)"/>
  {''.join(card_svg(a, b, a == 0) for a, b in FAN)}
</svg>
'''
open(os.path.join(OUT, 'icon.svg'), 'w', encoding='utf-8', newline='\n').write(svg)
print('icons written')
