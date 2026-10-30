import numpy as np

import sys
sys.path.append('..')

from practico4.ejercicio_7 import sol_cuadmin

from ejercicio_11 import arnoldi


def sol_gmres(A, b, x_0, err, M, m_A):
    # Paso 0
    x_mas = x_0.copy()
    r = b - A @ x_mas
    sigma = np.linalg.norm(r)

    # Paso 1
    for k in range(M):
        if sigma <= err:
            break
        H, V = arnoldi(A, r, m_A)
        e_1 = np.zeros(H.shape[0])
        e_1[0] = 1.0
        alpha, sigma = sol_cuadmin(H, sigma * e_1)
        x_mas = x_mas + V @ alpha
        r = b - A @ x_mas

    # Paso 2
    return x_mas

# TEST 
n = 100
A = np.eye(n) + np.random.random((n,n))

b = np.random.random(n)

x_0 = np.random.random(n)

x_mas = sol_gmres(A, b, x_0, 1e-5, 100, 5)

print(np.linalg.norm(b-A@x_mas,2))