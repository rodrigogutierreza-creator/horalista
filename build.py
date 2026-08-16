#!/usr/bin/env python3
"""Compila landing.src.html en las dos salidas del proyecto.

  dist/index.html         documento completo y autocontenido; es lo unico que
                          Vercel publica (vercel.json apunta a dist/)
  horalista-artifact.html el mismo contenido sin <html>/<head>/<body>, para publicar
                          como artifact (el publicador pone su propio esqueleto)

Las tipografias de fonts/ se incrustan como data URI: el CSP de los artifacts
bloquea los CDN de fuentes, asi que empotrarlas es la unica forma de que la
pagina no caiga a Arial. Uso:  python3 build.py
"""

import base64
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent
FUENTE = BASE / "landing.src.html"
DIST = BASE / "dist"
INDEX = DIST / "index.html"
ARTIFACT = BASE / "horalista-artifact.html"

# El <title> largo lleva palabras clave para buscadores; la galeria de artifacts
# muestra solo el nombre del producto.
TITULO_SEO = "HoraLista — agenda automática por WhatsApp para PyMEs"
TITULO_CORTO = "HoraLista"

TIPOGRAFIAS = {
    "__FONT_ARCHIVO__": BASE / "fonts" / "archivo.woff2",
    "__FONT_NEWSREADER__": BASE / "fonts" / "newsreader.woff2",
}


def extraer(patron, html, que):
    m = re.search(patron, html, re.DOTALL | re.IGNORECASE)
    if not m:
        sys.exit("No se encontro %s en el HTML generado" % que)
    return m.group(1).strip()


def main():
    if not FUENTE.exists():
        sys.exit("Falta %s" % FUENTE.name)
    html = FUENTE.read_text(encoding="utf-8")

    for marca, ruta in TIPOGRAFIAS.items():
        if not ruta.exists():
            sys.exit("Falta la tipografia %s" % ruta)
        if marca not in html:
            sys.exit("La marca %s ya no aparece en landing.src.html" % marca)
        html = html.replace(marca, base64.b64encode(ruta.read_bytes()).decode("ascii"))

    if "__TITLE__" not in html:
        sys.exit("Falta la marca __TITLE__ en landing.src.html")

    DIST.mkdir(exist_ok=True)
    INDEX.write_text(html.replace("__TITLE__", TITULO_SEO), encoding="utf-8")

    estilos = extraer(r"(<style>.*?</style>)", html, "el <style>")
    cuerpo = extraer(r"<body[^>]*>(.*?)</body>", html, "el <body>")
    ARTIFACT.write_text(
        "<title>%s</title>\n\n%s\n\n%s\n" % (TITULO_CORTO, estilos, cuerpo),
        encoding="utf-8",
    )

    for f in (INDEX, ARTIFACT):
        print("OK -> %-26s %6.1f KB" % (f.relative_to(BASE), f.stat().st_size / 1024))


if __name__ == "__main__":
    main()
