import numpy as np 

A = np.array([[1, 0, 4, 2],
              [2, -7, 1, 0],
              [0, 0, -3, 1],
              [-4, 1, 0, 2]])

B = np.array([[1, 2, 0, -1],
              [2, 0, -3, 0],
              [-1, 2, 0, -1],
              [1, 0, 1, 5]])

A00 = A[:2, :3]
A01 = A[:2, 3:4]
A10 = A[2:4, 0:3]
A11 = A[2:4, 3:4]

B00 = B[:3, :2]
B01 = B[:3, 2:4]
B10 = B[3, :2]
B11 = B[3, 2:4]

# Muestre que AB = C
# Ai0 @ B0j + Ai1 @ B1j = Cij 

# i = 0, j = 0
C_00 = A00@B00 + np.outer(A01,B10) 
# i = 1, j = 0
C_10 = A10@B00 + np.outer(A11,B10) 
# i = 0, j = 1
C_01 = A00@B01 + np.outer(A01,B11) 
# i = 1, j = 1
C_11 = A10@B01 + np.outer(A11,B11) 

C = np.block([[C_00, C_01], [C_10, C_11]])

print(C)

# A[i, :] Recorre la fila i y toda la columna j
# A[i:j, :] Recorre la fila i hasta el indice j-1 y toda la columna j
# A[:i, :] Recorre desde la fila 0 hasta la fila i-1 y toda la columna j

# A[:, j] Recorre toda la fila i y solo toma la columna j
# A[:, j:i] Recorre toda la fila i y la columna j hasta el indice i-1 
# A[:, :j] Recorre toda la fila i  y recorre desde la columna 0 hasta el indice j-1
