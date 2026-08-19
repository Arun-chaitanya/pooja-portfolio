#!/usr/bin/env python3
"""Rebuild assets/friend-paper.png (home-page hero) from its two layers.
Usage: /usr/bin/python3 make-hero.py [PAPER_Y]   (PAPER_Y = top of the paper in px, default 128)
"""
import sys
from PIL import Image
W, H = 929, 1411
PAPER_Y = int(sys.argv[1]) if len(sys.argv) > 1 else 128
p = Image.open('assets/crumpled-paper.png').convert('RGBA')
c = Image.open('assets/pooja-cutout.png').convert('RGBA')
P = p.resize((W, round(p.height * W / p.width)), Image.LANCZOS)
C = c.resize((W, round(c.height * W / c.width)), Image.LANCZOS)
out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
out.alpha_composite(P, (0, PAPER_Y))
out.alpha_composite(C, (0, H - C.height))  # person pinned to the bottom edge
out.save('assets/friend-paper.png', optimize=True)
print('wrote assets/friend-paper.png, paper top at', PAPER_Y)
