#!/usr/bin/env python3
"""Proceso de búsqueda heurística para el posicionamiento de montaje robotizado

Precondiciones:
- El robot conoce su posición nominal "B" sobre la horizontal H.
- El punto de montaje real "A" se desplazó lateralmente un valor desconocido.
- A diferencia de la búsqueda exhaustiva, el brazo dispone de un sensor de relieve
  que le permite estimar, al palpar una posición, qué tan cerca está del punto
  de montaje A.
- El block presenta un anillo prominente con una perforación roscada centrada en
  A. El perfil de relieve medido desde un plano paralelo de referencia tiene un
  valor característico en A (mínimo en el centro del anillo).
- La función heurística h(n) se calcula como la diferencia entre el relieve
  medido y el relieve esperado en A. La búsqueda elige, en cada paso, el
  movimiento que reduce ese valor. Si ninguno mejora, retrocede y prueba el
  sentido contrario.

Método: búsqueda local por descenso de colinas (hill climbing) con retroceso.
No es A* ni búsqueda voraz primero el mejor: no mantiene una frontera de
estados pendientes ni calcula f(n) = g(n) + h(n); la decisión es local,
comparando únicamente h de los vecinos inmediatos.
"""

import argparse
import sys


def pedir_valor(mensaje, tipo, valor_defecto):
    """Solicita un valor por teclado; Enter conserva el valor por defecto."""
    while True:
        entrada = input(f"{mensaje} [{valor_defecto}]: ").strip()
        if not entrada:
            return valor_defecto
        try:
            return tipo(entrada)
        except ValueError:
            print("Valor no válido. Intente nuevamente.")


def menu_ejecucion():
    """Muestra el menú inicial y devuelve '1' (default) o '2' (manual)."""
    print("=" * 60)
    print("MENÚ DE EJECUCIÓN")
    print("=" * 60)
    print("1) Ejecutar con valores por defecto")
    print("2) Ingresar valores manualmente")
    while True:
        opcion = input("Seleccione una opción (1/2): ").strip()
        if opcion in ("1", "2"):
            return opcion
        print("Opción inválida. Intente nuevamente.")


def perfil_anillo(distancia, escala=10.0):
    """Modelo del relieve de la cara lateral del block en función de la distancia a A.

    El perfil es suave, simétrico y alcanza su mínimo en 0 (centro del anillo).
    Cuanto mayor sea |distancia|, mayor será el relieve medido.
    """
    return (distancia / escala) ** 2


def medir_relieve(posicion, objetivo, escala=10.0):
    """Simula la lectura del sensor de relieve al apoyarse en 'posicion'."""
    return perfil_anillo(posicion - objetivo, escala)


def palpar(posicion, objetivo):
    """Simula la acción del sensor de contacto: indica si se halla en A."""
    return posicion == objetivo


def heuristica(medicion, relieve_objetivo=0.0):
    """Heurística: distancia entre el relieve medido y el relieve esperado en A."""
    return abs(medicion - relieve_objetivo)


def busqueda_heuristica(inicial, objetivo, paso=1, limite=100, max_iter=1000,
                        escala=10.0):
    """Búsqueda heurística por descenso de colinas con retroceso.

    En cada iteración se mide el relieve en la posición actual y en los dos
    vecinos inmediatos (izquierda y derecha). Se avanza hacia el vecino cuya
    heurística sea menor. Si ninguno mejora, se retrocede un paso y se explora
    la otra dirección.

    Nota: no es A*. No existe una frontera global de estados pendientes ni una
    función de evaluación f(n) = g(n) + h(n); la elección se hace solo con el
    valor h de los vecinos de la posición actual.

    Retorna:
        (camino, palpaciones) o (None, palpaciones) si no se halla A.
    """
    if palpar(inicial, objetivo):
        return [inicial], 0

    x = inicial
    camino = [x]
    visitados = {x}
    palpaciones = 0

    for _ in range(max_iter):
        if palpar(x, objetivo):
            return camino, palpaciones

        rel_actual = medir_relieve(x, objetivo, escala)
        h_actual = heuristica(rel_actual)
        palpaciones += 1

        candidatos = []
        for sentido in (paso, -paso):
            nx = x + sentido
            if abs(nx - inicial) > limite or nx in visitados:
                continue
            rel_n = medir_relieve(nx, objetivo, escala)
            h_n = heuristica(rel_n)
            palpaciones += 1
            candidatos.append((h_n, nx))

        if not candidatos:
            # Sin vecinos válidos dentro del límite; retroceder si es posible.
            if len(camino) > 1:
                camino.pop()
                x = camino[-1]
                continue
            return None, palpaciones

        candidatos.sort()
        h_mejor, nx = candidatos[0]

        if h_mejor >= h_actual:
            # Mínimo local; si no es A, retrocede para evitar quedar atrapado.
            if len(camino) > 1:
                camino.pop()
                x = camino[-1]
                continue
            return None, palpaciones

        x = nx
        camino.append(x)
        visitados.add(x)

    return None, palpaciones


