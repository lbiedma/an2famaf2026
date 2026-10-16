import numpy as np 


def cociente_rayleigh(A,q0, tol = 1e-10, m =500):
    q = q0.copy()/np.linalg.norm(q0,2)
    lamb_ = 0
 
    for i in range(m):
        z = A@q
        lamb = q.T@z
        q = z/np.linalg.norm(z)

        err = np.abs(lamb_ - lamb)
        if err < tol:
            break
        lamb_ = lamb

    return q, lamb

A = np.random.random((4,4))
q0 = np.random.random(4)

q, lamb = cociente_rayleigh(A, q0)

aut_vals = np.linalg.eigvals(A)

print(lamb)
print(aut_vals)




