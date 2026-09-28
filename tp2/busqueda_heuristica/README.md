# Búsqueda heurística

Este programa simula un robot que parte de una posición teórica `B` y busca el punto real de montaje `A`. A diferencia de la búsqueda exhaustiva, el robot cuenta con una medición de relieve que estima qué tan cerca está del centro del anillo situado en `A`. La búsqueda usa esa medición para decidir hacia dónde moverse.

## Cómo funciona, paso a paso

### 1. Modela y mide el relieve

- `perfil_anillo(distancia, escala)` simula el perfil del anillo con la fórmula `(distancia / escala) ** 2`. El relieve es mínimo (cero) en el centro y aumenta al alejarse.
- `medir_relieve(posicion, objetivo, escala)` calcula ese perfil según la distancia entre la posición probada y `A`.
- `heuristica(medicion)` compara el relieve medido con el esperado en el objetivo, que por defecto es cero. Un valor heurístico menor indica una posición más prometedora.
- `palpar(posicion, objetivo)` simula el sensor de contacto que confirma si se llegó exactamente a `A`.

### 2. Inicializa la búsqueda

1. Si la posición inicial ya es el objetivo, devuelve el camino `[B]` sin realizar palpaciones.
2. Si no, establece la posición actual en `B`, inicializa el camino con esa posición y la registra como visitada.
3. Inicializa el contador de palpaciones.

### 3. Elige el siguiente movimiento

En cada iteración, hasta alcanzar `max_iter`:

1. Comprueba si la posición actual es el objetivo.
2. Mide el relieve en la posición actual y calcula su heurística.
3. Calcula la medición y la heurística de los dos vecinos (`x + delta` y `x - delta`), descartando posiciones ya visitadas o fuera del límite. Cada medición realizada incrementa el contador de palpaciones.
4. Si no quedan vecinos válidos, retrocede a la posición anterior del camino. Si ya no puede retroceder, termina sin solución.
5. Ordena los candidatos por heurística y selecciona el de menor valor. En caso de empate, el ordenamiento de tuplas usa la posición menor como segundo criterio.
6. Si el mejor candidato no mejora la heurística actual, retrocede un paso para intentar otra opción. Si no hay una posición anterior, termina sin solución.
7. Si mejora, avanza al candidato, lo agrega al camino y lo marca como visitado.

La búsqueda termina cuando confirma `A`, cuando no puede seguir o retroceder, o cuando alcanza el máximo de iteraciones. Devuelve el camino y el número de palpaciones; si no encuentra el objetivo, devuelve `None` y el contador.

### 4. Muestra los resultados

El programa imprime los parámetros utilizados y, si encuentra `A`, muestra el camino, la cantidad de movimientos y las palpaciones realizadas. Si no lo encuentra dentro de las condiciones de búsqueda, lo informa.

## Parámetros

- `inicial`: posición inicial `B` (por defecto, `50`).
- `objetivo`: posición real `A` (por defecto, `67`).
- `--delta` / `-d`: tamaño de cada movimiento (por defecto, `1`).
- `--limite` / `-l`: distancia máxima respecto de la posición inicial (por defecto, `100`).
- `--escala` / `-e`: escala del perfil simulado (por defecto, `10.0`).
- `max_iter`: máximo de iteraciones de la búsqueda (en el código, por defecto, `1000`).

## Ejecución

Desde esta carpeta, ejecutar con los valores predeterminados:

```bash
python3 busqueda_heuristica.py
```

También se pueden indicar posiciones y opciones, por ejemplo:

```bash
python3 busqueda_heuristica.py 50 67 --delta 1 --limite 100 --escala 10
```

Con los valores predeterminados, el relieve disminuye al acercarse a `67`; por eso la búsqueda avanza hacia ese objetivo y lo confirma con el sensor de contacto.

## Ventajas y limitaciones

- Usa información del relieve para orientar la búsqueda y evitar explorar sistemáticamente ambos sentidos.
- Puede requerir menos palpaciones que una búsqueda exhaustiva cuando el perfil guía correctamente hacia el objetivo.
- Depende de que las mediciones y el perfil simulado representen adecuadamente el entorno.
- Un `delta` demasiado grande puede hacer que los movimientos salten sobre el objetivo; la búsqueda solo confirma una coincidencia exacta.
- El máximo de iteraciones también puede detener la búsqueda antes de encontrar una solución.
