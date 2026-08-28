import numpy as np 

def egauss(A,b):
    n =  A.shape[0]
    U = A.copy()
    y = b.copy()

    for k in range(n-1):
        v = U[k+1:,k]/U[k,k]
        U[k+1: , k:] = U[k+1: , k:]-np.outer(v, U[k, k:])
        y[k+1:] = y[k+1:] + v*y[k]

    return U, y   

