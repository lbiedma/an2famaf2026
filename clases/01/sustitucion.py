import numpy as np
import time

def sustitucion_adelante(A, b):
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        x[i] = b[i]
        for j in range(i):
            x[i] -= A[i, j] * x[j]
        x[i] /= A[i, i]
    return x

def sustitucion_adelante_filas(A, b):
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        x[i] = (b[i] - A[i, :i] @ x[:i]) / A[i, i]
    return x

### TEST CON MATRICES MUY GRANDES Y COMPARAR PERFORMANCE
N = 1000

# Creación de matriz A triangular inferior
A_large = np.tril(np.random.rand(N, N))

# Creación de vector b
b_large = np.random.rand(N)

print(f"Resolviendo sistema de tamaño {N}x{N}...")

# Medición de tiempo para el enfoque basado en bucle
start_col = time.time()
x_loop = sustitucion_adelante(A_large, b_large)
end_col = time.time()
time_loop = end_col - start_col

# Medición de tiempo para el enfoque basado en filas
start_row = time.time()
x_row = sustitucion_adelante_filas(A_large, b_large)
end_row = time.time()
time_row = end_row - start_row

# Verificación de que los resultados son iguales (dentro de la tolerancia de punto flotante)
matches = np.allclose(x_loop, x_row)

print(f"Los resultados coinciden: {matches}")
print(f"Tiempo (loop): {time_loop:.4f} segundos")
print(f"Tiempo (filas): {time_row:.4f} segundos")

if matches and time_row < time_loop:
    print("El enfoque basado en filas es más rápido.")
elif matches:
    print("El enfoque basado en columnas es más rápido.")
else:
    print("Los resultados no coinciden.")
