# Búsqueda exhaustiva

Este programa simula el posicionamiento de un robot que parte de una posición teórica `B` y debe encontrar la posición real de montaje `A`. Como no tiene información que indique hacia qué lado está el objetivo, explora posiciones en ambos sentidos. Incluye dos estrategias: búsqueda primero en anchura (BFS) y búsqueda primero en profundidad (DFS).

## Cómo funciona, paso a paso

### 1. Simula la palpación

La función `palpar(posicion, objetivo)` representa el sensor de contacto. Devuelve verdadero únicamente cuando la posición probada coincide exactamente con `A`.

### 2. Ejecuta BFS

1. Si `B` ya coincide con `A`, termina y devuelve el camino `[B]`.
2. En caso contrario, coloca la posición inicial y su camino en una cola. Mantiene además un conjunto de posiciones visitadas para no repetir estados.
3. Toma de la cola la posición más antigua pendiente de explorar y cuenta ese nodo.
4. Genera los dos vecinos: avanzar `delta` y retroceder `delta`.
5. Descarta los vecinos visitados y aquellos cuya distancia respecto de `B` supera el límite.
6. Marca cada vecino válido como visitado y añade su posición al camino.
7. Si el sensor confirma que ese vecino es `A`, devuelve el camino. Si no, lo agrega al final de la cola.
8. Repite el proceso hasta hallar `A` o agotar la cola.

Como la cola procesa los estados por capas, BFS encuentra el objetivo con la menor cantidad de movimientos entre los estados alcanzables dentro del límite.

### 3. Ejecuta DFS

1. También termina inmediatamente si la posición inicial es el objetivo.
2. Si no, coloca el estado inicial en una pila.
3. Saca el último estado agregado. Si ya fue visitado, lo ignora; de lo contrario, lo marca y aumenta el contador de nodos explorados.
4. Comprueba si la posición actual es el objetivo. Si lo es, devuelve el camino.
5. Si no, agrega a la pila los vecinos válidos que no hayan sido visitados ni excedan el límite.
6. Como una pila procesa primero el último estado agregado, DFS puede avanzar bastante en un sentido antes de explorar el otro.

DFS puede consumir menos memoria que BFS, pero no garantiza encontrar primero el camino más corto. Si la pila se agota, devuelve que no encontró el objetivo.

### 4. Muestra los resultados

El programa ejecuta ambas estrategias con los mismos parámetros e imprime el camino, el número de movimientos y los nodos explorados. Si ninguna encuentra el objetivo dentro del rango permitido, informa que no se encontró.

## Parámetros

- `inicial`: posición inicial `B` (por defecto, `50`).
- `objetivo`: posición real `A` (por defecto, `67`).
- `--delta` / `-d`: tamaño de cada movimiento (por defecto, `1`).
- `--limite` / `-l`: distancia máxima de exploración desde la posición inicial (por defecto, `100`).

## Ejecución

Desde esta carpeta, ejecutar con los valores predeterminados:

```bash
python3 busqueda_exhaustiva.py
```

También se pueden indicar posiciones y opciones, por ejemplo:

```bash
python3 busqueda_exhaustiva.py 50 67 --delta 1 --limite 100
```

Con los valores predeterminados, BFS encuentra `67` partiendo de `50` en 17 movimientos. Aunque explora ambos lados para asegurar que no haya un objetivo más cercano, el camino devuelto hasta ese objetivo es `[50, 51, 52, ..., 67]`.

## Limitaciones

- La cantidad de posiciones examinadas crece con la distancia al objetivo.
- El límite evita que la exploración se extienda indefinidamente.
- El programa solo verifica coincidencia exacta y no utiliza información del entorno para orientar la búsqueda.
