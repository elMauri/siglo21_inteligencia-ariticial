#!/usr/bin/env python3
"""Proceso de búsqueda exhaustiva para el problema del posicionamiento de montaje.

Escenario simplificado:
- El robot conoce su posicion nominal "B" sobre la horizontal H.
- El punto de montaje real "A" se desplazo por un valor desconocido hacia la
  izquierda o la derecha.
- El robot no dispone de una heuristica, por lo que debe explorar ordenadamente
  ambos sentidos de H hasta "palpar" la posicion correcta.
- Cada movimiento avanza un incremento fijo "delta_h" y luego se verifica si la
  posicion alcanzada coincide con "A".
"""

import argparse
from collections import deque


def palpar(posicion, objetivo):
    """Simula la accion del sensor: indica si se halla en el punto de montaje."""
    return posicion == objetivo


def busqueda_exhaustiva_bfs(inicial, objetivo, paso=1, limite=1000):
    """Busqueda exhaustiva primero en anchura (BFS) sobre la recta H.

    Explora por capas desde la posicion inicial, alternando ambos sentidos,
    lo que garantiza que el primer objetivo encontrado sea el mas cercano en
    numero de movimientos.

    Retorna:
        (camino, nodos_explorados) o (None, nodos_explorados) si no se halla.
    """
    if inicial == objetivo:
        return [inicial], 0

    frontera = deque([(inicial, [inicial])])
    visitados = {inicial}
    nodos_explorados = 0

    while frontera:
        actual, camino = frontera.popleft()
        nodos_explorados += 1

        for siguiente in (actual + paso, actual - paso):
            if siguiente in visitados:
                continue
            if abs(siguiente - inicial) > limite:
                continue

            visitados.add(siguiente)
            camino_nuevo = camino + [siguiente]

            if palpar(siguiente, objetivo):
                return camino_nuevo, nodos_explorados

            frontera.append((siguiente, camino_nuevo))

    return None, nodos_explorados


def busqueda_exhaustiva_dfs(inicial, objetivo, paso=1, limite=1000):
    """Busqueda exhaustiva primero en profundidad (DFS) sobre la recta H.

    Se incluye con fines comparativos. DFS consume menos memoria, pero para este
    problema puede alejarse primero en una direccion arbitraria y no garantiza
    la solucion mas cercana.
    """
    if inicial == objetivo:
        return [inicial], 0

    pila = [(inicial, [inicial])]
    visitados = set()
    nodos_explorados = 0

    while pila:
        actual, camino = pila.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_explorados += 1

        if palpar(actual, objetivo):
            return camino, nodos_explorados

        for siguiente in (actual + paso, actual - paso):
            if siguiente in visitados:
                continue
            if abs(siguiente - inicial) > limite:
                continue
            pila.append((siguiente, camino + [siguiente]))

    return None, nodos_explorados


def main():
    parser = argparse.ArgumentParser(
        description="Busqueda exhaustiva para posicionamiento de montaje robotico."
    )
    parser.add_argument(
        "inicial", type=int, nargs="?", default=50,
        help="Posicion inicial del robot B (default: 50)"
    )
    parser.add_argument(
        "objetivo", type=int, nargs="?", default=67,
        help="Posicion objetivo real A (default: 67)"
    )
    parser.add_argument(
        "--delta", "-d", type=int, default=1,
        help="Incremento de cada palpacion (default: 1)"
    )
    parser.add_argument(
        "--limite", "-l", type=int, default=100,
        help="Rango maximo de exploracion (default: 100)"
    )
    args = parser.parse_args()

    posicion_b = args.inicial
    posicion_a = args.objetivo
    delta_h = args.delta
    limite = args.limite

    print("=" * 60)
    print("BUSQUEDA EXHAUSTIVA: POSICIONAMIENTO DE MONTAJE")
    print("=" * 60)
    print(f"Posicion teorica B      : {posicion_b}")
    print(f"Posicion real A         : {posicion_a}")
    print(f"Incremento de palpacion : {delta_h}")
    print(f"Rango maximo de bisqueda: {limite}")
    print()

    # BFS
    camino_bfs, explorados_bfs = busqueda_exhaustiva_bfs(
        posicion_b, posicion_a, delta_h, limite
    )
    print("--- Primero en anchura (BFS) ---")
    if camino_bfs:
        print(f"Camino recorrido: {camino_bfs}")
        print(f"Movimientos hasta A: {len(camino_bfs) - 1}")
        print(f"Nodos explorados: {explorados_bfs}")
    else:
        print("No se encontro la posicion A dentro del limite.")
    print()

    # DFS
    camino_dfs, explorados_dfs = busqueda_exhaustiva_dfs(
        posicion_b, posicion_a, delta_h, limite
    )
    print("--- Primero en profundidad (DFS) ---")
    if camino_dfs:
        print(f"Camino recorrido: {camino_dfs}")
        print(f"Movimientos hasta A: {len(camino_dfs) - 1}")
        print(f"Nodos explorados: {explorados_dfs}")
    else:
        print("No se encontro la posicion A dentro del limite.")
    print()

    print("=" * 60)
    print("ANALISIS DEL METODO")
    print("=" * 60)
    print(
        "BFS resulta mas conveniente para este problema porque el desplazamiento\n"
        "de A respecto de B es desconocido y puede estar a cualquiera de los dos\n"
        "lados. Al expandir las posiciones por capas (B+1, B-1, B+2, B-2, ...),\n"
        "garantiza hallar la solucion con la menor cantidad de movimientos y, por\n"
        "tanto, con el menor recorrido del brazo robotizado."
    )
    print()
    print(
        "DFS consume menos memoria, pero en un espacio lineal sin orientacion\n"
        "prefiere avanzar en una sola direccion hasta el limite. Si el objetivo\n"
        "esta del lado opuesto, recorre muchas posiciones innecesarias antes de\n"
        "dar con A, aumentando el tiempo de parada de la linea."
    )
    print()
    print("Limitaciones comunes:")
    print("- Crecimiento lineal del numero de palpaciones con la distancia |A - B|.")
    print("- Requiere un criterio de parada (limite) para evitar exploracion infinita.")
    print("- No aprovecha informacion del entorno; solo verifica cada posicion.")


if __name__ == "__main__":
    main()
