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

# Cores tiradas do logotipo: grafite (estrutura) + laranja (acento).
BRAND_900 = (27, 29, 32)
BRAND_700 = (51, 55, 59)
BRAND_100 = (231, 233, 234)
TEAL_SOFT = (169, 174, 178)   # cinza claro, usado no brilho superior
GOLD = (244, 123, 32)         # o laranja do logotipo
GOLD_SOFT = (251, 216, 182)
MIST = (169, 174, 178)
SUB = (199, 203, 206)

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
# Mesma marca do site (index.html), em coordenadas de um viewBox 40x40:
# um anel de grafite aberto à direita, atravessado por um swoosh laranja.
SWOOSH_PATH = (
    "M8 18.5 "
    "c2 7 9 11 16.8 9.3 "
    "c7.2 -1.6 12 -8.8 15.2 -20.8 "
    "c-3 8 -8.5 13.6 -15 14.9 "
    "c-6.7 1.3 -13.5 -.1 -17 -3.4 z"
)
RING_CENTRO = (20, 20)
RING_RAIO = 12.6
RING_ESPESSURA = 3.6
RING_ANGULOS = (36, 277)  # graus; a abertura fica à direita, como no logotipo


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


def draw_mark(img, x, y, scale, cor_anel, cor_swoosh):
    """Desenha a marca (anel + swoosh) com supersampling, para sair sem serrilhado."""
    ss = 3
    big = Image.new("RGBA", (img.width * ss, img.height * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)

    cx = (x + RING_CENTRO[0] * scale) * ss
    cy = (y + RING_CENTRO[1] * scale) * ss
    r = RING_RAIO * scale * ss
    d.arc([cx - r, cy - r, cx + r, cy + r], RING_ANGULOS[0], RING_ANGULOS[1],
          fill=cor_anel + (255,), width=max(1, round(RING_ESPESSURA * scale * ss)))

    pts = [((x + px * scale) * ss, (y + py * scale) * ss) for px, py in flatten(SWOOSH_PATH)]
    d.polygon(pts, fill=cor_swoosh + (255,))

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

    draw_mark(img, 78, 74, 2.1, (169, 174, 178), GOLD)

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
