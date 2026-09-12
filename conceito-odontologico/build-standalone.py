#!/usr/bin/env python3
"""
Gera conceito-odontologico.html — versão de arquivo único.

Embute o CSS, o JavaScript e o favicon dentro do próprio HTML, para que o site
possa ser aberto com dois cliques, sem servidor e sem a pasta de assets ao lado.

Uso:  python3 build-standalone.py
"""

import base64
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "index.html")
OUT = os.path.join(BASE, "conceito-odontologico.html")


def read(path):
    return io.open(path, encoding="utf-8").read()


def main():
    html = read(SRC)
    css = read(os.path.join(BASE, "css", "styles.css"))
    js = read(os.path.join(BASE, "js", "main.js"))
    favicon = io.open(os.path.join(BASE, "assets", "favicon.svg"), "rb").read()
    favicon_uri = "data:image/svg+xml;base64," + base64.b64encode(favicon).decode()

    # CSS -> <style> inline
    html = html.replace(
        '<link rel="stylesheet" href="css/styles.css">',
        "<style>\n" + css + "\n</style>",
    )

    # JS -> <script> inline
    html = html.replace(
        '<script src="js/main.js" defer></script>',
        "<script>\n" + js + "\n</script>",
    )

    # Favicon -> data URI (as meta tags Open Graph continuam apontando para as
    # URLs absolutas de produção, que é o correto para compartilhamento)
    html = re.sub(r'href="assets/favicon\.svg"', f'href="{favicon_uri}"', html)

    # Nota para quem abrir o arquivo
    html = html.replace(
        "<body>",
        "<body>\n<!-- Versão de arquivo único, gerada por build-standalone.py. "
        "Para editar, use os arquivos-fonte: index.html + css/styles.css + js/main.js -->",
        1,
    )

    io.open(OUT, "w", encoding="utf-8").write(html)
    print("gerado:", OUT, os.path.getsize(OUT) // 1024, "KB")


if __name__ == "__main__":
    main()
