import numpy as np 

def egauss(A,b):
    n =  A.shape[0]
    U = A.copy()
    y = b.copy()
    idx = 0
    for k in range(n-1):
        if U[k,k] == 0.0:
            idx = k+1
            print("La matriz tiene un cero en la diagonal!")
            print(f'posicion {idx}')
            U = []
            y = []
            return U, y
        break
    if idx == 0:
        for k in range(n-1):
            v = U[k+1:,k]/U[k,k]
            U[k+1: , k:] = U[k+1: , k:]-np.outer(v, U[k, k:])
            y[k+1:] = y[k+1:] + v*y[k]
        return U, y   

# TEST
A = np.random.rand(4,4)
b = np.random.rand(4)
U, y = egauss(A,b)

