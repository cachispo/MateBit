# Material de terceros

MateBit incluye (dentro de `vendor/`) las piezas ajenas siguientes, cada una con su licencia:

| Qué | Para qué | Licencia | Texto completo |
|---|---|---|---|
| [chess.js](https://github.com/jhlywa/chess.js) 0.10.3 | Reglas del ajedrez | BSD-2-Clause | `vendor/LICENSE-chess.js.txt` |
| [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) (subconjunto latino) | Letra de 8 bits | SIL Open Font License 1.1 | `vendor/LICENSE-press-start-2p.txt` |
| [Noto Sans Symbols 2](https://github.com/notofonts/symbols) (solo U+2654–265F, las piezas de ajedrez) | Dibujo de las piezas ♔♕♖♗♘♙♚♛♜♝♞♟ | SIL Open Font License 1.1 | `vendor/LICENSE-noto-sans-symbols-2.txt` |

El subconjunto de Noto se renombró internamente como `AjedrezPiezas` en el CSS; el fichero `vendor/piezas.woff2`
se obtuvo recortando la fuente original (ver `vendor/LEEME.md`).

## Puzles

Los puzles se piden en directo a la [API de Lichess](https://lichess.org/api) (`/api/puzzle/next`).
La [base de datos de puzles de Lichess](https://database.lichess.org/#puzzles) se publica con licencia CC0.
El uso de la API está sujeto a las [condiciones de Lichess](https://lichess.org/terms-of-service)
(límites de uso razonables, acceso revocable a su criterio).

MateBit no está afiliado a Lichess ni a ninguno de los proyectos anteriores.
