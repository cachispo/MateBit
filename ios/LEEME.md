# MateBit en iOS (Xcode)

> **Sin probar.** Estas fuentes se escribieron sin acceso a Xcode ni a un iPhone. Son pocas líneas y estándar
> (SwiftUI + `WKWebView`), pero puede que haga falta algún retoque.

## Qué necesitas

- Un Mac con **Xcode** (versión reciente; el proyecto apunta a iOS 15 o superior).
- Un **Apple ID**. Con la cuenta gratuita puedes instalarla en tu propio iPhone, pero la firma caduca a los
  **7 días** y hay que volver a instalarla. Para TestFlight o App Store hace falta el *Apple Developer Program*
  (de pago, según tengo entendido unos 99 dólares al año).

## Pasos

1. Xcode → **File → New → Project… → iOS → App**. Nombre `MateBit`, *Interface:* SwiftUI, *Language:* Swift.
2. Borra del proyecto los ficheros que crea Xcode (`MateBitApp.swift` y `ContentView.swift`).
3. Arrastra al proyecto, marcando *Copy items if needed* y el *target* MateBit, estos tres ficheros de `ios/MateBit/`:
   - `MateBitApp.swift`
   - `GameView.swift`
   - `index.html` (debe aparecer en *Build Phases → Copy Bundle Resources*)
4. **Icono:** en `Assets.xcassets → AppIcon`, arrastra `ios/AppIcon-1024.png` al hueco de 1024 px.
5. **Solo vertical:** en el *target* → *General → Deployment Info*, deja marcado solo *Portrait*.
6. **Fondo negro al arrancar:** en *Info* añade la clave *Launch Screen* (`UILaunchScreen`) y dentro
   *Background color* con un color negro; así no hay destello blanco.
7. Elige tu iPhone (o un simulador), pulsa ▶ y, en el iPhone, confía en tu perfil en
   *Ajustes → General → VPN y gestión de dispositivos*.

## Cómo funciona

`GameView.swift` carga `index.html` con `loadHTMLString` y la URL base ficticia `https://appassets.local/`
para que `localStorage` y las peticiones a Lichess se comporten como en una web normal.
Bloquea la navegación a cualquier otro sitio. El CSS ya respeta la muesca y la isla dinámica con `env(safe-area-inset-*)`.

Si cambias el juego, ejecuta `python3 tools/build.py` y vuelve a arrastrar el nuevo `ios/MateBit/index.html`
(o sustitúyelo en el proyecto).
