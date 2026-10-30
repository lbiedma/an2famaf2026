import numpy as np

import sys
sys.path.append("..")
from practico2.ejercicio_12 import inv_lu

"Jacobi"

def sol_jacobi(A, b, x0, eps =1e-10, m =200):

    n = A.shape[0]
    diag_A = np.diag(A)
  
    if diag_A.any() == 0:
            print('Hay al menos un cero en A')    
            raise Exception

    x = x0.copy()
    x_mas = x0.copy()

    L = np.tril(A,-1)
    U = np.triu(A, 1)
    D = np.diag(np.diag(A))

    D_inv = D.copy()
    for i in range(n):
        D_inv[i,i] = 1/D[i,i]

    b_ = D_inv@b
    A_ = D_inv@(L+U)

    for k in range(m):
        x_mas = b_ -A_ @x
        sigma = np.linalg.norm(x_mas-x, np.inf)
        if sigma< eps:
            break
        x = x_mas

    return x_mas
        
A  = np.array([[10., 1],
                [4, 6]])

b = np.array([3., 9])

x0 = np.array([1.,1])

print("----- Teste Jacobi ------")

x_sol = sol_jacobi(A,b, x0)

print(f'x_sol ={x_sol}')
    
A  = np.random.random((4,4)) + 4*np.eye(4)
b = np.random.random(4)
x0 = np.random.random(4)

print("----- Test Jacobi con matriz random ------")

x_sol = sol_jacobi(A,b, x0)

b_ = A@x_sol

print(f'x_sol_jacobi ={x_sol}')
print(np.linalg.norm(b_-b,2))

"Gauss Seidel"

def sol_gseidel(A, b, x0, eps =1e-10, m =200):

    n = A.shape[0]
    diag_A = np.diag(A)
  
    if diag_A.any() == 0:
            print('Hay al menos un cero en A')    
            raise Exception

    x = x0.copy()
    x_mas = x0.copy()

    L = np.tril(A, -1)
    D = np.diag(np.diag(A))
    U = np.triu(A, 1)

    D_inv = D.copy()
    for i in range(n):
        D_inv[i,i] = 1/D[i,i]

    b_ = D_inv@b
    A_ = D_inv@(L+U)

    # b_ = b.copy().astype(float)
    # D_inv = np.diag(1/diag_A)
    # b_ = D_inv@b
    # A_ = A.copy().astype(float)
    # np.fill_diagonal(A_, 0.0)
    # A_ = D_inv@A_

    for k in range(m):
        for i in range(n):
            x_mas[i] = b_[i] -A_[i,:] @x_mas
        sigma = np.linalg.norm(x_mas-x, np.inf)
        if sigma< eps:
            print(f'sigma = {sigma}')
            break
        x = x_mas.copy()

    return x_mas    

print("----- Test GS con matriz random ------")

x_sol = sol_gseidel(A,b, x0)

print(f'x_sol_gs ={x_sol}')
b_ = A@x_sol
print(np.linalg.norm(b_-b,2))