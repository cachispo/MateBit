# vendor/

Dependencias incluidas tal cual para que el proyecto se construya sin red. Licencias en `../THIRD_PARTY.md`.

- `chess.js`: v0.10.3 (npm: `chess.js@0.10.3`).
- `press-start-2p-latin.woff2`: subconjunto latino (npm: `@fontsource/press-start-2p`).
- `piezas.woff2`: las 12 piezas de ajedrez de Noto Sans Symbols 2. Se obtuvo así:

```bash
pip install fonttools brotli
npm i @fontsource/noto-sans-symbols-2
pyftsubset node_modules/@fontsource/noto-sans-symbols-2/files/noto-sans-symbols-2-symbols-400-normal.woff \
  --unicodes=U+2654-265F --flavor=woff2 --output-file=piezas.woff2
```
