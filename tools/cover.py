"""Build the UserStyles.world cover: the home page cut into diagonal shards,
each shard a different accent colour, Slate last, the theme name overlaid.

Usage: python tools/cover.py <shots dir> <out.png> <shot ...>
The shots are full-window browser screenshots of the home page in display
order (left to right); the browser chrome is cropped off the top.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

shots_dir, out, *names = sys.argv[1:]
CHROME = 82                 # browser tab + address bar height in the shots
SCROLLBAR = 18              # the window's scrollbar at the right edge of the shots
W, H = 1600, 900            # cover size (16:9)
SLANT = 150                 # how far each cut leans, top to bottom
GAP = 3                     # light seam between shards
AA = 4                      # supersampling for the cuts: ImageDraw has no antialiasing
GLOW = 12                   # width of the glow line before blurring
GLOW_BLUR = 6               # blur radius of the glow
GLOW_ALPHA = 200            # strength of the glow (coloured, so it can be stronger than white)

def accent_of(im):
    """The accent colour of a shot: the most saturated pixel around the
    diamond marker beside the FANFICTION heading (at ~232,219 in the
    full-window shots)."""
    best, best_sat = (255, 255, 255), -1
    for x in range(224, 241):
        for y in range(211, 228):
            r, g, b = im.getpixel((x, y))[:3]
            sat = max(r, g, b) - min(r, g, b)
            if sat > best_sat:
                best, best_sat = (r, g, b), sat
    return best

def lift(c, k):
    """Mix a colour towards white by k (0..1)."""
    return tuple(round(v + (255 - v) * k) for v in c)

# 1. load, crop the chrome, scale to the cover width, crop the top of the page
frames, accents = [], []
for n in names:
    im = Image.open(f'{shots_dir}/{n}').convert('RGB')
    accents.append(accent_of(im))
    im = im.crop((0, CHROME, im.width - SCROLLBAR, im.height))
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    frames.append(im.crop((0, 0, W, H)))

def aa_polygon(poly):
    """An antialiased L mask of a polygon: drawn at AA times the size and
    scaled down."""
    m = Image.new('L', (W * AA, H * AA), 0)
    ImageDraw.Draw(m).polygon([(x * AA, y * AA) for x, y in poly], fill=255)
    return m.resize((W, H), Image.LANCZOS)

def aa_line(pts, width):
    """An antialiased L mask of a line."""
    m = Image.new('L', (W * AA, H * AA), 0)
    ImageDraw.Draw(m).line([(x * AA, y * AA) for x, y in pts], fill=255, width=width * AA)
    return m.resize((W, H), Image.LANCZOS)

# 2. shards: parallelograms whose cuts lean right going down. The first and
#    last run off the canvas so the edges stay square.
n = len(frames)
step = (W + SLANT) / n
cover = Image.new('RGB', (W, H))
for i, fr in enumerate(frames):
    x0 = i * step - SLANT          # top-left of this cut
    x1 = (i + 1) * step - SLANT    # top-left of the next cut
    poly = [(x0, 0), (x1, 0), (x1 + SLANT, H), (x0 + SLANT, H)]
    if i == 0:
        poly = [(-SLANT, 0), (x1, 0), (x1 + SLANT, H), (-SLANT, H)]
    if i == n - 1:
        poly = [(x0, 0), (W + SLANT, 0), (W + SLANT, H), (x0 + SLANT, H)]
    cover.paste(fr, (0, 0), aa_polygon(poly))

# 3. seams: an outer glow (a wide blurred line) under a crisp line, so the
#    shards read even where two light pages meet. Each seam takes the accent
#    of the shard on its left: the glow in the accent itself, the line lifted
#    towards white so it stays visible on the dark bar.
cover = cover.convert('RGBA')
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
seams = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for i in range(1, n):
    x = i * step - SLANT
    c = accents[i - 1]
    pts = [(x, 0), (x + SLANT, H)]
    g = Image.new('RGBA', (W, H), c + (0,))
    g.putalpha(aa_line(pts, GLOW).point(lambda v: v * GLOW_ALPHA // 255))
    glow = Image.alpha_composite(glow, g)
    l = Image.new('RGBA', (W, H), lift(c, 0.55) + (0,))
    l.putalpha(aa_line(pts, GAP).point(lambda v: v * 240 // 255))
    seams = Image.alpha_composite(seams, l)
print('accents', ['#%02x%02x%02x' % a for a in accents])
glow = glow.filter(ImageFilter.GaussianBlur(GLOW_BLUR))
cover = Image.alpha_composite(cover, glow)
cover = Image.alpha_composite(cover, seams)

# 4. the wordmark: the aero gradient treatment on the glass plate (chosen
#    2026-11-12 from the three in tools/wordmark.py)
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wordmark
cover = wordmark.variant_aero(cover, accents)
cover.convert('RGB').save(out, optimize=True)
print('wrote', out, cover.size)
