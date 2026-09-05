import numpy as np 

import sys
sys.path.append('..')

from practico1.ejercicio_1b import sol_trisup_col
from ejercicio_10 import egaussp


def sol_egauss(A,b):
    U, y = egaussp(A,b)
    x = sol_trisup_col(U, y)

    return x

A = np.array([[2., 10, 8, 8, 6],
              [1, 4, -2, 4, -1],
              [0, 2, 3, 2, 1],
              [3, 8, 3, 10, 9],
              [1, 4, 1, 2, 1]])

b_1 = np.array([52., 14, 12, 51, 15])
b_2 = np.array([50., 4, 12, 48, 12])

sol_1 = sol_egauss(A,b_1)

sol_2 = sol_egauss(A,b_2)

print(f'sol_2 = {sol_2}')

print(f'sol_1 = {sol_1}')

