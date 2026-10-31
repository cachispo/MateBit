# MateBit ♞

Puzles de ajedrez infinitos con estética de 8 bits, en **blanco y negro puro** (1 bit).
Tablero oscuro pensado para jugar de noche, piezas ♔♕♖♗♘♙♚♛♜♝♞♟ y pitidos de máquina recreativa.

## ▶ Jugar (es lo único que necesitas)

### Android: descarga el APK

1. Entra en **[Releases → última versión](../../releases/latest)** y baja el fichero `matebit.apk`.
   (La carpeta *Releases* está también en la columna derecha de la página principal del repositorio.)
2. Ábrelo desde *Descargas*. Android te pedirá permitir **«instalar apps desconocidas»** al navegador o gestor de
   archivos que uses: acéptalo. Es normal, la app no está en Play Store.
3. Listo. Sin cuentas ni anuncios, y sin más permiso que internet (para pedir los puzles).

> **Eso es todo para jugar.** Lo que sigue es para quien quiera estudiar, modificar o rehacer el proyecto.

---

## Cómo funciona

- **El juego** es HTML, CSS y JavaScript (reglas con [chess.js](https://github.com/jhlywa/chess.js)). Es casi todo el código.
- **La app Android** es una «cáscara» de unas 80 líneas de **Java** que abre un `WebView` (un navegador sin barra de
  direcciones) y le entrega el juego, que va guardado dentro del APK. Sirve el HTML bajo un origen https interno,
  de modo que `localStorage` y las llamadas a Lichess funcionan como en una web normal.
- **La app iOS** es lo mismo en **Swift** (`WKWebView`).
- Los puzles se piden a la [API de Lichess](https://lichess.org/api) (`/api/puzzle/next`); se guardan 25 de reserva
  para jugar sin conexión. Récord y reserva se guardan en el dispositivo.

## Rehacer o modificar el proyecto

```
src/        el juego: index.html (plantilla), style.css, app.js
vendor/     chess.js y tipografías (con sus licencias)
tools/      build.py (genera todo) y make_icons.py (iconos)
dist/       matebit.html: un solo fichero que abre cualquier navegador
docs/       la web instalable para GitHub Pages
android/    app Android (WebView) + build.sh que compila y firma el APK
ios/        fuentes Swift para Xcode (ver ios/LEEME.md)
```

Tras editar algo en `src/`, ejecuta `python3 tools/build.py`: regenera `dist/`, `docs/` y el contenido de las apps.
Lo generado también está en el repositorio para que funcione nada más clonarlo. Para probar sin instalar nada,
abre `dist/matebit.html` en el navegador.

### Compilar el APK

`android/build.sh` compila y firma el APK **sin Android Studio ni Gradle**; probado en Ubuntu 24.04:

```bash
sudo apt install default-jdk-headless aapt apksigner zipalign dalvik-exchange libandroid-23-java
./android/build.sh          # genera dist/matebit.apk
```

Si no existe `android/matebit.keystore`, el script crea una clave nueva. Un APK firmado con **otra** clave no se
instala encima de uno anterior: hay que desinstalar, y se pierde el récord guardado.

## Publicar una versión nueva (para quien mantiene el repositorio)

1. Sube `versionCode` (siempre un número mayor) y `versionName` en `android/AndroidManifest.xml`.
2. Compila con **la misma clave de siempre**: copia `matebit.keystore` a `android/` y ejecuta `./android/build.sh`.
3. Crea la *release* con el APK adjunto, en la web (*Releases → Draft a new release*) o con GitHub CLI:

   ```bash
   gh release create v1.3 dist/matebit.apk --title "MateBit 1.3" --notes "Qué cambia en esta versión"
   ```

## Estado de las pruebas

- **Android:** APK probado en un móvil Android real por el autor.

## Notas sobre los puzles

La API de Lichess es pública y de uso libre dentro de sus [condiciones](https://lichess.org/terms-of-service),
que se reservan límites y la revocación del acceso. Si el juego llegara a tener mucho uso, lo prudente es empaquetar
un subconjunto de la [base de datos de puzles](https://database.lichess.org/#puzzles) (licencia CC0) en la propia app.

## Licencia

## Regenerar los iconos

```bash
pip install pillow fonttools brotli
python3 tools/make_icons.py
```
