#!/usr/bin/env python3
"""
Gerar imagem "showroom studio" de um carro para a Garagem do Dr. Rodrigo.

Fluxo:
  1. Obtém uma FOTO DE REFERÊNCIA real do modelo (via --foto ou pesquisa ddgs).
  2. Gera uma imagem estilo estúdio com a Google Gemini API (Nano Banana),
     usando a foto real como referência visual e o estilo por prompt.
  3. Aplica título + subtítulo em código (Pillow) — nunca pelo gerador.
  4. Grava o PNG (nome com hash) na pasta servida pelo Pages e regista no manifest.

Uso:
  python gerar_carro.py --modelo "Lamborghini Miura SV" \
      --subtitulo "O primeiro supercarro moderno" \
      --outdir assets/generated --manifest assets/generated/manifest.json
"""
import argparse
import datetime as _dt
import io
import json
import os
import re
import secrets
import sys
import textwrap
import unicodedata

import requests
from PIL import Image, ImageDraw, ImageFont

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

PROMPT_ESTILO = """Create a photorealistic automotive studio "showroom" photograph of the SAME car
shown in the reference image. It is essential to preserve the exact car: keep its
shape, proportions, badges, headlights, wheels and factory paint colour identical
to the reference. Do not invent a different car or restyle it.

Composition and style:
- Three-quarter FRONT view, camera at a low height (roughly headlight level),
  equivalent to a 35-50mm lens.
- Place the car in the LOWER HALF of the frame with generous empty negative space
  above it.
- A single large softbox visible at the TOP of the frame; soft, diffuse main light
  wrapping around the bodywork; gentle falloff; clean specular reflections on the
  panels; no hard shadows.
- Seamless cyclorama (infinity wall) background with a smooth vertical gradient,
  charcoal-grey in the corners fading to lighter grey toward the top. Neutral, no
  colour cast, no distractions.
- Polished concrete floor producing a soft, faithful mirror reflection of the car.
- Ultra-sharp, high dynamic range, exact factory colour, realistic reflections on
  paint and glass, correct badges and proportions, impeccable showroom condition
  (no dirt, no people, no text or logos overlaid).
- Leave the lower portion clean for a text overlay to be added later.
- Portrait orientation, 4:5 aspect ratio.
"""


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "carro"


def log(msg: str) -> None:
    print(f"[gerar_carro] {msg}", flush=True)


# --------------------------------------------------------------------------- #
# 1. FOTO DE REFERÊNCIA
# --------------------------------------------------------------------------- #
def _download_image(url: str, min_side: int = 600) -> Image.Image | None:
    try:
        r = requests.get(url, headers={"User-Agent": BROWSER_UA}, timeout=25)
        r.raise_for_status()
        im = Image.open(io.BytesIO(r.content)).convert("RGB")
        if min(im.size) < min_side:
            log(f"  descartada (pequena {im.size}): {url[:80]}")
            return None
        return im
    except Exception as e:  # noqa: BLE001
        log(f"  falhou download ({e}): {url[:80]}")
        return None


def obter_referencia(modelo: str, foto_url: str) -> Image.Image:
    if foto_url:
        log(f"A descarregar foto de referência indicada: {foto_url}")
        im = _download_image(foto_url, min_side=1)  # confiar no link do utilizador
        if im is None:
            sys.exit("ERRO: não foi possível descarregar a foto indicada em --foto.")
        return im

    log(f"Sem --foto: a pesquisar referência de '{modelo}' (ddgs / DuckDuckGo)…")
    query = f"{modelo} car 3/4 front studio high resolution"
    try:
        from ddgs import DDGS
    except Exception:  # noqa: BLE001
        from duckduckgo_search import DDGS  # type: ignore

    candidatas = []
    try:
        with DDGS() as d:
            for r in d.images(query, max_results=12):
                url = r.get("image") or r.get("url")
                w, h = r.get("width") or 0, r.get("height") or 0
                if url:
                    candidatas.append((url, min(w, h)))
    except Exception as e:  # noqa: BLE001
        log(f"pesquisa ddgs falhou: {e}")

    # tentar as maiores primeiro, no máximo 8
    candidatas.sort(key=lambda t: -t[1])
    for url, _ in candidatas[:8]:
        im = _download_image(url, min_side=600)
        if im is not None:
            log(f"Referência obtida: {url[:90]}")
            return im

    sys.exit(
        "ERRO: não foi possível obter uma foto de referência automaticamente. "
        "Volte a correr indicando --foto <URL de uma foto do modelo>."
    )


# --------------------------------------------------------------------------- #
# 2. GERAÇÃO VIA GEMINI
# --------------------------------------------------------------------------- #
def gerar_com_gemini(ref: Image.Image, api_key: str) -> Image.Image:
    from google import genai

    client = genai.Client(api_key=api_key)
    log("A gerar imagem com gemini-2.5-flash-image (Nano Banana)…")
    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[PROMPT_ESTILO, ref],
    )

    try:
        parts = resp.candidates[0].content.parts
    except Exception:  # noqa: BLE001
        sys.exit(f"ERRO: resposta inesperada do Gemini:\n{resp}")

    for part in parts:
        inline = getattr(part, "inline_data", None)
        if inline is not None and getattr(inline, "data", None):
            data = inline.data
            if isinstance(data, str):  # base64
                import base64
                data = base64.b64decode(data)
            return Image.open(io.BytesIO(data)).convert("RGB")

    # Nenhuma imagem — imprimir estrutura para diagnóstico (risco assinalado)
    log("Nenhuma parte com imagem encontrada. Estrutura das parts:")
    for i, part in enumerate(parts):
        log(f"  part[{i}]: text={getattr(part, 'text', None)!r} "
            f"inline_data={getattr(part, 'inline_data', None)!r}")
    sys.exit("ERRO: o Gemini não devolveu imagem.")


