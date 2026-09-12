#!/usr/bin/env python3
"""
Extrai a cor dominante de um logotipo e gera o bloco de tokens CSS do site.

O site inteiro é retintado a partir de seis variáveis no :root de css/styles.css.
Este script lê um arquivo de logotipo, encontra a cor de marca predominante e
monta a escala completa preservando exatamente a mesma progressão de luminosidade
do design original — ou seja, troca o matiz sem alterar os contrastes já validados.

Uso:
    python3 assets/extract-brand-colors.py assets/logo.png           # mostra o bloco
    python3 assets/extract-brand-colors.py assets/logo.png --write   # já aplica no CSS
    python3 assets/extract-brand-colors.py --hex "#1B4F8A"           # a partir de um hex

Requer: pillow  (pip install pillow)
"""

import argparse
import colorsys
import io
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(BASE, "..", "css", "styles.css")

# Progressão de luminosidade/saturação do design original (verde petróleo).
# Cada degrau é (luminosidade alvo, saturação alvo).
ESCALA = [
    ("--brand-900", 0.106, 0.78),
    ("--brand-800", 0.145, 0.75),
    ("--brand-700", 0.184, 0.74),
    ("--brand-500", 0.272, 0.71),
    ("--brand-300", 0.569, 0.26),
    ("--brand-100", 0.896, 0.28),
]
SAT_REFERENCIA = 0.72  # saturação média da marca original, usada para normalizar

COMENTARIOS = {
    "--brand-900": "fundos escuros: hero, seções deep, rodapé",
    "--brand-800": "",
    "--brand-700": "botões primários, links",
    "--brand-500": "ícones, detalhes",
    "--brand-300": "traços claros sobre fundo escuro",
    "--brand-100": "fundo dos ícones de card",
}


def hex_para_rgb(valor):
    v = valor.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise ValueError(f"hex inválido: {valor}")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def rgb_para_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def cor_dominante(caminho):
    """Cor mais saturada e frequente da imagem, ignorando fundo e neutros."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("pillow não instalado. Rode: pip install pillow")

    img = Image.open(caminho)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        fundo = Image.new("RGBA", img.size, (255, 255, 255, 0))
        img = Image.alpha_composite(fundo, img)
    else:
        img = img.convert("RGBA")

    img.thumbnail((400, 400))
    # get_flattened_data() no Pillow novo; getdata() nas versões anteriores
    pixels = img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata()

    candidatos = {}
    for r, g, b, a in pixels:
        if a < 128:
            continue  # transparente: é fundo, não marca
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if s < 0.18 or l < 0.06 or l > 0.94:
            continue  # cinza, branco, preto: não carregam o matiz da marca
        chave = (round(r / 16), round(g / 16), round(b / 16))
        atual = candidatos.get(chave)
        # pontua por frequência, dando peso extra à saturação
        candidatos[chave] = (atual[0] + 1 if atual else 1, (r, g, b), s)

    if not candidatos:
        sys.exit(
            "Nenhuma cor de marca encontrada na imagem — ela parece ser só "
            "preto/branco/cinza. Passe a cor manualmente com --hex \"#RRGGBB\"."
        )

    melhor = max(candidatos.values(), key=lambda c: c[0] * (0.5 + c[2]))
    return melhor[1]


def gerar_escala(base_rgb):
    r, g, b = (c / 255 for c in base_rgb)
    h, _, s_src = colorsys.rgb_to_hls(r, g, b)
    fator = min(max(s_src / SAT_REFERENCIA, 0.35), 1.45)

    saida = []
    for nome, l_alvo, s_alvo in ESCALA:
        s = min(max(s_alvo * fator, 0.04), 0.95)
        rr, gg, bb = colorsys.hls_to_rgb(h, l_alvo, s)
        saida.append((nome, tuple(round(c * 255) for c in (rr, gg, bb))))
    return saida


def montar_bloco(escala):
    linhas = []
    for nome, rgb in escala:
        comentario = COMENTARIOS.get(nome, "")
        sufixo = f"   /* {comentario} */" if comentario else ""
        linhas.append(f"  {nome}:   {rgb_para_hex(rgb)};{sufixo}")

    d900 = dict(escala)["--brand-900"]
    d300 = dict(escala)["--brand-300"]
    linhas.append("")
    linhas.append(f"  --brand-rgb:      {d900[0]}, {d900[1]}, {d900[2]};      /* = --brand-900, para sombras e bordas */")
    linhas.append(f"  --brand-soft-rgb: {d300[0]}, {d300[1]}, {d300[2]};  /* = --brand-300, para o brilho do hero */")
    return "\n".join(linhas)


def aplicar_no_css(escala):
    css = io.open(CSS, encoding="utf-8").read()
    original = css
    for nome, rgb in escala:
        css = re.sub(
            rf"({re.escape(nome)}:\s*)#[0-9A-Fa-f]{{3,6}};",
            lambda m, v=rgb_para_hex(rgb): m.group(1) + v + ";",
            css,
            count=1,
        )
    d900 = dict(escala)["--brand-900"]
    d300 = dict(escala)["--brand-300"]
    css = re.sub(r"(--brand-rgb:\s*)[\d,\s]+;", rf"\g<1>{d900[0]}, {d900[1]}, {d900[2]};", css, count=1)
    css = re.sub(r"(--brand-soft-rgb:\s*)[\d,\s]+;", rf"\g<1>{d300[0]}, {d300[1]}, {d300[2]};", css, count=1)

    if css == original:
        sys.exit("Nada foi alterado — o bloco de tokens no CSS não foi encontrado.")
    io.open(CSS, "w", encoding="utf-8").write(css)
    print(f"\nAplicado em {os.path.relpath(CSS, os.getcwd())}.")
    print("Se você usa a versão de arquivo único, rode agora: python3 build-standalone.py")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("imagem", nargs="?", help="arquivo do logotipo (PNG, JPG, WebP...)")
    ap.add_argument("--hex", help="usa esta cor em vez de extrair de uma imagem")
    ap.add_argument("--write", action="store_true", help="aplica direto em css/styles.css")
    args = ap.parse_args()

    if args.hex:
        base = hex_para_rgb(args.hex)
        origem = f"cor informada {args.hex.upper()}"
    elif args.imagem:
        base = cor_dominante(args.imagem)
        origem = f"cor dominante de {args.imagem}"
    else:
        ap.error("informe um arquivo de imagem ou --hex \"#RRGGBB\"")

    escala = gerar_escala(base)
    print(f"Base: {rgb_para_hex(base)}  ({origem})\n")
    print("Cole no :root de css/styles.css, no bloco CORES DA MARCA:\n")
    print(montar_bloco(escala))

    if args.write:
        aplicar_no_css(escala)


if __name__ == "__main__":
    main()
