
import numpy as np 

def diag_jacobi(A):
    c = 1
    s = 0
    if A[0, 1] == 0:
        return c,s
    else:
        tau = (A[1,1]-A[0,0])/(2*A[0,1])
        if tau < 0:
            t = 1/(-tau+np.sqrt(tau**2+1))
        else:
            t = -1/(tau+np.sqrt(tau**2+1))
        c = 1/np.sqrt(1+t**2)
        s = t*c
        return c, s 

def off(A):
    n = A.shape[0]
    A_off = A.copy()

    for i in range(n):
        A_off[i,i] = 0
    norm_off = np.linalg.norm(A_off, 'fro') 

    return norm_off

def autjacobi(A, eps= 1e-10, m = 500):
    n = A.shape[0]
    A_aut = A.copy()
    Q = np.eye(n)
    for i in range(m):
        if off(A_aut)< eps:
            break
        else: 
            A_aux = A_aut - np.diag(np.diag(A_aut))
            [i, j] = np.unravel_index(np.argmax(np.abs(A_aux), axis= None), A_aut.shape)

            D = np.array([[A_aut[i,i], A_aut[i,j]],
                          [A_aut[j,i], A_aut[j,j]] ])
            c, s = diag_jacobi(D)

            jac = np.array([[c, -s],
                            [s, c]])
            A_aut[[i,j], :] = jac.T@A_aut[[i,j], :]
            A_aut[:, [i,j]] = A_aut[:,[i,j]]@jac
            Q[:, [i,j]] = Q[:, [i,j]]@jac

    B = A_aut
    return B, Q

A = np.random.rand(4,4)

A = 0.5*(A.T+A)

B, Q = autjacobi(A)

autovalores = np.linalg.eigvals(A)

print(np.diag(B))
print(autovalores)
                         




     



