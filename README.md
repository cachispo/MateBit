# MateBit ♞

Puzles de ajedrez infinitos con estética de 8 bits, en **blanco y negro puro** (1 bit).
Tablero oscuro pensado para jugar de noche, piezas ♔♕♖♗♘♙♚♛♜♝♞♟ y pitidos de máquina recreativa.

- Puzles nuevos sin fin, pedidos a la [API de Lichess](https://lichess.org/api) (`/api/puzzle/next`).
- Tres vidas, racha, puntos, pista y récord (guardado en el dispositivo).
- Reserva de 25 puzles guardados para jugar sin conexión.
- Sin dependencias en ejecución: todo (código, motor de ajedrez y tipografías) va dentro de un único HTML.

## Estructura

```
src/        el juego: index.html (plantilla), style.css, app.js
vendor/     chess.js y tipografías (con sus licencias)
tools/      build.py (genera todo) y make_icons.py (iconos)
dist/       matebit.html: un solo fichero que abre cualquier navegador
docs/       la PWA para GitHub Pages (instalable en Android e iOS)
android/    app Android (WebView) + build.sh que compila y firma el APK
ios/        fuentes Swift para Xcode (ver ios/LEEME.md)
```

Tras editar algo en `src/`, ejecuta `python3 tools/build.py` para regenerar `dist/`, `docs/` y las apps.
Los resultados generados también están en el repositorio para que funcione nada más clonarlo.

## Jugar ya

Abre `dist/matebit.html` en cualquier navegador.

## Publicarlo como web instalable (Android e iOS) con GitHub Pages

1. Sube el repositorio a GitHub.
2. En el repositorio: **Settings → Pages → Build and deployment → Deploy from a branch**,
   rama `main`, carpeta **`/docs`**.
3. Tras un minuto estará en `https://TU_USUARIO.github.io/NOMBRE_DEL_REPO/`.
4. Instalación en el móvil:
   - **Android (Firefox o Chrome):** menú ⋮ → *Instalar* (o *Añadir a la pantalla de inicio*).
   - **iPhone/iPad:** hay que abrirla con **Safari** → botón Compartir → *Añadir a pantalla de inicio*.
     (Los demás navegadores de iOS no instalan webs.)

Una vez instalada se abre a pantalla completa, con su icono, y funciona sin conexión
(la reserva de puzles se rellena sola mientras haya red).

## Android (APK)

`android/build.sh` compila y firma el APK **sin Android Studio ni Gradle**; probado en Ubuntu 24.04:

```bash
sudo apt install default-jdk-headless aapt apksigner zipalign dalvik-exchange libandroid-23-java
./android/build.sh          # genera dist/matebit.apk
```

- La app es un `WebView` que sirve `index.html` desde `assets/` bajo un origen https interno,
  de modo que `localStorage` y las llamadas a Lichess funcionan como en una web normal.
- La primera vez crea `android/matebit.keystore`. **Guarda una copia**: con otra clave, Android no deja
  actualizar encima de una instalación previa (habría que desinstalar y se perdería el récord).
  El `.gitignore` impide subirla por error.
- Para instalar: copia el APK al móvil y ábrelo (hay que permitir "instalar apps desconocidas").
- Para **Google Play** este APK no sirve tal cual: hace falta un paquete AAB, una clave de firma propia,
  una versión de Android objetivo más reciente y los requisitos de la consola de desarrolladores.

## iOS (app nativa)

No se puede compilar sin un Mac con Xcode. Las fuentes (`ios/MateBit/`) y los pasos están en
[`ios/LEEME.md`](ios/LEEME.md). Si solo quieres jugar en el iPhone, la web instalable de arriba es lo más sencillo.

## Estado de las pruebas

- Web (`dist/` y `docs/`): probada en Chromium emulando un móvil (jugar, errores, reserva sin conexión,
  service worker, arranque sin red).
- Android: el APK se construye y verifica (firma, alineado, manifiesto), pero **no está probado en un Android real**.
- iOS (PWA y fuentes Swift): **sin probar**; no se ha podido ejecutar Safari ni Xcode.

## Notas sobre los puzles

La API de Lichess es pública y de uso libre dentro de sus [condiciones](https://lichess.org/terms-of-service),
que se reservan límites y la revocación del acceso. Si el juego llegara a tener mucho uso, lo prudente es empaquetar
un subconjunto de la [base de datos de puzles](https://database.lichess.org/#puzzles) (licencia CC0) en la propia app.

## Licencia

Aún sin elegir: añade un fichero `LICENSE` con la que prefieras. Material de terceros y sus licencias en
[`THIRD_PARTY.md`](THIRD_PARTY.md).

## Regenerar los iconos

```bash
pip install pillow fonttools brotli
python3 tools/make_icons.py
```
