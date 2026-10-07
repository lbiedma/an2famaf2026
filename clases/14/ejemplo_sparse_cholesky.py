import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

# 1. Definir dimensión del sistema
n = 100
total_elementos = n * n

# 2. Construir la matriz "Punta de Flecha" (Arrowhead)
# Solo tiene entradas no nulas en la fila 0, columna 0 y diagonal principal
diag = 4.0 * np.ones(n)
A_dense = np.diag(diag)
A_dense[0, :] = 1.0
A_dense[:, 0] = 1.0

# Aseguramos que sea Simétrica Definida Positiva (SPD)
A_dense[0, 0] = 2.0 * n

# 3. Factorización de Cholesky A = L @ L.T
L_dense = la.cholesky(A_dense, lower=True)

# 4. Cuantificar la pérdida de dispersión
nnz_A = np.count_nonzero(A_dense)
nnz_L = np.count_nonzero(L_dense)

print(f"Dimensión del sistema: {n}x{n} ({total_elementos} entradas)")
print(f"Elementos no nulos en A (original) : {nnz_A} ({100 * (1 - nnz_A/total_elementos):.2f}% de ceros)")
print(f"Elementos no nulos en L (factor)   : {nnz_L} ({100 * nnz_L / (n*(n+1)/2):.2f}% de densidad en L)")

# 5. Graficar los patrones de dispersión (Spy Plot)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

axes[0].spy(A_dense, markersize=2, color='navy')
axes[0].set_title(f"Matriz Rala Original A\n(nnz = {nnz_A})")

axes[1].spy(L_dense, markersize=2, color='crimson')
axes[1].set_title(f"Factor de Cholesky L\n(nnz = {nnz_L} -> ¡100% Denso!)")

plt.tight_layout()
plt.show()
