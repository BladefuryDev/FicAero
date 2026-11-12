"""Glossy FicAero wordmarks for the cover, rendered with Pillow.

Each variant takes the cover (RGBA) and the shard accents and returns the
cover with the title composited bottom-left.

  aero      sky-to-blue gradient fill, glass band, white top edge, blue glow,
            on the dark glass plate with the tagline
  spectrum  fill is a left-to-right gradient through the shard accents,
            glass band and edge, on the plate
  mirror    "Fic" white and "Aero" in the aero gradient, no plate: a soft
            dark halo behind the word and a fading reflection beneath it

Run directly for a comparison sheet: python tools/wordmark.py <cover.png> <out.png>
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

GLOW_BLUR = 22          # outer glow blur radius
GLOW_STRENGTH = 90      # outer glow peak alpha (0..255)

FONT_B = 'C:/Windows/Fonts/segoeuib.ttf'
FONT_R = 'C:/Windows/Fonts/segoeui.ttf'
TITLE, TAGLINE = 'FicAero', 'A FanFiction.net theme in the 2000s Aero look'


def text_mask(text, font, pad=40):
    """An L mask of the text with padding, and the text's box inside it."""
    x0, y0, x1, y1 = font.getbbox(text)
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((pad - x0, pad - y0), text, font=font, fill=255)
    return m, (pad, pad, pad + x1 - x0, pad + y1 - y0)


def vgradient(size, stops):
    """Vertical gradient; stops = [(t, (r,g,b)), ...] with t in 0..1."""
    w, h = size
    im = Image.new('RGB', (1, h))
    px = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / max(1e-6, t1 - t0)
                px[0, y] = tuple(round(a + (b - a) * k) for a, b in zip(c0, c1))
                break
    return im.resize((w, h))


def hgradient(size, colours):
    w, h = size
    im = Image.new('RGB', (w, 1))
    px = im.load()
    n = len(colours) - 1
    for x in range(w):
        t = x / max(1, w - 1) * n
        i = min(int(t), n - 1)
        k = t - i
        px[x, 0] = tuple(round(a + (b - a) * k) for a, b in zip(colours[i], colours[i + 1]))
    return im.resize((w, h))


