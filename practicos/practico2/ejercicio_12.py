
import numpy as np

import sys
sys.path.append('..')
from practico1.ejercicio_1b import sol_trisup_col
from practico1.ejercicio_1b import sol_trinf_col

from ejercicio_10 import dlup 


def inv_lu(A):
    n = A.shape[0]
    I = np.eye(n)
    inv_A = np.zeros((n,n))
    U, L, P = dlup(A)
    for k in range(n):
        y = sol_trinf_col(L, P@I[k])
        x = sol_trisup_col(U, y)
        inv_A[:, k] = x 
    return inv_A

# TEST
A = np.array([[2., 10, 8, 8, 6], 
              [1, 4, -2, 4, -1],  
              [0, 2, 3, 2, 1], 
              [3, 8, 3, 10, 9], 
               [1, 4, 1, 2, 1]])

inv_A = inv_lu(A)
print(f'I={inv_A@A}')