import numpy as np

import sys
sys.path.append('..')

from practico4.ejercicio_3 import rot_givens

def qrgivensp(A):
    m, n = A.shape
    Q = np.eye(m)
    P = np.eye(n)
    R = A.copy()
    # Forma rápida de calcular la norma de todas las columnas de A
    c_norm = np.linalg.norm(A, axis=0) ** 2
    p = min(m - 1, n)

    for j in range(p):
        # Pivoteo por derecha, cambiando columnas en vez de filas
        l = j + np.argmax(c_norm[j:])
        if l != j:
            R[:, [l, j]] = R[:, [j, l]]
            P[:, [l, j]] = P[:, [j, l]]
            c_norm[[l, j]] = c_norm[[j, l]]
        # Givens común y corriente
        for i in range(j+1, m):
            if R[i, j] != 0:
                #I = [j, i], J = j:
                c, s = rot_givens(R[j, j], R[i, j])
                G = np.array([[c, -s], [s, c]])

                R[[j, i], j:] = G @ R[[j, i], j:]
                Q[:, [j, i]] = Q[:, [j, i]] @ G.T
        # Actualización de c_norm SOLO UNA VEZ DESPUES DE ACTUALIZAR FILAS
        c_norm[j:] = c_norm[j:] - R[j, j:] * R[j, j:]

    if m <= n and R[m - 1, m - 1] < 0:
        # J = m:
        R[m - 1, m - 1:] = -R[m - 1, m - 1:]
        Q[:, m - 1] = -Q[:, m - 1]

    return Q, R, P