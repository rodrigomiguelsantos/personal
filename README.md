# Garagem do Dr. Rodrigo

Aplicação web privada para gerir e apresentar a coleção de automóveis do Dr. Rodrigo.
Curadoria de **Gervásio**.

> **Estado atual:** protótipo visual (WIP) — montra estática da coleção com pesquisa e filtros.
> A app completa (gestão de carros com base de dados, visualizador 3D e garagem navegável)
> será construída sobre esta base. Ver *roadmap* abaixo.

## Ver a montra

- **Localmente:** abrir o ficheiro `index.html` num browser.
- **Online (grátis):** ativar o GitHub Pages (ver instruções abaixo).

### Ativar GitHub Pages
1. No repositório: **Settings → Pages**
2. Em *Source*, escolher a branch `claude/garage-3d-web-app-kdbt4i` e a pasta `/ (root)`
3. Guardar. Ao fim de ~1 min fica disponível num endereço `https://<utilizador>.github.io/personal/`

## Princípios

- **Independente** — dados e conteúdos vivem na própria app, sem bases de dados de carros externas.
- **Portável** — pensada para correr em qualquer sítio (local, VPS, ou home server).
- **Acessível em todo o lado** — web, iPad e iPhone.

## Arquitetura prevista (app completa)

| Camada | Tecnologia |
|---|---|
| Frontend + Backend | Next.js + TypeScript |
| UI | Tailwind CSS + shadcn/ui |
| Base de dados | SQLite (ficheiro único, via Prisma) |
| 3D | Three.js + React Three Fiber |
| Empacotamento | Docker |

## Roadmap

- [x] **Fase 0 —** Conceito, estrutura de dados e linguagem de design
- [x] **Fase 1a —** Montra visual WIP (esta página) com pesquisa e filtros
- [ ] **Fase 1b —** App real: CRUD de carros, base de dados, upload de fotos
- [ ] **Fase 2 —** Página de veículo completa (todos os cards) + coleções/grupos
- [ ] **Fase 3 —** Visualizador 3D (GLB) por veículo
- [ ] **Fase 4 —** PWA, documentos, backup/exportação
- [ ] **Fase 5 —** Interações 3D (portas, vista explodida)
- [ ] **Fase 6 —** "Garage World": ambiente 3D navegável em primeira pessoa

## Coleção (10 automóveis)

Porsche Carrera GT · Ferrari F355 Berlinetta · Ferrari Enzo · Porsche 911 GT2 RS ·
Porsche 959 · Aston Martin V12 Vantage Roadster · Mercedes-Benz SLR McLaren ·
Porsche 917 (versão de estrada) · Lancia Delta (homologação) · DS Automobiles N°8