def main():
    parser = argparse.ArgumentParser(
        description="Búsqueda heurística para posicionamiento de montaje robotico."
    )
    parser.add_argument(
        "inicial", type=int, nargs="?", default=50,
        help="Posición inicial del robot B (default: 50)"
    )
    parser.add_argument(
        "objetivo", type=int, nargs="?", default=67,
        help="Posición objetivo real A (default: 67)"
    )
    parser.add_argument(
        "--delta", "-d", type=int, default=1,
        help="Incremento de cada palpación (default: 1)"
    )
    parser.add_argument(
        "--limite", "-l", type=int, default=100,
        help="Rango máximo de exploración (default: 100)"
    )
    parser.add_argument(
        "--escala", "-e", type=float, default=10.0,
        help="Escala del perfil de relieve (default: 10.0)"
    )
    args = parser.parse_args()

    posicion_b = args.inicial
    posicion_a = args.objetivo
    delta_h = args.delta
    limite = args.limite
    escala = args.escala

    # Sin argumentos de línea de comandos, se muestra el menú interactivo.
    if len(sys.argv) == 1:
        if menu_ejecucion() == "2":
            posicion_b = pedir_valor(
                "Posición inicial del robot B", int, posicion_b)
            posicion_a = pedir_valor(
                "Posición objetivo real A", int, posicion_a)
            delta_h = pedir_valor(
                "Incremento de cada palpación", int, delta_h)
            limite = pedir_valor(
                "Rango máximo de exploración", int, limite)
            escala = pedir_valor(
                "Escala del perfil de relieve", float, escala)
        print()

    print("=" * 60)
    print("BÚSQUEDA HEURÍSTICA: POSICIONAMIENTO DE MONTAJE")
    print("=" * 60)
    print(f"Posición teórica B    : {posicion_b}")
    print(f"Posición real A       : {posicion_a}")
    print(f"Incremento de palpación: {delta_h}")
    print(f"Rango máximo de búsqueda: {limite}")
    print(f"Escala del relieve    : {escala}")
    print()

    camino, palpaciones = busqueda_heuristica(
        posicion_b, posicion_a, delta_h, limite, escala=escala
    )

    if camino:
        print("--- Descenso de colinas con retroceso ---")
        print(f"Camino recorrido       : {camino}")
        print(f"Movimientos hasta A    : {len(camino) - 1}")
        print(f"Palpaciones realizadas : {palpaciones}")
    else:
        print("No se encontró la posición A dentro del límite.")
    print()

    print("=" * 60)
    print("ANÁLISIS DEL MÉTODO")
    print("=" * 60)
    print(
        "El método heurístico implementado es una búsqueda local por descenso\n"
        "de colinas (hill climbing) con retroceso, guiada por el relieve del\n"
        "block. En cada paso el robot palpa los puntos B + delta y B - delta\n"
        "y elige el que reduce la diferencia entre el relieve medido y el\n"
        "relieve esperado en A. Como el perfil del anillo tiene un mínimo en A,\n"
        "reducir esa diferencia equivale a acercarse al punto de montaje."
    )
    print()
    print("Características:")
    print("- Usa información del entorno (relieve) para orientar la búsqueda.")
    print("- No requiere explorar ambos sentidos simultáneamente.")
    print("- Realiza retrocesos si un camino deja de mejorar la heurística.")
    print("- El número de palpaciones crece de forma mucho menor que en BFS.")
    print("- Es un método local: no es A*; no usa una frontera de estados")
    print("  pendientes ni la función de evaluación f(n) = g(n) + h(n).")
    print()
    print("Ventajas:")
    print("- Mayor eficiencia: evita recorrer todo el espacio de estados.")
    print("- Decide localmente en cada paso, lo que lo hace sencillo de ejecutar.")
    print("- Aprovecha el conocimiento del perfil patrón del block.")
    print()
    print("Limitaciones:")
    print("- La calidad depende de la precisión del sensor y del perfil patrón.")
    print("- Un paso delta demasiado grande puede hacer saltar sobre A.")
    print()
    print("Justificación del método elegido:")
    print(
        "Para este problema, el descenso de colinas es el más apropiado\n"
        "porque el robot dispone de información directa (relieve) que indica\n"
        "hacia qué lado se encuentra A en la recta H. A diferencia de BFS, no\n"
        "necesita mantener una frontera amplia ni explorar en ambos sentidos a\n"
        "la vez, por lo que reduce el tiempo de parada de la línea.\n"
        "Se descartó A* porque no hay costos diferenciados entre movimientos\n"
        "ni una heurística admisible sobre la distancia restante; el relieve\n"
        "solo permite una decisión local, que es lo que resuelve el descenso\n"
        "de colinas."
    )


if __name__ == "__main__":
    main()
