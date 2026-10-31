#!/usr/bin/env python3
"""Genera todas las salidas de MateBit a partir de src/ y vendor/ (solo biblioteca estándar).

  dist/matebit.html           un solo fichero que se abre en cualquier navegador
  docs/                       PWA para GitHub Pages (instalable en Android e iOS)
  android/assets/index.html   contenido de la app Android
  ios/MateBit/index.html      contenido de la app iOS

Uso:  python3 tools/build.py
"""
import base64
import hashlib
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKERS = ['<!--HEAD-->', '<!--STYLE-->', '<!--CHESS-->', '<!--APP-->', '<!--TAIL-->']


def text(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def b64(rel):
    return base64.b64encode((ROOT / rel).read_bytes()).decode()


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        p.write_bytes(content)
    else:
        p.write_text(content, encoding='utf-8')
    print('  %-30s %7d bytes' % (rel, len(content)))


FONTS = (
    "@font-face { font-family: 'Press Start 2P'; font-style: normal; font-weight: 400; font-display: swap;\n"
    "  src: url(data:font/woff2;base64,%s) format('woff2'); }\n"
    "@font-face { font-family: 'AjedrezPiezas'; font-style: normal; font-weight: 400; font-display: block;\n"
    "  src: url(data:font/woff2;base64,%s) format('woff2'); unicode-range: U+2654-265F, U+FE0E; }\n"
) % (b64('vendor/press-start-2p-latin.woff2'), b64('vendor/piezas.woff2'))

HEAD_PWA = '''<link rel="manifest" href="manifest.webmanifest">
  <link rel="icon" type="image/png" href="icon-192.png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="MateBit">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">'''

TAIL_PWA = '''<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('sw.js').catch(function () { /* sin service worker: sigue funcionando en línea */ });
  });
}
</script>'''

SW = '''// Service worker de MateBit: guarda la app para abrirla sin conexión.
// La versión cambia sola cuando cambia el contenido (la calcula tools/build.py).
const VERSION = 'matebit-%s';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  const url = new URL(req.url);
  // Solo lo propio; la API de Lichess va siempre directa a la red.
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit =>
      hit || fetch(req).catch(() => (req.mode === 'navigate' ? caches.match('./index.html') : Response.error()))
    )
  );
});
'''


def page(head='', tail=''):
    html = text('src/index.html')
    html = html.replace('<!--HEAD-->', head)
    html = html.replace('<!--STYLE-->', '<style>\n' + FONTS + text('src/style.css') + '\n</style>')
    for rel in ('vendor/chess.js', 'src/app.js'):
        assert '</script' not in text(rel), rel
    html = html.replace('<!--CHESS-->', '<script>\n' + text('vendor/chess.js') + '\n</script>')
    html = html.replace('<!--APP-->', '<script>\n' + text('src/app.js') + '\n</script>')
    html = html.replace('<!--TAIL-->', tail)
    for m in MARKERS:
        assert m not in html, 'marcador sin sustituir: ' + m
    assert 'googleapis' not in html and 'cdnjs' not in html
    return html


def main():
    print('Generando MateBit...')
    plain = page()
    write('dist/matebit.html', plain)
    write('android/assets/index.html', plain)
    write('ios/MateBit/index.html', plain)

    pwa = page(HEAD_PWA, TAIL_PWA)
    write('docs/index.html', pwa)
    write('docs/sw.js', SW % hashlib.sha1(pwa.encode('utf-8')).hexdigest()[:10])
    write('docs/manifest.webmanifest', json.dumps({
        'name': 'MateBit',
        'short_name': 'MateBit',
        'description': 'Puzles de ajedrez infinitos en 1 bit.',
        'lang': 'es',
        'start_url': './',
        'scope': './',
        'display': 'standalone',
        'orientation': 'portrait',
        'background_color': '#000000',
        'theme_color': '#000000',
        'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
        ],
    }, indent=2, ensure_ascii=False) + '\n')
    for name in ('icon-192.png', 'icon-512.png', 'apple-touch-icon.png'):
        shutil.copyfile(ROOT / 'assets' / name, ROOT / 'docs' / name)
    (ROOT / 'docs' / '.nojekyll').touch()
    print('Hecho.')


if __name__ == '__main__':
    main()
