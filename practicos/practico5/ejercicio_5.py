import numpy as np

import matplotlib.pyplot as plt

def im_aprox_svd(A, tol):
    m,n = A.shape
    p = min(m,n)    
    U, S, Vt = np.linalg.svd(A)
    k = 0
    for i in range(p):
        if S[i] <= tol:
            k = i-1
            break
    A_k = np.zeros((m,n))

    for j in range(k):
        A_k = A_k + S[j]*np.outer(U[:,j], Vt[j,:])

    err = np.linalg.norm(A-A_k, 2)
    print(err)
    
    plt.imshow(A_k)
    plt.show()

A = np.loadtxt("/home/ganyc/Desktop/an2famaf2026/practicos/practico5/imagen3.txt")

tol = 500

im_aprox_svd(A, tol)
                    
            

    