# Fotografias dos veículos

Cada veículo tem a sua pasta, com o nome (`slug`) correspondente ao definido em `index.html`.

## Como adicionar fotos a um carro

1. Colocar os ficheiros de imagem dentro da pasta do carro, ex.: `assets/cars/carrera-gt/01.jpg`
2. Registar os nomes dos ficheiros no mapa `PHOTOS` em `index.html`:
   ```js
   const PHOTOS = {
     "carrera-gt": ["01.jpg", "02.jpg", "03.jpg"],
   };
   ```
3. A **1.ª foto da lista** é a principal (hero do card). As restantes servem para a galeria (na ficha completa).

## Regras de rigor (curadoria)

- As fotografias devem ser **mesmo do exemplar do Dr. Rodrigo**, não de outro carro do mesmo modelo.
- Preferir **alta resolução**. Para o efeito "de estúdio" das marcas, PNG com **fundo transparente** (recorte do carro) fica ideal; JPG de boa qualidade também serve.
- Enquanto uma pasta estiver vazia, o card usa um fundo de estúdio provisório com a cor real do carro.

## Slugs

| Veículo | Pasta |
|---|---|
| Porsche Carrera GT | `carrera-gt` |
| Ferrari F355 Berlinetta | `f355-berlinetta` |
| Ferrari Enzo | `enzo` |
| Porsche 911 GT2 | `911-gt2` |
| Porsche 959 | `959` |
| Aston Martin V12 Vantage Roadster | `v12-vantage-roadster` |
| Mercedes-Benz SLR McLaren | `slr-mclaren` |
| Porsche 917 (versão de estrada) | `917-stradale` |
| Lancia Delta Integrale | `delta-integrale` |
| DS Automobiles N°8 | `ds-n8` |
