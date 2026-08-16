# Garagem do Dr. Rodrigo — memória do projeto

## Contexto
Projeto pessoal do Dr. Rodrigo (independente do seu atelier), com fins de
investigação profissional. Web app privada para gerir e apresentar a sua
coleção de automóveis, acessível em qualquer lado (web, iPad, iPhone).

## Preferências (sempre respeitar)
- **Idioma:** Português de Portugal (PT-PT).
- **Tratamento:** "Dr. Rodrigo".
- **Curador:** "Gervásio" (voz da curadoria e das notas/opiniões).
- **Não é programador** — explicar termos técnicos em linguagem simples e, como
  é um projeto de investigação, explicar também o *porquê* das decisões.
- Só adicionar um veículo à coleção **após confirmação explícita** do proprietário.

## Estado e estratégia
- **Fase atual: Modelo A** — site estático (`index.html`) alojado no GitHub,
  visível via GitHub Pages. Dados vivem no próprio ficheiro. Desenvolvimento
  feito por mim (Claude): editar → commit → push → aparece online.
- **Passar ao Modelo B** (app Node.js + base de dados SQLite alojada na própria
  app, a correr num servidor cloud) **só quando o Dr. Rodrigo der luz verde** —
  quando a UI, features e dados estiverem bem. Sem bases de dados externas.
- Branch de trabalho: `claude/garage-3d-web-app-kdbt4i`.

## Arquitetura futura (Modelo B)
Next.js + TypeScript · Tailwind + shadcn/ui · SQLite (ficheiro, via Prisma) ·
Three.js/React Three Fiber (3D) · Docker. Alojamento grátis e sempre-ligado a
decidir na altura (candidato: VM "Always Free", ou home server; deploy por git).

## Linguagem de design
- **"Galeria diurna" (v0.4, 2026-07-16):** redesenho a pedido do Dr. Rodrigo —
  **fundo branco**, UI simples/requintada, animações fluidas e subtis (entrada
  do hero em cascata, fade entre separadores). Tiles cinza-claro tipo menu
  Porsche; nome do carro em tinta escura sobre estúdio claro tingido pela cor
  do carro; único momento escuro: tile do valor no dashboard (verde profundo).
  O tema escuro anterior fica na história do git se quisermos volta atrás.
- **Molde "showroom studio" (v0.5, 2026-07-16):** fotos religadas dentro de um
  molde editorial — título em **serifada display** (var(--font-serif)) +
  subtítulo em itálico, gradiente de luz e tipografia de revista, no espírito
  das referências do Dr. Rodrigo (McLaren F1, 300 SL, Miura, XKSS, Carrera GT).
  **Não gero imagens** (sem ferramenta + regra de rigor): uso fotos reais no
  molde. Fundo puro de estúdio exigiria recorte/geração — não fazemos.
  Fotos de estúdio limpas por modelo podem ser trocadas quando surgirem.
- Inspiração de origem: Porsche (menu claro), Ferrari (Luce), Aston Martin.
- Cada carro apresentado como peça de museu: **halo de luz de estúdio tingido
  com a cor real do carro**; nome grande como herói; pills minimalistas;
  dados em tipo monospace (sensação de instrumento); botão circular com seta;
  cantos arredondados; muito espaço branco.
