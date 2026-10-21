import numpy as np 

import sys
sys.path.append('..')
from practico4.ejercicio_3 import rot_givens
from ejercicio_9 import fhess

def autqr_hess(A, m=500):
    
    H, Q = fhess(A, 'house')
    n = H.shape[0]
    rot_g = np.zeros((n-1,2))
    for k in range(m):
        for j in range(n-1):
            c,s = rot_givens(H[j,j],H[j+1,j])
            rot_g[j,:] = np.array([c,s])
            G = np.array([[c, -s],
                          [s, c]])
            H[[j ,j+1], j:] = G@H[[j ,j+1], j:] 
        for l in range(n-1):
            c, s = rot_g[l,:]
            G = np.array([[c, -s],
                          [s, c]])
            H[:, [l,l+1]] = H[:, [l,l+1]]@G.T
            Q[:, [l,l+1]] =  Q[:, [l,l+1]]@G.T

    return H, Q 

diag_0 = np.array([4, 4,4])
diag_1 = -np.array([1, 1])

B = np.diag(diag_1, -1)+ np.diag(diag_0) +np.diag(diag_1,1)

I = np.eye(3)
Z = np.zeros((3,3)) 

C = np.block([[B, -I, Z],
              [-I, B, -I],
              [Z, -I, B]])

print('--------------- Iteracion QR---------------------')

H, Q = autqr_hess(C)

err = H - Q.T@C@Q

print(np.linalg.norm(err, 2))

            


