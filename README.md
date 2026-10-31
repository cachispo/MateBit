# MateBit ♞

Puzles de ajedrez infinitos con estética de 8 bits, en **blanco y negro puro** (1 bit).
Tablero oscuro pensado para jugar de noche, piezas ♔♕♖♗♘♙♚♛♜♝♞♟ y pitidos de máquina recreativa.

* Puzles nuevos sin fin, pedidos a la [API de Lichess](https://lichess.org/api) (`/api/puzzle/next`).
* Tres vidas, racha, puntos, pista y récord (guardado en el dispositivo).
* Reserva de 25 puzles guardados para jugar sin conexión.
* Sin dependencias en ejecución: todo (código, motor de ajedrez y tipografías) va dentro de un único HTML.

## Estructura

```
src/        el juego: index.html (plantilla), style.css, app.js
vendor/     chess.js y tipografías (con sus licencias)
tools/      build.py (genera todo) y make\_icons.py (iconos)
dist/       matebit.html: un solo fichero que abre cualquier navegador
docs/       la PWA para GitHub Pages (instalable en Android e iOS)
android/    app Android (WebView) + build.sh que compila y firma el APK
ios/        fuentes Swift para Xcode (ver ios/LEEME.md)
```

Tras editar algo en `src/`, ejecuta `python3 tools/build.py` para regenerar `dist/`, `docs/` y las apps.
Los resultados generados también están en el repositorio para que funcione nada más clonarlo.

## Notas sobre los puzles

La API de Lichess es pública y de uso libre dentro de sus [condiciones](https://lichess.org/terms-of-service),
que se reservan límites y la revocación del acceso. Si el juego llegara a tener mucho uso, lo prudente es empaquetar
un subconjunto de la [base de datos de puzles](https://database.lichess.org/#puzzles) (licencia CC0) en la propia app.

