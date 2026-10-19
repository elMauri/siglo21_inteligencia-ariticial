# Prototipo de red de Hopfield

El archivo `prototipo_hopfield.py` implementa una demostración de una **red neuronal de Hopfield** para recuperar un patrón a partir de una imagen con ruido. Compara dos métodos de entrenamiento: la regla de **Hebb** y la **pseudoinversa**.

## Qué hace el programa

1. Genera tres imágenes de 10 × 10 píxeles con un aro de radio aproximado de 2 píxeles, centrado en las posiciones `(3, 3)`, `(6, 3)` y `(5, 6)`. Las coordenadas se expresan como `(x, y)` y van de 0 a 9.
2. Representa cada imagen con valores bipolares: `1` para el aro y `-1` para el fondo. Cada píxel corresponde a una neurona, por lo que la red tiene 100 neuronas.
3. Toma el patrón con centro `(6, 3)` e invierte cinco píxeles para simular ruido. Los índices utilizados, sobre la imagen aplanada por filas, son `9`, `17`, `27`, `64` y `88`.
4. Entrena una matriz de pesos con cada método. En ambos casos elimina las conexiones de cada neurona consigo misma y simetriza la matriz.
5. Intenta recuperar la imagen mediante actualizaciones asíncronas: actualiza las neuronas una por una, en orden fijo, utilizando el estado disponible en ese momento. Se detiene cuando un barrido completo no produce cambios o cuando alcanza 30 barridos.
6. Compara la salida con los tres patrones memorizados. Solo informa un centro reconocido si coincide exactamente con alguno; en caso contrario muestra `None`.

Los patrones y el ruido se generan dentro del código: **no se necesitan imágenes, archivos de datos ni entradas por teclado**. El orden de actualización y los píxeles alterados son fijos para que la demostración sea reproducible.

## Requisitos

- Python 3.
- NumPy.

## Instalación y ejecución

Abrí una terminal en la carpeta donde está `prototipo_hopfield.py`. Se recomienda crear un entorno virtual para instalar la dependencia.

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy
python prototipo_hopfield.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy
.\.venv\Scripts\python.exe prototipo_hopfield.py
```

Si ya tenés Python y NumPy disponibles en tu entorno, basta con ejecutar:

```bash
python prototipo_hopfield.py
```

En sistemas donde el comando de Python 3 sea `python3`, usá `python3 prototipo_hopfield.py`.

## Parámetros y configuración

**El script no admite parámetros de línea de comandos.** Al ejecutarlo, corre automáticamente la misma demostración con ambos métodos de entrenamiento.

Para modificar el experimento, editá estos valores en el código:

| Valor | Ubicación | Función |
| --- | --- | --- |
| `N = 10` | Inicio del archivo | Define el ancho y alto de las imágenes. |
| `POSICIONES` | Inicio del archivo | Define los centros de los patrones memorizados. |
| `original = patrones[1]` | `ejecutar()` | Selecciona el patrón al que se añade ruido. |
| `indices = [9, 17, 27, 64, 88]` | `ejecutar()` | Define los píxeles que se invierten. |
| `max_barridos=30` | `recuperar()` | Establece el máximo de barridos para recuperar una imagen. |

Si cambiás el tamaño o las posiciones, ajustá también los índices de ruido y la selección del patrón cuando corresponda. Los índices deben estar entre `0` y `N * N - 1`. El texto que anuncia el centro esperado también está fijado en `ejecutar()` y debe actualizarse si cambiás el patrón elegido.

## Cómo interpretar la salida

El programa imprime en la terminal:

- Los tres patrones utilizados para entrenar.
- La imagen alterada por el ruido.
- El resultado de cada método, con la cantidad de barridos realizados, el centro reconocido y las diferencias respecto de cada patrón.

Las imágenes se dibujan con `X` para los píxeles del aro y espacios para el fondo. La lista de diferencias sigue el orden de `POSICIONES`: cada número indica cuántos píxeles difieren del patrón correspondiente. Un `0` indica una coincidencia exacta.

La cantidad de barridos incluye el barrido final sin cambios cuando se detecta estabilidad. Si se llega al máximo de barridos, la función devuelve el último estado sin indicar por separado si logró estabilizarse. Una salida estable puede no coincidir con un patrón memorizado; por eso el centro reconocido puede ser `None`.

El script no guarda archivos ni abre ventanas gráficas.

## Problemas frecuentes

- **`ModuleNotFoundError: No module named 'numpy'`**: instalá NumPy en el mismo entorno de Python con el que ejecutás el script, usando `python -m pip install numpy`.
- **No se encuentra el archivo**: verificá que la terminal esté ubicada en la carpeta del script o ejecutalo indicando su ruta completa.
