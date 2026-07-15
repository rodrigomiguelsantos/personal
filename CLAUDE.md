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
- **"Showroom noturno":** fundo quase-preto cinematográfico, escolha deliberada
  de tema único (escuro). Inspiração: Porsche, Ferrari (ex.: Luce), Aston Martin.
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

## Features da montra (v0.2)
- Pesquisa + filtros por coleção (chips) · ficha completa por carro (overlay
  com galeria, história, curiosidades, nota do Gervásio) · vista grelha/lista
  (toggle, persistida) · menu: Coleção / Grupos / Arquivo.
- **Grupos personalizados (✦):** criar/editar/remover no gestor (chip
  "＋ Grupos" ou menu). Guardados em `localStorage` — **só no dispositivo**;
  migram para a BD no Modelo B. Sugestões de um toque: Alemães, Italianos,
  Britânicos, Franceses, V12, Século XX, Ar livre.

## Ritual por prompt
A cada prompt de desenvolvimento, fazer **uma pesquisa de design** (UI de
showrooms/marcas/leiloeiras, animações fluidas, micro-interações) e aplicar
o que for útil. Registar aprendizagens relevantes aqui.

## Fluxo para adicionar um carro novo (Modelo A)
1. Eu apresento um **formulário** com os campos a preencher.
2. O Dr. Rodrigo preenche os dados e envia fotografias do exemplar.
3. Eu complemento a investigação (specs, história, curiosidades) com rigor,
   e peço mais fotos se as que há não chegarem / não forem do carro dele.
4. Eu adiciono à "base de dados" (array `CARS` em `index.html`), coloco as fotos,
   crio a ficha e integro visualmente na UI.
5. Eu faço **commit e push**. Aparece online.

## Coleção (10) e arquivo de curadoria
Ver `README.md`. Correções já aplicadas: é **911 GT2 (2007)** — não GT2 RS;
**SLR McLaren** versão base (~2 157 unid., ainda assim exclusivo);
**Lancia Delta Integrale** (homologação Grupo A).
