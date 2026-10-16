import numpy as np 

import sys
sys.path.append('..')
from practico4.ejercicio_3 import rot_givens
from ejercicio_9 import fhess

def autqr_hess(A, m):
    
    H, Q = fhess(A)
    n = H.shape[0]
    for k in range(m):
        for j in range(n-1):
            c,s = rot_givens(H[j,j],H[j+1,j])
            G = np.array([[c, -s],
                          [s, c]])
            H[[j ,j+1], j:] = G@H[[j ,j+1], j:] 

            


