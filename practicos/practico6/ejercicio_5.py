import numpy as np 

import sys
sys.path.append('..')
from practico2.ejercicio_10 import egaussp
from practico2.ejercicio_11 import sol_egauss

# Version norma infinito
def autpotencias_inf(A, q_0, err=1e-10, m=500):
    q_tilde = A @ q_0
    rho_tilde = np.inf
    for k in range(m):
        j = np.argmax(np.abs(q_tilde))
        q = q_tilde/q_tilde[j]
        q_tilde = A @ q
        rho = q_tilde[j]

        if np.abs(rho - rho_tilde) < err:
            print("iteraciones:", k)
            return q, rho

        rho_tilde = rho

    return q, rho

# TEST
A_0 = np.random.random((3,3))
q_0 = np.random.random(3)

q_inf, rho_inf = autpotencias_inf(A_0, q_0)

print(f"||A@q_inf - rho_inf*q_inf||_inf = {np.linalg.norm(A_0@q_inf - rho_inf*q_inf, np.inf)}")


# Version norma 2
def autpotencias_2 (A, q_0, err=1e-10, M=500):
    q_tilde = A @ q_0
    potencia = np.linalg.norm(q_0, 2)**2
    rho_tilde = (q_0.T@q_tilde)/potencia
    for k in range(M):
        q = q_tilde/np.linalg.norm(q_tilde, 2)
        q_tilde = A @ q
        rho = q.T@q_tilde
        if np.abs(rho - rho_tilde) < err:
            print("iteraciones:", k)
            break
        rho_tilde = rho
    return q, rho

#TEST
A_0 = np.random.random((3,3))
q_0 = np.random.random(3)

q_2, rho_2 = autpotencias_2(A_0, q_0)

print(f"||A@q_2 - rho_2*q_2||_2 = {np.linalg.norm(A_0@q_2 - rho_2*q_2, 2)}")

# Version cociente de Rayleigh

def autrayleigh(A, q_0, err=1e-10, M=600):
    n = A.shape[0]
    Id = np.eye(n)
    q = q_0 /np.linalg.norm(q_0)
    q_tilde = q.copy()
    rho = q.T@A@q
    for k in range(M):
        z = sol_egauss(A - rho*Id, q_tilde)
        sigma = np.linalg.norm(z)
        q = z/sigma
        theta = np.dot(q, q_tilde) / sigma
        if np.abs(theta)< err:
            print("iteraciones", k)
            return q, rho+theta

        q_tilde = q
        rho = rho+theta

    return q, rho+theta

#TEST
A_0 = np.random.random((3,3))
q_0 = np.random.random(3)

q_r, rho_r = autrayleigh(A_0, q_0)

print(f"||A@q_r - rho_r*q_r||_2 = {np.linalg.norm(A_0@q_r - rho_r*q_r, 2)}")
