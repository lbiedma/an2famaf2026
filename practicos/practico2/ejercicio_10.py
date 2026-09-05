import numpy as np 

def egaussp(A, b):
    m, n = A.shape
    U = A.copy()
    y = b.copy()

    for k in range(min(m - 1, n)):
        # si la columna son ceros no hace aplicar gauss
        if np.max(np.abs(U[k:, k])) != 0:
            # Elegimos el pivot
            l = k + np.argmax(np.abs(U[k:, k]))
            # Pivoteamos (sin multiplicar por matriz elemental)
            U[[k, l], :] = U[[l, k], :]
            y[[k, l]] = y[[l, k]]
            # Aplicamos las tranformaciones de gauss
            v = U[k + 1:, k] / U[k, k]
            U[k + 1:, k] = 0
            U[k + 1:, k + 1:] = U[k + 1:, k + 1:] - np.outer(v, U[k, k + 1:])
            y[k + 1:] = y[k + 1:] - v * y[k]

    return U, y

#TEST 
A= np.random.rand(5,5)
b = np.random.rand(5)
U, y = egaussp(A,b)

print(f'U= {U}')
print(f'y= {y}')

import numpy as np 

def dlup(A):
    n = A.shape[0]
    U = A.copy()
    P = np.eye(n)
    for k in range(n): 
        pivot = k + np.argmax(np.abs(U[k:, k]))
        if pivot != k:
            U[[k, pivot], :] = U[[pivot, k], :]
            P[[k, pivot], :] = P[[pivot, k], :]
        
        U[k+1: , k] = U[k+1:, k]/U[k, k] 
        U[k+1: , k +1:] = U[k+1: , k+1:]-np.outer(U[k+1: , k], U[k, k+1:])
        
    L = np.tril(U,-1)+np.eye(n)
    U = np.triu(U)
           
    return U, L, P 

# #TEST 
A= np.random.rand(5,5)
U, L, P = dlup(A)
print(f'U={U}')
print(f'A={L}')
print(f'P={P}')
print(P.T@L@U-A)

            