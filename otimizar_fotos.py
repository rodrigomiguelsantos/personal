#!/usr/bin/env python3
"""Gera versões menores de cada fotografia, para o browser descarregar só o
que precisa.

O problema: as fotos estão guardadas a 1600 px de largura, mas um card na
grelha ocupa ~400 px e uma miniatura ~96 px. No iPhone, isso é descarregar
quatro vezes mais dados do que se vê. A solução normal na web é dar ao browser
**várias medidas da mesma foto** (`srcset`) e deixá-lo escolher conforme o ecrã.

Este script cria, ao lado de cada `foto.jpg`, um `foto-480.jpg` e um
`foto-960.jpg`. **O original nunca é tocado** — continua a ser a medida grande,
para a ficha em ecrã cheio e para o futuro.

Uso: python otimizar_fotos.py [--forcar]
"""
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).parent / 'assets/cars'
MEDIDAS = (480, 960)
QUALIDADE = 82
FORCAR = '--forcar' in sys.argv


def derivadas(foto: Path):
    for m in MEDIDAS:
        yield m, foto.with_name(f'{foto.stem}-{m}.jpg')


def main() -> None:
    originais = sorted(
        f for f in RAIZ.glob('*/*.jpg')
        if not any(f.stem.endswith(f'-{m}') for m in MEDIDAS)
    )
    feitas = poupado = 0
    for foto in originais:
        im = None
        for largura, destino in derivadas(foto):
            if destino.exists() and not FORCAR:
                continue
            im = im or Image.open(foto).convert('RGB')
            if im.width <= largura:
                continue  # já é menor do que o alvo — não vale a pena
            novo = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
            novo.save(destino, 'JPEG', quality=QUALIDADE, optimize=True, progressive=True)
            feitas += 1
            poupado += foto.stat().st_size - destino.stat().st_size
            print(f'  ✓ {destino.relative_to(RAIZ)}  '
                  f'({destino.stat().st_size // 1024} kB vs {foto.stat().st_size // 1024} kB)')
    print(f'\n{feitas} versões geradas a partir de {len(originais)} originais.')
    if feitas:
        print(f'Cada card poupa em média {poupado / feitas / 1024:.0f} kB.')


if __name__ == '__main__':
    main()
