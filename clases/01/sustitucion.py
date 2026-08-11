import numpy as np
import time

def sustitucion_adelante_filas(A, b):
    # Enfoque por filas (escalar)
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        x[i] = b[i]
        for j in range(i):
            x[i] -= A[i, j] * x[j]
        x[i] /= A[i, i]
    return x

def sustitucion_adelante_filas_vec(A, b):
    # Enfoque por filas (vectorizado)
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        x[i] = (b[i] - A[i, :i] @ x[:i]) / A[i, i]
    return x

def sustitucion_adelante_columnas(A, b):
    # Enfoque por columnas (escalar)
    n = len(b)
    x = np.array(b, dtype=float)
    for j in range(n):
        x[j] /= A[j, j]
        for i in range(j + 1, n):
            x[i] -= A[i, j] * x[j]
    return x

def sustitucion_adelante_columnas_vec(A, b):
    # Enfoque por columnas (vectorizado)
    n = len(b)
    x = np.array(b, dtype=float)
    for j in range(n):
        x[j] /= A[j, j]
        x[j+1:] -= A[j+1:, j] * x[j]
    return x

### TEST CON MATRICES GRANDES Y COMPARAR PERFORMANCE
N = 5000

# Creación de matriz A triangular inferior
A_large = np.tril(np.random.rand(N, N))
# Evitar que la diagonal sea cero
np.fill_diagonal(A_large, A_large.diagonal() + 0.5)

# Creación de vector b
b_large = np.random.rand(N)

print(f"Resolviendo sistema de tamaño {N}x{N}...")

# 1. Filas (Escalar)
start = time.time()
x_row_esc = sustitucion_adelante_filas(A_large, b_large)
t_row_esc = time.time() - start

# 2. Filas (Vectorizado)
start = time.time()
x_row_vec = sustitucion_adelante_filas_vec(A_large, b_large)
t_row_vec = time.time() - start

# 3. Columnas (Escalar)
start = time.time()
x_col_esc = sustitucion_adelante_columnas(A_large, b_large)
t_col_esc = time.time() - start

# 4. Columnas (Vectorizado)
start = time.time()
x_col_vec = sustitucion_adelante_columnas_vec(A_large, b_large)
t_col_vec = time.time() - start

# Verificación de correctitud
ok_row_vec = np.allclose(x_row_esc, x_row_vec)
ok_col_esc = np.allclose(x_row_esc, x_col_esc)
ok_col_vec = np.allclose(x_row_esc, x_col_vec)

print(f"Resultados coinciden:")
print(f"  - Filas Vec vs Escalar: {ok_row_vec}")
print(f"  - Columnas Esc vs Filas Esc: {ok_col_esc}")
print(f"  - Columnas Vec vs Filas Esc: {ok_col_vec}")

print("\nTiempos de ejecución:")
print(f"  - Filas (Escalar):      {t_row_esc:.4f} segundos")
print(f"  - Filas (Vectorizado):  {t_row_vec:.4f} segundos")
print(f"  - Columnas (Escalar):   {t_col_esc:.4f} segundos")
print(f"  - Columnas (Vectorizado): {t_col_vec:.4f} segundos")
