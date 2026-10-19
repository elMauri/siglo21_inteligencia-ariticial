import numpy as np

N = 10
# Tres posiciones posibles del aro dentro de la imagen del motor.
POSICIONES = [(3, 3), (6, 3), (5, 6)]  # (x, y), coordenadas 0..9

def aro(cx, cy):
    # Circunferencia discreta: radio aproximado de 2 pixeles.
    y, x = np.indices((N, N))
    distancia = np.sqrt((x - cx)**2 + (y - cy)**2)
    return np.where((distancia >= 1.5) & (distancia <= 2.5), 1, -1).astype(int)

def dibujar(matriz):
    return '\n'.join(''.join('X' if p == 1 else ' ' for p in fila) for fila in matriz)

def entrenar(patrones, metodo='pseudoinversa'):
    P = np.array([p.ravel() for p in patrones], dtype=float).T
    if metodo == 'hebb':
        W = P @ P.T / P.shape[0]
    else:
        W = P @ np.linalg.pinv(P)  # regla de proyeccion/pseudoinversa
    np.fill_diagonal(W, 0)
    return (W + W.T) / 2

def recuperar(imagen, W, max_barridos=30):
    estado = imagen.ravel().copy()
    for barrido in range(1, max_barridos + 1):
        anterior = estado.copy()
        # Actualizacion asincrona, orden fijo para resultados reproducibles
        for i in range(estado.size):
            campo = W[i] @ estado
            if campo > 1e-10:
                estado[i] = 1
            elif campo < -1e-10:
                estado[i] = -1
        if np.array_equal(estado, anterior):
            return estado.reshape(N, N), barrido
    return estado.reshape(N, N), max_barridos

def centro_estimado(resultado, patrones):
    # Reconocimiento por coincidencia con los patrones memorizados.
    diferencias = [np.sum(resultado != p) for p in patrones]
    indice = int(np.argmin(diferencias))
    if diferencias[indice] != 0:
        return None, diferencias
    return POSICIONES[indice], diferencias

def ejecutar():
    patrones = [aro(*pos) for pos in POSICIONES]
    # Se simula ruido: cambiar cinco pixeles del aro ubicado en (6,3).
    original = patrones[1]
    alterada = original.copy().ravel()
    indices = [9, 17, 27, 64, 88]
    alterada[indices] *= -1
    alterada = alterada.reshape(N, N)
    print('PATRONES ENTRENADOS (X=negro, espacio=blanco)')
    for pos, p in zip(POSICIONES, patrones):
        print(f'\nAro con centro {pos}:\n{dibujar(p)}')
    print('\nIMAGEN CON RUIDO (centro esperado: (6,3)):\n' + dibujar(alterada))
    for metodo in ('hebb', 'pseudoinversa'):
        W = entrenar(patrones, metodo)
        salida, barridos = recuperar(alterada, W)
        centro, diferencias = centro_estimado(salida, patrones)
        print(f'\nMETODO {metodo.upper()} - barridos: {barridos}, centro reconocido: {centro}')
        print(f'Diferencias respecto a patrones: {diferencias}')
        print(dibujar(salida))

if __name__ == '__main__':
    ejecutar()
