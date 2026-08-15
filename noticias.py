#!/usr/bin/env python3
"""
Agregador de notícias da Garagem.

Lê feeds RSS/Atom de publicações automóveis reputáveis, junta, limpa, ordena
por data e grava um ficheiro JSON que a web app lê para montar a secção
"Notícias".

Rigor e boas práticas:
  - Guarda apenas **título, resumo curto, fonte, data e link** para o original.
    Nunca o texto integral do artigo — a leitura acontece no site da fonte.
  - Limite por fonte, para nenhuma publicação dominar o agregado.

Uso:
  python noticias.py --out assets/news/noticias.json --max 60
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys
from urllib.parse import urlparse

import feedparser

# (nome, url, categoria, é_português)
FEEDS = [
    # ---- Desporto motorizado ----
    ("Motorsport.com",  "https://www.motorsport.com/rss/all/news/",        "Desporto",  False),
    ("Autosport",       "https://www.autosport.com/rss/all/news/",         "Desporto",  False),
    ("Formula 1",       "https://www.formula1.com/en/latest/all.xml",      "Desporto",  False),
    ("FIA",             "https://www.fia.com/rss/news",                    "Desporto",  False),
    ("AutoSport",       "https://www.autosport.pt/feed/",                  "Desporto",  True),
    # ---- Indústria e novos modelos ----
    ("Autocar",         "https://www.autocar.co.uk/rss",                   "Modelos",   False),
    ("Motor1",          "https://www.motor1.com/rss/news/all/",            "Modelos",   False),
    ("Carscoops",       "https://www.carscoops.com/feed/",                 "Modelos",   False),
    ("Car and Driver",  "https://www.caranddriver.com/rss/all.xml/",       "Modelos",   False),
    ("Road & Track",    "https://www.roadandtrack.com/rss/all.xml/",       "Modelos",   False),
    ("Razão Automóvel", "https://www.razaoautomovel.com/feed",             "Modelos",   True),
    # ---- Coleção e clássicos ----
    ("Hagerty",         "https://www.hagerty.com/media/feed/",             "Clássicos", False),
]

UA = "Mozilla/5.0 (compatible; GaragemBot/1.0; agregador pessoal de notícias)"
MAX_POR_FONTE = 8
RESUMO_MAX = 190


def limpar(texto: str) -> str:
    """Remove HTML, entidades e espaços a mais."""
    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html.unescape(texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def encurtar(texto: str, limite: int = RESUMO_MAX) -> str:
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0]
    return corte.rstrip(".,;:—- ") + "…"


def data_iso(entry) -> str | None:
    for campo in ("published_parsed", "updated_parsed"):
        t = getattr(entry, campo, None)
        if t:
            try:
                return dt.datetime(*t[:6], tzinfo=dt.timezone.utc).isoformat().replace("+00:00", "Z")
            except Exception:  # noqa: BLE001
                continue
    return None


def chave(titulo: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", titulo.lower())[:70]


def main() -> None:
    ap = argparse.ArgumentParser(description="Agregar notícias automóveis para a Garagem.")
    ap.add_argument("--out", default="assets/news/noticias.json", help="Ficheiro JSON de saída.")
    ap.add_argument("--max", type=int, default=60, help="Número máximo de notícias guardadas.")
    args = ap.parse_args()

    itens, vistos, falhas = [], set(), []

    for nome, url, categoria, pt in FEEDS:
        try:
            feed = feedparser.parse(url, agent=UA)
            entradas = feed.entries or []
            if not entradas:
                falhas.append(nome)
                print(f"  ⚠ {nome}: sem entradas")
                continue
            contados = 0
            for e in entradas:
                titulo = limpar(getattr(e, "title", ""))
                link = getattr(e, "link", "") or ""
                if not titulo or not link:
                    continue
                k = chave(titulo)
                if k in vistos or link in vistos:
                    continue
                vistos.add(k)
                vistos.add(link)
                resumo = encurtar(limpar(getattr(e, "summary", "") or getattr(e, "description", "")))
                itens.append({
                    "titulo": titulo,
                    "resumo": resumo,
                    "url": link,
                    "fonte": nome,
                    "dominio": urlparse(link).netloc.replace("www.", ""),
                    "categoria": categoria,
                    "pt": pt,
                    "data": data_iso(e),
                })
                contados += 1
                if contados >= MAX_POR_FONTE:
                    break
            print(f"  ✓ {nome}: {contados} notícias")
        except Exception as exc:  # noqa: BLE001
            falhas.append(nome)
            print(f"  ✗ {nome}: {exc}")

    if not itens:
        sys.exit("ERRO: nenhuma notícia obtida — nada a gravar.")

    # mais recentes primeiro (sem data vai para o fim)
    itens.sort(key=lambda x: x["data"] or "", reverse=True)
    itens = itens[: args.max]

    dados = {
        "atualizado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "fontes": sorted({i["fonte"] for i in itens}),
        "itens": itens,
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)

    print(f"\n{len(itens)} notícias de {len(dados['fontes'])} fontes → {args.out}")
    if falhas:
        print("Fontes sem resposta desta vez:", ", ".join(falhas))


if __name__ == "__main__":
    main()