- **Verde British Racing Green** como cor de assinatura (liga ao Carrera GT).
- Fotografia é o elemento estrutural principal — quando há foto real, ocupa o card.
- Princípios recolhidos de referências: curadoria "story-first" (Bring a Trailer);
  relatório de condição 1–5 e documentos em PDF (RM Sotheby's); histórico e
  lembretes de manutenção (Custodian); visualização 360° e partilha (configurador
  Porsche). A incorporar na ficha completa / app.
- Responsive e fluida em web, iPad e iPhone. Respeitar `prefers-reduced-motion`.

## Estrutura de dados
Separar **"O Modelo"** (factos comuns a todos os exemplares — specs, história,
produção) de **"Este Exemplar"** (dados do carro do Dr. Rodrigo — cor, estado,
chassis, aquisição, valor, fotos, documentos). É a separação central da futura
base de dados (entidade Modelo vs. entidade Veículo).

Campos por veículo (atual + previstos): marca, modelo, ano, cor (ext/int),
estado, potência, velocidade máx., 0–100, motor, produção/raridade, coleções
(grupos), tags, história, curiosidades, mercado/valor, notas do curador,
galeria de fotos, documentos (PDF), cronologia, condição (1–5), modelo 3D.

## Fotografias — regras de rigor
- Fotos enviadas pelo Dr. Rodrigo = fotos do exemplar dele; eu coloco-as na
  pasta do carro, otimizo e registo. Têm sempre prioridade sobre tudo o resto.
- Quando ele **não** envia fotos, posso **pesquisar fotos de referência do
  modelo exato** (modelo/ano/cor/spec certos — pesquisa rigorosa), mas:
  **notificá-lo sempre** do que foi usado, e marcar como *referência do modelo*,
  nunca apresentar como o exemplar dele. Em dúvida, pedir fotos.
- **Nunca inventar/gerar imagens.**
- Pastas: `assets/cars/<slug>/` (uma subpasta por carro, fotos numeradas
  `01.jpg, 02.jpg…`); registar no mapa `PHOTOS` em `index.html`.
  A 1.ª foto é a principal (hero do card e da ficha). Ver `assets/cars/README.md`.
- Estado: **carrera-gt tem 5 fotos do exemplar** (2026-07-15). Pendente: confirmar
  jantes (4 fotos com jantes prateadas/pinças amarelas; 1 com jantes bronze).
- **Fotos de referência (2026-07-15):** os outros 9 carros têm `ref-01.jpg`
  da Wikimedia Commons (licenças CC BY-SA — atribuição obrigatória em
  `assets/cars/CREDITS.md`). Marcadas na UI com selo "◈ referência do modelo"
  e nota na ficha. **Fracas/a substituir:** Aston (é coupé preto, não Roadster
  verde) e 917 (é o 917K Gulf de corrida). Tratamento aplicado via PIL
  (autocontraste, nitidez, saturação -6%) antes de entrar na app.
- `DADOS-EM-FALTA.md` na raiz: levantamento por carro do que falta (chassis,
  km, aquisição, cores por confirmar, variantes) + revisão de categorias.

## Features da montra (v0.3)
- Pesquisa + filtros por coleção (chips) · ficha completa por carro (overlay
  com galeria, história, curiosidades, nota do Gervásio) · vista grelha/lista
  (toggle, persistida) · **ordenação** (curadoria/ano/potência/vmáx/valor/nome,
  persistida) · menu-separadores: **Coleção / Cronologia / Dashboard / Grupos /
  ▶ Apresentação**.
- **Grupos personalizados (✦):** criar/editar/remover no gestor (chip
  "＋ Grupos" ou menu). Guardados em `localStorage` — **só no dispositivo**;
  migram para a BD no Modelo B. Sugestões de um toque: Alemães, Italianos,
  Britânicos, Franceses, V12, Século XX, Ar livre.
- **Cronologia:** linha temporal vertical por ano do automóvel (marcos por
  década); passará a usar datas de aquisição quando existirem.
- **Dashboard:** valor estimado total (campo `valueK` em milhares €, estimativas
  do Gervásio a validar), potência total/média, recordes, barras por
  nacionalidade/motorização/década (campo `engType`).
- **▶ Apresentação:** slideshow ecrã-cheio (foto cover, Ken Burns, auto-advance
  6,5 s, setas/toque, dots), usa os carros filtrados na Coleção.
- **PWA:** manifest.webmanifest + apple-touch-icon (monograma "G" gerado por
  PIL em assets/icons/) + metas iOS. Instalável via Safari → "Adicionar ao
  ecrã principal".
- Categorias afinadas (2026-07-16): Track→Competição, Raros→Ícones.
- **v1.0 (2026-08-06) — varrimento de qualidade da UI:**
  **escala tipográfica** consolidada de 19 tamanhos avulsos para **7 degraus**
  (10 · 11,5 · 12,5 · 13,5 · 15 · 17 · 21 px; +16 px nos campos em mobile).
  **Foco acessível** (`:focus-visible`) que só aparece com teclado.
  **Resposta ao toque** (`:active`) em cards/chips/botões/linhas + remoção do
  flash cinzento do iOS (`-webkit-tap-highlight-color`), alvos ≥44 px no
  telemóvel. **Hero em serifada** — unifica com cards/ficha (identidade
  editorial). Corrigido zoom automático do Safari em campos <16 px.
  Estado vazio, seleção de texto e ligaduras afinados.
- **v0.9 (2026-07-19):** UI varrida e movimento uniformizado; **Three.js
  auto-alojado** (`assets/vendor/three.module.js`) — luz ambiente subtil (blobs
  verdes a derivar, parallax ao ponteiro), com fallback para o gradiente CSS
  (não carrega na pré-visualização Artifact por CSP; carrega no Pages). Reveal
  uniforme estendido aos tiles/cards do Dashboard. Corrigidos estilos em falta
  da ficha (v0.8) e formatação no iPhone.
- **Koenigsegg Gemera (V8/HV8) adicionado (2026-07-19):** 11.º carro, a pedido.
  2 300 cv, 400 km/h, 0–100 1,9 s, V8 5.0 biturbo híbrido, 300 unid., ~€2,2M.
  Foto de referência (Commons, CC BY-SA, creditada). **Cor branca** (nome
  a confirmar), 2025 confirmado pelo Dr. Rodrigo.
- **v0.7 (2026-07-19):** decisão do Dr. Rodrigo — trazer capacidades à app
  vanilla no Pages, SEM React (React fica para Modelo B com servidor). Pages
  não corre servidor/BD: edição sincronizada exige Modelo B; no Pages só
  local (localStorage) + exportação p/ eu commitar. Feito agora: reveal ao
  rolar (IntersectionObserver) + parallax subtil do hero; separador Estúdio
  escondido (pipeline Gemini dormante — grátis não gera imagens). A seguir:
  edição local (CRUD) e visualizador 3D (Three.js, pendente de modelos GLB).

## Pipeline de imagens "showroom studio" (v0.6, 2026-07-19)
Geração **não local**: workflow GitHub Actions `.github/workflows/gerar.yml`
(`workflow_dispatch`, inputs modelo/subtitulo/foto) corre `gerar_carro.py`:
obtém foto real (input --foto ou pesquisa ddgs) → gera estúdio via **Google
Gemini `gemini-2.5-flash-image`** (segredo `GEMINI_API_KEY`) → aplica
título/subtítulo com Pillow (Playfair Display) → grava em `assets/generated/`
com nome `<slug>-<hash>.png` → regista em `assets/generated/manifest.json` →
commit+push (permissions: contents: write) → dispara o Pages.
Web app: separador **Estúdio** faz fetch do manifest e mostra grelha.
`robots.txt` (Disallow: /) + nomes com hash mitigam o repo ser público.
Nota de rigor: imagens IA marcadas como apresentação; fotos reais do exemplar
mantêm prioridade. Pendente: segredo GEMINI_API_KEY; workflow_dispatch só
aparece se o ficheiro existir na branch default.

## Notícias (v1.1, 2026-08-15)
Separador **Notícias** agrega títulos de 12 feeds RSS de publicações de
referência: **Desporto** (Motorsport.com, Autosport, Formula 1, FIA,
AutoSport PT) · **Modelos/indústria** (Autocar, Motor1, Carscoops, Car and
Driver, Road & Track, Razão Automóvel) · **Clássicos** (Hagerty).
Pipeline: `noticias.py` (feedparser) → `assets/news/noticias.json` →
a app faz fetch do JSON (mesma origem, **sem CORS nem terceiros em runtime**).
Workflow `.github/workflows/noticias.yml`: cron de 6/6 h + manual; faz
checkout da branch do site, corre o script, commit+push → dispara o Pages.
**Nota:** o `schedule` só dispara a partir da branch predefinida (`main`) —
o ficheiro tem de lá estar para a atualização ser automática.
Rigor: guarda só título, resumo curto, fonte, data e link para o original;
nunca o texto integral. Máx. 8 notícias por fonte, 60 no total.
Filtros na UI: Todas · Modelos · Desporto · Clássicos · Portugal.
Validado a 2026-08-16: workflow na `main`, run manual bem-sucedido, o robô
commitou `Atualizar notícias` na branch do site → Pages atualizado.

## Ritual por prompt
A cada prompt de desenvolvimento, fazer **uma pesquisa de design** (UI de
showrooms/marcas/leiloeiras, animações fluidas, micro-interações) e aplicar
o que for útil. Registar aprendizagens relevantes aqui.

## Motor de investigação de carros (protocolo de rigor)
Objetivo: aceder a ~99% dos carros da história (tudo o que foi homologado,
vendido, corrido ou leiloado), incluindo raros. Não há BD instalada — pesquisar
e **cruzar** fontes na internet, em EN/DE/IT/FR além de PT, e verificar.

Fontes por camada:
1. **Fabricante** (autoridade p/ specs e produção): Porsche Newsroom/Heritage,
   Ferrari, Mercedes-Benz Group Media, Aston Martin Heritage, DS, etc.
2. **Enciclopédico/estruturado**: Wikipedia (cruzar EN/DE/IT/PT), Wikidata.
3. **BD técnicas**: Ultimatespecs, automobile-catalog, carfolio, conceptcarz,
   supercars.net, allcarindex.
4. **Leiloeiras/mercado (ouro p/ raros: proveniência, chassis, valor)**:
   RM Sotheby's, Gooding, Bonhams, Broad Arrow, Artcurial, Mecum,
   Bring a Trailer, Collecting Cars, Car & Classic.
5. **Registos de marca / clubes / papéis FIA** (nível chassis do exemplar).
6. **Motorsport**: Racing Sports Cars, arquivos FIA, Le Mans, WRC.
7. **Avaliação**: Hagerty Valuation, Classic.com (p/ valor e valorização).
8. **Imprensa histórica**: Road & Track, Autocar, EVO, Quattroruote, Automobile Revue.
9. **Comunidades**: Rennlist, FerrariChat, PistonHeads (detalhes de variantes raras).

Método: cruzar 2–3 fontes por dado-chave (specs → fabricante/época; chassis/
proveniência/valor → leiloeira/registo); separar Modelo vs. Exemplar; assinalar
confirmado/estimado/conflito (⚑); notificar as fontes usadas; para one-offs, os
documentos primários do Dr. Rodrigo prevalecem sobre tudo.

## Fluxo para adicionar um carro novo (Modelo A)
1. Eu apresento um **formulário** com os campos a preencher.
2. O Dr. Rodrigo preenche os dados e envia fotografias do exemplar.
3. Eu complemento a investigação (specs, história, curiosidades) com rigor,
   e peço mais fotos se as que há não chegarem / não forem do carro dele.
4. Eu adiciono à "base de dados" (array `CARS` em `index.html`), coloco as fotos,
   crio a ficha e integro visualmente na UI.
5. Eu faço **commit e push**. Aparece online.

## Coleção (11) e arquivo de curadoria
Ver `README.md`. Correções já aplicadas: é **911 GT2 (2007)** — não GT2 RS;
**SLR McLaren** versão base (~2 157 unid., ainda assim exclusivo);
**Lancia Delta Integrale** (homologação Grupo A).