# --------------------------------------------------------------------------- #
# 3. OVERLAY DE TEXTO (Pillow)
# --------------------------------------------------------------------------- #
W, H = 1080, 1350  # retrato 4:5


def _fit_4x5(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((left, top, left + W, top + H))


def _load_font(paths: list[str], size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for p in paths:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                # fontes variáveis (Playfair[wght]): fixar peso
                try:
                    f.set_variation_by_axes([700 if bold else 400])
                except Exception:  # noqa: BLE001
                    pass
                return f
            except Exception:  # noqa: BLE001
                continue
    # fallback DejaVu (sempre presente com Pillow)
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    try:
        return ImageFont.truetype(name, size)
    except Exception:  # noqa: BLE001
        return ImageFont.load_default()


def _text_w(draw, text, font) -> int:
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def aplicar_texto(im: Image.Image, titulo: str, subtitulo: str) -> Image.Image:
    im = _fit_4x5(im)
    draw = ImageDraw.Draw(im)

    f_title = _load_font(
        ["fonts/PlayfairDisplay-Bold.ttf", "fonts/PlayfairDisplay[wght].ttf"], 78, bold=True
    )
    f_sub = _load_font(
        ["fonts/PlayfairDisplay-Italic.ttf", "fonts/PlayfairDisplay-Italic[wght].ttf"], 34
    )

    # gradiente subtil extra em baixo para legibilidade
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        t = max(0.0, (y - H * 0.62) / (H * 0.38))
        grad.putpixel((0, y), int(150 * t * t))
    veil = Image.new("RGB", (W, H), (8, 10, 9))
    im = Image.composite(veil, im, grad.resize((W, H)))
    draw = ImageDraw.Draw(im)

    def centered(text, font, y, fill, shadow=True):
        w = _text_w(draw, text, font)
        x = (W - w) // 2
        if shadow:
            draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=fill)

    # subtítulo: quebra em até 2 linhas a ~80% da largura
    sub_lines: list[str] = []
    if subtitulo:
        max_w = int(W * 0.8)
        words, line = subtitulo.split(), ""
        for wd in words:
            probe = (line + " " + wd).strip()
            if _text_w(draw, probe, f_sub) <= max_w or not line:
                line = probe
            else:
                sub_lines.append(line)
                line = wd
        if line:
            sub_lines.append(line)
        sub_lines = sub_lines[:2]

    title_bbox = draw.textbbox((0, 0), titulo, font=f_title)
    title_h = title_bbox[3] - title_bbox[1]
    sub_h = 46 * len(sub_lines)
    block_h = title_h + (18 + sub_h if sub_lines else 0)
    y = H - 90 - block_h

    centered(titulo, f_title, y, (255, 255, 255))
    y += title_h + 18
    for ln in sub_lines:
        centered(ln, f_sub, y, (222, 224, 220))
        y += 46
    return im


# --------------------------------------------------------------------------- #
# 4. MANIFEST
# --------------------------------------------------------------------------- #
def atualizar_manifest(caminho: str, entrada: dict) -> None:
    dados = []
    if os.path.exists(caminho):
        try:
            with open(caminho, encoding="utf-8") as fh:
                dados = json.load(fh)
                if not isinstance(dados, list):
                    dados = []
        except Exception:  # noqa: BLE001
            dados = []
    dados.append(entrada)
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2)
    log(f"Manifest atualizado ({len(dados)} entradas): {caminho}")


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Gerar imagem showroom-studio de um carro.")
    ap.add_argument("--modelo", required=True, help="Nome do modelo (título).")
    ap.add_argument("--subtitulo", default="", help="Subtítulo (uma linha).")
    ap.add_argument("--foto", default="", help="URL de foto de referência (opcional).")
    ap.add_argument("--outdir", default="assets/generated", help="Pasta de saída servida pelo Pages.")
    ap.add_argument("--manifest", default="assets/generated/manifest.json", help="Caminho do manifest JSON.")
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        sys.exit("ERRO: variável de ambiente GEMINI_API_KEY em falta.")

    subtitulo = args.subtitulo.strip()
    ref = obter_referencia(args.modelo, args.foto.strip())
    gerada = gerar_com_gemini(ref, api_key)
    final = aplicar_texto(gerada, args.modelo.strip(), subtitulo)

    os.makedirs(args.outdir, exist_ok=True)
    ficheiro = f"{slugify(args.modelo)}-{secrets.token_hex(3)}.png"
    destino = os.path.join(args.outdir, ficheiro)
    final.save(destino, "PNG")
    log(f"Imagem gravada: {destino}")

    atualizar_manifest(
        args.manifest,
        {
            "modelo": args.modelo.strip(),
            "subtitulo": subtitulo,
            "ficheiro": ficheiro,
            "data": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d"),
        },
    )
    log("Concluído.")


if __name__ == "__main__":
    main()
