"""Prepare listing screenshots: crop the browser chrome off full-window
shots and scale them to the cover's width.

Usage: python tools/shots.py <shots dir> <out dir> name=file [name=file ...]
"""
import sys
from PIL import Image

CHROME = 82     # tab strip + address bar in the shots
SCROLLBAR = 18  # the window's scrollbar at the right edge
W = 1600

shots_dir, out_dir, *pairs = sys.argv[1:]
for pair in pairs:
    name, file = pair.split('=', 1)
    im = Image.open(f'{shots_dir}/{file}').convert('RGB')
    im = im.crop((0, CHROME, im.width - SCROLLBAR, im.height))
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{out_dir}/{name}.png', optimize=True)
    print(name, im.size)
