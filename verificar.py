#!/usr/bin/env python3
"""Verificações rápidas ao index.html, antes de cada commit.

Existe por causa de um erro que já apareceu três vezes: ao inserir código
procurando um comentário (ex.: "/* ---------- Ficha ---------- */"), o mesmo
comentário existe no CSS **e** no JavaScript, e o bloco vai parar ao sítio
errado. O browser não se queixa — a página é que deixa de funcionar a meio.

Uso: python verificar.py     (sai com código 1 se algo estiver mal)
"""
import re
import sys
from pathlib import Path

s = Path(__file__).with_name('index.html').read_text(encoding='utf-8')
css = s[s.index('<style>') + 7: s.index('</style>')]
css_sem_comentarios = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
html = s[:s.index('<style>')] + s[s.index('</style>') + 8:]
falhas = []


def testar(nome, ok, detalhe=''):
    print(('  ✓ ' if ok else '  ✗ ') + nome + (f' — {detalhe}' if detalhe and not ok else ''))
    if not ok:
        falhas.append(nome)


# 1. JavaScript que escorregou para dentro do <style> (o erro histórico)
intrusos = re.findall(r'\b(?:function\s+\w+\s*\(|document\.getElementById|=>\s*\{|addEventListener)',
                      css_sem_comentarios)
testar('sem JavaScript dentro do <style>', not intrusos, str(intrusos[:3]))

# 2. chavetas equilibradas no CSS
a, f = css_sem_comentarios.count('{'), css_sem_comentarios.count('}')
testar('chavetas do CSS equilibradas', a == f, f'{a} abertas, {f} fechadas')

# 3. seletores declarados mais do que uma vez no mesmo âmbito
depth, ctx, buf, vistos = 0, [], '', {}
for ch in css_sem_comentarios:
    if ch == '{':
        sel = ' '.join(buf.split())
        if sel.startswith('@'):
            ctx.append(sel)
        else:
            vistos[(tuple(ctx), sel)] = vistos.get((tuple(ctx), sel), 0) + 1
        depth += 1
        buf = ''
    elif ch == '}':
        depth -= 1
        buf = ''
        if ctx and depth == len(ctx) - 1:
            ctx.pop()
    elif ch == ';':
        buf = ''
    else:
        buf += ch
dups = [k[1] for k, v in vistos.items() if v > 1]
testar('sem seletores CSS duplicados', not dups, ', '.join(dups[:4]))

# 4. ids usados pelo JavaScript que não existem no HTML
ids = set(re.findall(r'\bid="([\w-]+)"', s))
usados = set(re.findall(r"getElementById\('([\w-]+)'\)", s))
testar('todos os ids existem', not (usados - ids), ', '.join(sorted(usados - ids)))

# 5. imagens sem texto alternativo
sem_alt = [m for m in re.findall(r'<img[^>]*>', s) if 'alt=' not in m]
testar('todas as imagens têm alt', not sem_alt, str(len(sem_alt)))

# 6. botões só com ícone e sem nome acessível
anonimos = [m.group(0)[:60] for m in re.finditer(r'<button[^>]*>(.*?)</button>', s, re.S)
            if not re.sub(r'<[^>]+>', '', m.group(1)).strip() and 'aria-label' not in m.group(0)]
testar('botões de ícone com nome', not anonimos, str(anonimos[:2]))

# 7. classes definidas no CSS que ninguém usa
classes = set(re.findall(r'\.(-?[_a-zA-Z][\w-]*)', css_sem_comentarios))
texto = set(re.findall(r'[\w-]+', html))
mortas = sorted(c for c in classes if c not in texto) or []
testar('sem classes CSS mortas', len(mortas) <= 2, ', '.join(mortas[:6]))

print()
if falhas:
    print(f'{len(falhas)} verificação(ões) a falhar.')
    sys.exit(1)
print('Tudo em ordem.')
