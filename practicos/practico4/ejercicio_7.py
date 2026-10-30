import numpy as np

import sys
sys.path.append('..')

from practico1.ejercicio_1b import sol_trisup_col

from practico4.ejercicio_4 import qrgivensp

def sol_cuadmin(A, b):
    m, n = A.shape
    Q, R, P = qrgivensp(A)
    
    y = np.zeros(n)
    q = Q.T @ b
    r_i = np.diag(R)
    p = min(m, n)
    ceros = np.where(r_i == 0)[0]
    if len(ceros) != 0:
        p = ceros[0]

    y[:p] = sol_trisup_col(R[:p, :p], q[:p])

    x = P @ y

    residuo = np.linalg.norm(q[p:])

    return x, residuo
