#!/usr/bin/env python3
"""
Gera assets/og-image.png (1200x630) — a imagem de preview social do site.

Reproduz em bitmap a mesma identidade visual do og-image.svg:
gradiente verde petróleo, malha sutil, brilhos teal/dourado e a marca do dente.

Uso:  python3 assets/build-og-image.py
Requer: pillow  (pip install pillow)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")

BRAND_900 = (6, 48, 47)
BRAND_700 = (12, 82, 78)
BRAND_100 = (220, 237, 233)
TEAL_SOFT = (111, 179, 170)
GOLD = (199, 154, 60)
GOLD_SOFT = (239, 224, 194)
MIST = (143, 189, 182)
SUB = (185, 214, 209)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/dejavu/DejaVuSerif.ttf"
SANS = f"{FONT_DIR}/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diagonal_gradient(size, c0, c1):
    """Gradiente diagonal renderizado pequeno e ampliado (rápido e suave)."""
    w, h = 64, 64
    g = Image.new("RGB", (w, h))
    px = g.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = lerp(c0, c1, (x / (w - 1) + y / (h - 1)) / 2)
    return g.resize(size, Image.LANCZOS)


def radial_glow(size, color, opacity):
    """Brilho radial com alpha caindo suavemente até as bordas."""
    n = 128
    mask = Image.new("L", (n, n))
    px = mask.load()
    c = (n - 1) / 2
    for y in range(n):
        for x in range(n):
            d = min((((x - c) ** 2 + (y - c) ** 2) ** 0.5) / c, 1.0)
            px[x, y] = int(max(0.0, 1.0 - d) ** 2 * 255 * opacity)
    layer = Image.new("RGBA", (n, n), color + (255,))
    layer.putalpha(mask)
    return layer.resize(size, Image.LANCZOS)


# ---- Mini-renderizador do caminho SVG da marca (subconjunto M/c/l/z relativos) ----
BRAND_PATH = (
    "M20 6 c-3.4 -2.6 -8.2 -2.6 -11 .4 c-3 3.2 -3 8.4 -1.6 13 "
    "c1.1 3.6 2.8 7.1 4.3 10.2 c.9 1.9 3.6 1.7 4.3 -.3 l2.2 -6.4 "
    "c.3 -.9 1.6 -.9 1.9 0 l2.2 6.4 c.7 2 3.4 2.2 4.3 .3 "
    "c1.5 -3.1 3.2 -6.6 4.3 -10.2 c1.4 -4.6 1.4 -9.8 -1.6 -13 "
    "c-2.8 -3 -7.6 -3 -11 -.4 z"
)


def bezier(p0, p1, p2, p3, steps=18):
    pts = []
    for i in range(1, steps + 1):
        t = i / steps
        u = 1 - t
        pts.append((
            u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return pts


def flatten(path_d):
    tokens, i = [], 0
    while i < len(path_d):
        ch = path_d[i]
        if ch in "MmCcLlZz":
            tokens.append(ch)
            i += 1
        elif ch in " ,":
            i += 1
        else:
            j = i
            while j < len(path_d) and path_d[j] not in " ,MmCcLlZz":
                j += 1
            tokens.append(float(path_d[i:j]))
            i = j

    pts, cur, start, k = [], (0.0, 0.0), (0.0, 0.0), 0
    while k < len(tokens):
        cmd = tokens[k]
        k += 1
        if cmd == "M":
            cur = (tokens[k], tokens[k + 1]); k += 2
            start = cur
            pts.append(cur)
        elif cmd == "c":
            while k + 5 < len(tokens) and not isinstance(tokens[k], str):
                p1 = (cur[0] + tokens[k], cur[1] + tokens[k + 1])
                p2 = (cur[0] + tokens[k + 2], cur[1] + tokens[k + 3])
                p3 = (cur[0] + tokens[k + 4], cur[1] + tokens[k + 5])
                pts.extend(bezier(cur, p1, p2, p3))
                cur = p3
                k += 6
        elif cmd == "l":
            while k + 1 < len(tokens) and not isinstance(tokens[k], str):
                cur = (cur[0] + tokens[k], cur[1] + tokens[k + 1])
                pts.append(cur)
                k += 2
        elif cmd in ("z", "Z"):
            pts.append(start)
            cur = start
    return pts


def draw_mark(img, x, y, scale, color, width):
    pts = [(x + px * scale, y + py * scale) for px, py in flatten(BRAND_PATH)]
    # Supersampling: desenha 3x maior e reduz, para a linha sair suave.
    ss = 3
    big = Image.new("RGBA", (img.width * ss, img.height * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.line([(p[0] * ss, p[1] * ss) for p in pts], fill=color + (255,),
           width=width * ss, joint="curve")
    img.alpha_composite(big.resize(img.size, Image.LANCZOS))


def main():
    img = diagonal_gradient((W, H), BRAND_900, BRAND_700).convert("RGBA")

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 64):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 13))
    for y in range(0, H, 64):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 13))
    img.alpha_composite(grid)

    img.alpha_composite(radial_glow((680, 680), TEAL_SOFT, 0.55), (750, -250))
    img.alpha_composite(radial_glow((600, 600), GOLD, 0.40), (-180, 310))

    draw_mark(img, 78, 78, 2.1, BRAND_100, 5)

    d = ImageDraw.Draw(img)
    d.text((80, 250), "HORTOLÂNDIA · SP  —  DESDE 1994", font=font(SERIF, 26), fill=GOLD_SOFT)
    d.text((80, 300), "Conceito", font=font(SERIF_BOLD, 78), fill=(255, 255, 255))
    d.text((80, 388), "Odontológico", font=font(SERIF_BOLD, 78), fill=(255, 255, 255))
    d.text((80, 486), "Trinta anos cuidando do sorriso de Hortolândia.", font=font(SANS, 30), fill=SUB)

    d.line([(80, 546), (1120, 546)], fill=(255, 255, 255, 40), width=1)
    d.text((80, 566), "R. Antônio Fernandes Leite, 72 — Jd. Santa Izabel   ·   (19) 3845-6666",
           font=font(SANS, 24), fill=MIST)

    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print("gerado:", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
