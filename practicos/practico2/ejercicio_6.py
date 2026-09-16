import numpy as np 

def dlu(A):
    n = A.shape[0]
    U = A.copy()
    for k in range(n):         
        U[k+1: , k] = U[k+1:, k]/U[k, k] 
        U[k+1: , k +1:] = U[k+1: , k+1:]-np.outer(U[k+1: , k], U[k, k+1:])
        
    L = np.tril(U,-1)+np.eye(n)
    U = np.triu(U)
           
    return U, L

# TEST
A = np.random.rand(4,4)
b = np.random.rand(4)
U, L = dlu(A)


