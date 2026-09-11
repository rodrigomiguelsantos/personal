#!/usr/bin/env python3
"""Constrói a pré-visualização (Artifact) a partir do index.html.

Porque é preciso: a pré-visualização corre numa página isolada, sem acesso às
pastas do repositório. Logo, as fotografias e as notícias — que no site real
são ficheiros ao lado do index.html — têm de viajar *dentro* do HTML:
  - fotos  → convertidas em `data:` URI (o `photoSrc()` já as reconhece);
  - notícias → o JSON entra em linha, no lugar do `fetch`.
O site publicado no GitHub Pages continua a usar os ficheiros normais; isto é
só um espelho para eu mostrar o resultado ao Dr. Rodrigo.

Uso: python build_preview.py [saida.html]
"""
import base64
import json
import mimetypes
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).parent
ENTRADA = RAIZ / 'index.html'
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / 'preview.html'
NOTICIAS = RAIZ / 'assets/news/noticias.json'


def sub(s, a, b, n=1):
    c = s.count(a)
    assert c == n, f'esperado {n}, encontrado {c}: {a[:80]!r}'
    return s.replace(a, b, n)


LARGURA_MAX = 1400   # a pré-visualização não precisa de mais do que isto
QUALIDADE = 72


def data_uri(caminho: Path) -> str:
    """Fotos recomprimidas só para a pré-visualização — os ficheiros do
    repositório (e do site) mantêm a qualidade original, intocada."""
    try:
        from PIL import Image
        import io
        im = Image.open(caminho).convert('RGB')
        if im.width > LARGURA_MAX:
            im = im.resize((LARGURA_MAX, round(im.height * LARGURA_MAX / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=QUALIDADE, optimize=True, progressive=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        tipo = mimetypes.guess_type(caminho.name)[0] or 'image/jpeg'
        return f'data:{tipo};base64,' + base64.b64encode(caminho.read_bytes()).decode()


s = ENTRADA.read_text(encoding='utf-8')

# ---- 1. fotos em linha ----
i = s.index('const PHOTOS = {')
j = s.index('\n};', i) + 3
bloco = s[i:j]
mapa = {}
for slug, lista in re.findall(r'"([\w-]+)": \[([^\]]*)\]', bloco):
    fich = re.findall(r'"([^"]+)"', lista)
    uris = []
    for f in fich:
        p = RAIZ / 'assets/cars' / slug / f
        if not p.exists():
            print(f'  ⚠ sem ficheiro: {p}')
            continue
        uris.append(data_uri(p))
    mapa[slug] = uris
novo = 'const PHOTOS = {\n' + ',\n'.join(
    f'  "{k}": [' + ', '.join(f'"{u}"' for u in v) + ']' for k, v in mapa.items()) + '\n};'
s = s[:i] + novo + s[j:]
print(f'  ✓ {sum(len(v) for v in mapa.values())} fotos em linha')

# ---- 2. notícias em linha ----
if NOTICIAS.exists():
    dados = json.dumps(json.loads(NOTICIAS.read_text(encoding='utf-8')), ensure_ascii=False)
    s = sub(s, """    const res = await fetch('assets/news/noticias.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('sem ficheiro');
    newsData = await res.json();""", f'    newsData = {dados};')
    s = sub(s, """      const r = await fetch('assets/news/noticias.json', { cache: 'no-store' });
      if (!r.ok) throw new Error();
      newsData = await r.json();""", f'      newsData = {dados};')
    print(f'  ✓ {len(json.loads(NOTICIAS.read_text(encoding="utf-8"))["itens"])} notícias em linha')

SAIDA.write_text(s, encoding='utf-8')
print(f'\n{SAIDA} — {len(s) / 1e6:.2f} MB')
