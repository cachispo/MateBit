#!/usr/bin/env python3
"""Genera el icono 1 bit de MateBit (caballo con marco de píxeles) en todos los tamaños.

Requisitos:  pip install pillow fonttools brotli
Uso:         python3 tools/make_icons.py

Escribe: assets/icon-512.png, assets/icon-192.png, assets/apple-touch-icon.png,
         ios/AppIcon-1024.png y android/res/mipmap-*/ic_launcher.png
"""
import io
import pathlib

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
N = 64  # la imagen base es de 64x64 píxeles; el resto son ampliaciones


def knight_mask():
    font = TTFont(ROOT / 'vendor' / 'piezas.woff2')
    font.flavor = None
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    pil_font = ImageFont.truetype(buf, 46)
    g = Image.new('L', (N, N), 0)
    d = ImageDraw.Draw(g)
    bb = d.textbbox((0, 0), '♞', font=pil_font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((N - w) // 2 - bb[0], (N - h) // 2 - bb[1]), '♞', font=pil_font, fill=255)
    return g.point(lambda v: 255 if v >= 128 else 0).convert('1')


def base_image():
    img = Image.new('1', (N, N), 0)  # fondo negro
    dr = ImageDraw.Draw(img)
    dr.rectangle([3, 3, N - 4, N - 4], outline=1, width=2)  # marco blanco
    dr.rectangle([7, 7, N - 8, N - 8], outline=1, width=1)  # filete interior
    for x, y in [(3, 3), (N - 4, 3), (3, N - 4), (N - 4, N - 4)]:  # esquinas macizas
        dr.rectangle([x - 2, y - 2, x + 2, y + 2], fill=1)
    img.paste(1, mask=knight_mask())
    return img.convert('L')


def save(img, rel):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p)
    print('  ', rel, img.size)


def main():
    base = base_image()
    master = base.resize((512, 512), Image.NEAREST)
    save(master, 'assets/icon-512.png')
    save(base.resize((192, 192), Image.NEAREST), 'assets/icon-192.png')
    save(master.resize((180, 180), Image.LANCZOS).convert('RGB'), 'assets/apple-touch-icon.png')
    save(base.resize((1024, 1024), Image.NEAREST).convert('RGB'), 'ios/AppIcon-1024.png')
    rgba = master.convert('RGBA')
    sizes = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
    for dens, s in sizes.items():
        method = Image.NEAREST if s in (48, 96, 192) else Image.LANCZOS
        save(rgba.resize((s, s), method), 'android/res/mipmap-%s/ic_launcher.png' % dens)


if __name__ == '__main__':
    main()
