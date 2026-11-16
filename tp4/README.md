# Trabajo Practico N°4: 
## Detección de rectas y circunferencias con Transformada de Hough

El archivo `transformada_hough.py` reúne los dos prototipos.\
Recibe primero el tipo de transformada y luego la imagen.\
Analiza la imagen, informa las figuras encontradas y guarda una copia.\
Se utilizó una imagen alternativa en 2D descargada de Internet de ejemplo (diferente a la de la situación problemática),
adjunta en el repositorio, de nombre: `motor_ejemplo_tp4_inteligencia_artificial.jpg` para simplificar su analisis con los prototipos, según indicó que se podía hacer el profesor en la clase de sincronización de este TP.

## Instalación

Se necesita Python 3.9 o posterior y `pip`. En la carpeta de este proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Activar con `.venv\Scripts\activate`. Si la creación del entorno falla por falta de `venv`, instalar el paquete de soporte correspondiente a la distribución de Python. Se usa OpenCV sin interfaz gráfica; no es necesario abrir una ventana.

## Uso

```bash
python transformada_hough.py recta "motor_ejemplo_tp4_inteligencia_artificial.jpg"
python transformada_hough.py circunsferencia "motor_ejemplo_tp4_inteligencia_artificial.jpg"
```

La sintaxis general es:

```text
python transformada_hough.py {recta,circunsferencia} IMAGEN [opciones]
```

Por defecto se guarda, junto a la entrada, un PNG con el nombre original seguido de `_output_recta` o `_output_circunsferencia`. Por ejemplo, para la imagen incluida se generan `motor_ejemplo_tp4_inteligencia_artificial_output_recta.png` y `motor_ejemplo_tp4_inteligencia_artificial_output_circunsferencia.png`. Para elegir otro destino:

```bash
python transformada_hough.py circunsferencia "motor_ejemplo_tp4_inteligencia_artificial.jpg" -o resultado.png
```

La carpeta de destino debe existir. El programa protege la imagen original frente a una ruta de salida idéntica. Muestra errores de lectura o escritura en la salida de error y termina con código 1; argumentos inválidos producen código 2. Si no encuentra figuras, informa cero y guarda igualmente la imagen sin marcas.

### Salida

- **Recta:** imagen con segmentos rojos y, en la consola, cantidad, extremos `(x1, y1) - (x2, y2)` y longitud aproximada en píxeles. Son segmentos detectados, no necesariamente piezas distintas: un borde puede aparecer varias veces.
- **Circunferencia:** imagen con contornos verdes, centros y números rojos. La consola muestra la cantidad y, por cada número, centro `(x, y)` y radio, redondeados a píxeles. El origen está en la esquina superior izquierda; `x` crece hacia la derecha e `y` hacia abajo. Estas coordenadas no son milímetros ni coordenadas del robot.

Se pueden guardar los datos de consola con `> detecciones.txt`.

### Opción de salida

La opción `-o` o `--salida` permite indicar la ruta del archivo resultante. Para consultar la ayuda completa: `python transformada_hough.py --help`.

Los valores de detección están definidos como constantes en el código y se eligieron para la imagen proporcionada. Pueden modificarse allí para trabajar con otras imágenes. La distancia mínima entre centros puede hacer que se devuelva solo una de varias circunferencias concéntricas.

## Desarrollo y análisis

### Caso 1: rectas

Se pasa la imagen a escala de grises, se suaviza con un filtro gaussiano y se aplica Canny para obtener bordes. Luego `HoughLinesP` realiza una variante probabilística de la transformada y devuelve segmentos, que se dibujan sobre la imagen. La representación polar de una recta es `ρ = x cos(θ) + y sen(θ)`: los píxeles de borde votan por combinaciones de parámetros y los picos indican posibles rectas. Esta representación también admite rectas verticales, para las que la pendiente de `y = mx + b` no está definida.

**Ventajas:** integra información de varios píxeles y puede recuperar segmentos aunque el borde tenga pequeñas interrupciones; ofrece longitud y extremos útiles para estimar una orientación. **Limitaciones:** sombras, texturas y contornos de piezas pueden producir rectas ajenas al objeto buscado; un mismo borde puede generar varias detecciones. La perspectiva y la elección de umbrales también afectan el resultado.

### Caso 2: circunferencias

Tras convertir y suavizar la imagen, se aplica `HoughCircles` con el método de gradiente de OpenCV. El método usa información de bordes y gradientes para proponer centros y radios. La familia de circunferencias se describe por `(x-a)² + (y-b)² = r²`: el centro es `(a, b)` y `r` el radio. En el planteo conceptual del enunciado, si el radio es conocido, se buscan centros en un espacio de dos parámetros; aquí OpenCV busca radios dentro de un intervalo definido en el código, por lo que no se afirma que implemente literalmente ese acumulador bidimensional.

**Ventajas:** puede localizar el centro de contornos circulares aun con interrupciones moderadas y acotar radios ayuda a descartar otros tamaños. **Limitaciones:** el umbral y el rango de radios cambian los resultados; varios círculos próximos o concéntricos pueden suprimirse por la distancia mínima entre centros. Una circunferencia vista con perspectiva puede aparecer como elipse, y la oclusión, iluminación y textura pueden causar falsos positivos o pérdidas.

## Fuentes

- **Módulo 4, Lectura 3**, «Percepción y navegación robótica», especialmente pp. 8–10: etapas de visión artificial y transformada de Hough en coordenadas polares.
- **TP4, Situación problemática**, pp. 3–5: desplazamiento del motor, aro C, centro A y caso de radio conocido.
- Escalera, A. (2001). *Visión por computador: fundamentos y métodos*. Prentice Hall. Obra citada en las referencias de la Lectura 3; se incluye como bibliografía complementaria, sin atribuirle afirmaciones no verificadas directamente en ella.
