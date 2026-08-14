import numpy as np

# ITEM a)

diag_0 = np.array([2, 2, 2])
diag_1 = -np.array([1, 1])

# Usamos np.diag(v,k) de numpy que se lo puede usar para tomar la diagonal de una matriz
# o armar una matriz diagonal a partir de un array. La segunda entrada k es indica 
# la diagonal que se quiere tomar, por ejemplo si k= 0 es la diagonal principal por defecto
# si k >0 o k<0 son las subdiagonales    

A = np.diag(diag_1, -1)+ np.diag(diag_0) +np.diag(diag_1,1)

B = np.diag(diag_1, -1)+ 2*np.diag(diag_0) +np.diag(diag_1,1)

print(f'A = {A}')
print(f'B = {B}')

I = np.eye(3)
Z = np.zeros((3,3)) 

C = np.block([[A, -I, Z],
              [-I, B, -I],
              [Z, -I, A]])

print(f'C = {C}')

# ITEM b)

# X_1 se define de la siguiene forma:
X_1 = np.block([[I, Z],
                [Z, I],
                [Z, Z]])

print(X_1.T@C@X_1) 

# X_2 se define de la siguiene forma:
X_2 = np.block([[Z], 
                [I], 
                [Z]])

print(X_2.T@C@X_2) 

# X_3 se define de la siguiene forma:
X_3 = np.block([[Z, Z], 
                [I, Z],
                [Z, I]])

print(X_3.T@C@X_3) 

# ITEM c)

print(np.allclose(C[:6, :6], X_1.T@C@X_1))

print(np.allclose(C[3:6, 3:6], X_2.T@C@X_2))

print(np.allclose(C[3:9, 3:9], X_3.T@C@X_3))