import numpy as np

def lu_no_pivot(A):
    n = A.shape[0]
    L = np.eye(n)
    U = A.copy().astype(float)
    for k in range(n-1):
        for i in range(k+1, n):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            U[i, k:] -= factor * U[k, k:]
    return L, U

def solve_lu(L, U, b):
    # Sustitución hacia adelante Ly = b
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    # Sustitución hacia atrás Ux = y
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x

# Testeamos para valores de epsilon cada vez menores
epsilons = [1e-8, 1e-15, 1e-16, 1e-17]
for eps in epsilons:
    # El sistema lineal es:
    # eps * x_1  +  x_2 = 1 + eps
    # x_1        +  x_2 = 2
    # La solución exacta es x_1 = 1, x_2 = 1.

    A = np.array([
        [eps, 1.0],
        [1.0, 1.0],
    ])
    b = np.array([1.0 + eps, 2.0])
    
    L, U = lu_no_pivot(A)
    x_computed = solve_lu(L, U, b)
    x_exact = np.array([1.0, 1.0])
    
    print(f"Epsilon = {eps}")
    print(f"  L:\n{L}")
    print(f"  U:\n{U}")
    print(f"  Solución Calculada: {x_computed}")
    print(f"  Error Absoluto:     {np.linalg.norm(x_computed - x_exact)}")
    print("-" * 50)