def glossy(mask, box, fill, glow=(47, 111, 219), edge=True):
    """Build an RGBA word from a text mask: fill image, glass band over the
    top half of the glyphs, a white edge along the top, and an outer glow."""
    w, h = mask.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # outer glow: wide and faint, a hint of colour on the surface behind
    g = Image.new('RGBA', (w, h), glow + (0,))
    g.putalpha(mask.filter(ImageFilter.GaussianBlur(GLOW_BLUR)).point(lambda v: v * GLOW_STRENGTH // 255))
    out = Image.alpha_composite(out, g)
    # fill
    body = fill.convert('RGBA')
    body.putalpha(mask)
    out = Image.alpha_composite(out, body)
    # glass band: white over the upper 46% of the glyph box, hard bottom edge
    x0, y0, x1, y1 = box
    band = Image.new('L', (w, h), 0)
    ImageDraw.Draw(band).rectangle((0, 0, w, y0 + (y1 - y0) * 0.46), fill=255)
    band = ImageChops.multiply(band, mask)
    glass = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    glass.putalpha(band.point(lambda v: v * 72 // 255))
    out = Image.alpha_composite(out, glass)
    if edge:
        # white hairline along the top edges: the mask minus itself shifted down
        shifted = ImageChops.offset(mask, 0, 2)
        rim = ImageChops.subtract(mask, shifted)
        hl = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        hl.putalpha(rim.point(lambda v: v * 190 // 255))
        out = Image.alpha_composite(out, hl)
    return out


def shadow_for(mask, dy=8, blur=10, alpha=150):
    w, h = mask.size
    s = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    s.putalpha(ImageChops.offset(mask, 0, dy).filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * alpha // 255))
    return s


AERO_STOPS = [(0.0, (232, 246, 255)), (0.45, (150, 200, 250)), (0.5, (60, 130, 230)), (1.0, (24, 76, 170))]


def plate(W, H, px, py, pw, ph):
    """The dark glass plate: base, glass band and top hairline are separate
    layers composited together (ImageDraw replaces pixels, it does not blend,
    so drawing the band straight onto the base would punch a hole in it)."""
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(base).rounded_rectangle((px, py, px + pw, py + ph), radius=22, fill=(16, 18, 28, 200))
    band = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rounded_rectangle((px, py, px + pw, py + ph // 2), radius=22, fill=(255, 255, 255, 20))
    bd.rectangle((px, py + ph // 2 - 22, px + pw, py + ph // 2), fill=(255, 255, 255, 20))
    bd.line((px + 22, py + 1, px + pw - 22, py + 1), fill=(255, 255, 255, 70))
    p = Image.alpha_composite(base, band)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((px, py + 10, px + pw, py + ph + 10), radius=22, fill=(0, 0, 0, 120))
    return sh.filter(ImageFilter.GaussianBlur(18)), p


def on_plate(cover, word, box, tagline_colour=(214, 220, 232)):
    """Place a rendered word (with its ink box) and the tagline on the glass
    plate bottom-left: 16px above the ink, 10px between word and tagline."""
    W, H = cover.size
    sub_font = ImageFont.truetype(FONT_R, 34)
    sw = sub_font.getlength(TAGLINE)
    x0, y0, x1, y1 = box
    ink_w, ink_h = x1 - x0, y1 - y0
    pw = int(max(ink_w, sw) + 120)
    ph = 16 + ink_h + 10 + 34 + 20
    px, py = 72, H - ph - 72
    sh, p = plate(W, H, px, py, pw, ph)
    cover = Image.alpha_composite(cover, sh)
    cover = Image.alpha_composite(cover, p)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(word, (px + 60 - x0, py + 16 - y0))      # no mask: copy the alpha as is
    cover = Image.alpha_composite(cover, layer)
    tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tl).text((px + 62, py + 16 + ink_h + 6), TAGLINE, font=sub_font, fill=tagline_colour + (255,))
    return Image.alpha_composite(cover, tl)


def variant_aero(cover, accents):
    font = ImageFont.truetype(FONT_B, 118)
    mask, box = text_mask(TITLE, font)
    fill = vgradient(mask.size, AERO_STOPS)
    word = Image.alpha_composite(shadow_for(mask), glossy(mask, box, fill))
    return on_plate(cover, word, box)


def variant_spectrum(cover, accents):
    font = ImageFont.truetype(FONT_B, 118)
    mask, box = text_mask(TITLE, font)
    # the accents left to right, each lifted a little so the word stays bright
    cols = [tuple(round(v + (255 - v) * 0.18) for v in a) for a in accents]
    fill = hgradient(mask.size, cols)
    # darken the lower half for the gloss falloff
    shade = vgradient(mask.size, [(0.0, (255, 255, 255)), (0.5, (255, 255, 255)), (1.0, (120, 120, 120))])
    fill = ImageChops.multiply(fill, shade)
    word = Image.alpha_composite(shadow_for(mask), glossy(mask, box, fill, glow=(255, 255, 255)))
    return on_plate(cover, word, box)


def variant_mirror(cover, accents):
    W, H = cover.size
    font = ImageFont.truetype(FONT_B, 150)
    sub_font = ImageFont.truetype(FONT_R, 34)
    # the two halves as separate masks on one canvas
    full_mask, box = text_mask(TITLE, font, pad=60)
    fic_w = font.getlength('Fic')
    x0, y0, x1, y1 = box
    fic_mask = Image.new('L', full_mask.size, 0)
    ImageDraw.Draw(fic_mask).rectangle((0, 0, x0 + fic_w, full_mask.height), fill=255)
    fic_mask = ImageChops.multiply(full_mask, fic_mask)
    aero_mask = ImageChops.subtract(full_mask, fic_mask)
    white = Image.new('RGB', full_mask.size, (248, 250, 255))
    white = ImageChops.multiply(white, vgradient(full_mask.size, [(0.0, (255, 255, 255)), (0.5, (255, 255, 255)), (1.0, (200, 206, 220))]))
    fic = glossy(fic_mask, box, white, glow=(255, 255, 255))
    aero = glossy(aero_mask, box, vgradient(full_mask.size, AERO_STOPS))
    word = Image.alpha_composite(Image.alpha_composite(shadow_for(full_mask, dy=10, blur=14), fic), aero)
    # reflection: the word flipped, fading out over the top 55% of its ink
    refl = word.transpose(Image.FLIP_TOP_BOTTOM)
    rw, rh_img = refl.size
    rh = y1 - y0
    fade = Image.new('L', refl.size, 0)
    fp = fade.load()
    for y in range(rh_img):
        t = (y - (rh_img - y1)) / max(1, rh)     # 0 at the reflection's ink top
        v = int(max(0, 90 * (1 - t / 0.55))) if 0 <= t <= 0.55 else 0
        for x in range(rw):
            fp[x, y] = v
    refl.putalpha(ImageChops.multiply(refl.getchannel('A'), fade))
    # halo behind the word so it reads on the page
    wx, wy = 60, H - 72 - 34 - 24 - int(rh * 0.5) - y1
    hm = Image.new('L', (W, H), 0)
    hm.paste(full_mask, (wx, wy))
    halo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    halo.putalpha(hm.filter(ImageFilter.GaussianBlur(44)).point(lambda v: min(255, v * 3) * 165 // 255))
    cover = Image.alpha_composite(cover, halo)
    # true compositing: paste-with-mask blends alpha and washes the faint
    # reflection out, so each piece goes on its own full-size layer
    def full(im, pos):
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        L.paste(im, pos)
        return L
    # the reflection's ink top sits 6px under the word's ink bottom
    cover = Image.alpha_composite(cover, full(refl, (wx, wy + y1 + 6 - (rh_img - y1))))
    cover = Image.alpha_composite(cover, full(word, (wx, wy)))
    tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tl).text((wx + x0 + 6, wy + y1 + int(rh * 0.5) + 12), TAGLINE, font=sub_font, fill=(255, 255, 255, 235))
    return Image.alpha_composite(cover, tl)


VARIANTS = {'aero': variant_aero, 'spectrum': variant_spectrum, 'mirror': variant_mirror}


if __name__ == '__main__':
    import sys, json
    src, out, accents_json = sys.argv[1], sys.argv[2], sys.argv[3]
    accents = [tuple(a) for a in json.loads(accents_json)]
    base = Image.open(src).convert('RGBA')
    W, H = base.size
    crop = (0, H - 420, 1000, H)
    sheet = Image.new('RGB', (1000, 420 * 3 + 40), (40, 40, 40))
    label_font = ImageFont.truetype(FONT_B, 22)
    for i, (name, fn) in enumerate(VARIANTS.items()):
        im = fn(base.copy(), accents).crop(crop)
        sheet.paste(im, (0, i * (420 + 20)))
        ImageDraw.Draw(sheet).text((12, i * 440 + 10), name, font=label_font, fill=(255, 255, 255))
    sheet.save(out)
    print('wrote', out)
