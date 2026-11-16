#!/usr/bin/env python3
"""Detección ilustrativa de rectas y circunferencias con la transformada de Hough."""
import argparse
import math
from pathlib import Path
import sys

import cv2
import numpy as np

# Valores ajustados para la imagen de ejemplo; se pueden modificar en el código.
UMBRAL_RECTAS = 80
LONGITUD_MINIMA = 60
SEPARACION_MAXIMA = 10
RADIO_MIN = 10
RADIO_MAX = 110
DISTANCIA_CENTROS = 25
UMBRAL_CIRCULOS = 70


def argumentos():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tipo', choices=('recta', 'circunsferencia'), help='tipo de figura a detectar')
    parser.add_argument('imagen', type=Path, help='ruta de la imagen de entrada')
    parser.add_argument('-o', '--salida', type=Path, help='ruta de la imagen de salida (PNG o JPG)')
    return parser.parse_args()


def main():
    args = argumentos()
    imagen = cv2.imread(str(args.imagen), cv2.IMREAD_COLOR)
    if imagen is None:
        print(f'Error: no se pudo leer la imagen: {args.imagen}', file=sys.stderr)
        return 1
    destino = args.salida or args.imagen.with_name(f'{args.imagen.stem}_output_{args.tipo}.png')
    if destino.resolve() == args.imagen.resolve():
        print('Error: la imagen de salida debe ser diferente de la entrada.', file=sys.stderr)
        return 1
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (5, 5), 1.2)
    resultado = imagen.copy()
    if args.tipo == 'recta':
        bordes = cv2.Canny(gris, 50, 150)
        figuras = cv2.HoughLinesP(bordes, 1, np.pi / 180, UMBRAL_RECTAS,
                                  minLineLength=LONGITUD_MINIMA, maxLineGap=SEPARACION_MAXIMA)
        lineas = [] if figuras is None else figuras.reshape(-1, 4).tolist()
        lineas.sort(key=lambda p: (p[0], p[1], p[2], p[3]))
        print(f'Segmentos detectados: {len(lineas)}')
        for i, (x1, y1, x2, y2) in enumerate(lineas, 1):
            cv2.line(resultado, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)
            print(f'{i}: ({x1}, {y1}) - ({x2}, {y2}); longitud={math.hypot(x2-x1, y2-y1):.1f} px')
    else:
        figuras = cv2.HoughCircles(gris, cv2.HOUGH_GRADIENT, dp=1, minDist=DISTANCIA_CENTROS,
                                   param1=100, param2=UMBRAL_CIRCULOS,
                                   minRadius=RADIO_MIN, maxRadius=RADIO_MAX)
        circulos = [] if figuras is None else np.rint(figuras[0]).astype(int).tolist()
        circulos.sort(key=lambda c: (c[0], c[1], c[2]))
        print(f'Circunferencias detectadas: {len(circulos)}')
        for i, (x, y, radio) in enumerate(circulos, 1):
            cv2.circle(resultado, (x, y), radio, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.circle(resultado, (x, y), 3, (0, 0, 255), -1, cv2.LINE_AA)
            cv2.putText(resultado, str(i), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1, cv2.LINE_AA)
            print(f'{i}: centro=({x}, {y}); radio={radio} px')
    try:
        if not cv2.imwrite(str(destino), resultado):
            raise OSError('OpenCV no pudo guardar el archivo')
    except (cv2.error, OSError) as exc:
        print(f'Error al guardar {destino}: {exc}', file=sys.stderr)
        return 1
    print(f'Imagen guardada en: {destino}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
