import numpy as np 

import sys
sys.path.append('..')
from practico4.ejercicio_3 import house


def fhess(A, met):
    n = A.shape[0]
    H = A.copy()
    Q  = np.eye(n)

    if met == 'house':
        for j in range(n-2):
            rho, u = house(H[j+1:, j])
            w  = rho*u
            v = u.T@H[j+1: , j:]
            H[j+1: , j:] = H[j+1: , j:]-np.outer(w, v)
            H[: , j+1:] = H[: , j+1:]-H[: , j+1:]@np.outer(w,u)
            Q[: , j+1:] = Q[: , j+1:]-Q[: , j+1:]@np.outer(w,u)
    
    # Debo givens 
    return H, Q

A  = np.random.random((4,4))

H, Q = fhess(A, 'house')

print(H)

