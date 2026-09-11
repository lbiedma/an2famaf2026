import numpy as np

def rot_givens(x_1, x_2):


    if np.abs(x_1)+np.abs(x_2) == 0:
        c = 1
        s = 0
    elif np.abs(x_2) > np.abs(x_1):
        t = -x_1/x_2
        s = -np.sign(x_2)/np.sqrt(1+t**2)
        c = t*s
    else:
        t = -x_2/x_1
        c = np.sign(x_1)/np.sqrt(1+t**2)
        s = t*c

    return c, s

def qrgivens(A):
    m,n = A.shape
    R = A.copy()
    Q = np.eye(m)
    p = min(m-1, n)

    for j in range(p):
        for i in range(j+1, m):
            if R[i,j] != 0:
                c, s = rot_givens(R[j,j],R[i,j])
                G = np.array([[c, -s],
                             [s,   c]])
                R[[j,i],j:] = G@R[[j,i],j:]
                Q[:,[j,i]] = Q[:,[j,i]]@G.T
    if m <= n and R[m-1, m-1] == 0:
        R[m-1, m-1:] = -R[m-1, m-1:]
        Q[:, m-1] = -Q[:, m-1]

    return Q, R 

A = np.random.rand(4,5)

Q, R = qrgivens(A)

#print(Q.T@Q)

#print(R)

#print(np.linalg.norm(A-Q@R,2)) 

def house(x):
    m = len(x)
    u = x.copy()
    sigma = np.sum(x[1:]**2)

    if sigma == 0: 
        u = np.zeros(m)
        rho = 0
    else:
        mu = np.sqrt(sigma + x[0]**2)

        if x[0]<=0:
            gamma = x[0]-mu
        else: 
            gamma = -sigma/(x[0]+mu)

        rho = 2*gamma**2/(sigma+gamma**2)
        u[0] = 1
        u[1:] = u[1:]/gamma

    return rho, u

def qrhholder(A):
    m,n = A.shape
    R = A.copy()
    Q = np.eye(m)
    p = min(m,n)
    for j in range(p):
        rho, u = house(R[j:, j])
        w = rho*u
        v = u.T@R[j:,j:]
        v1 = Q[:, j:]@w
        R[j:,j:] = R[j:,j:] - np.outer(w, v)
        Q[:, j:] = Q[:, j:] - np.outer(v1, u)

    return  Q, R     

A = np.random.rand(5,8)

Q, R = qrhholder(A)

#print(Q.T@Q)

#print(R)

#print(np.linalg.norm(A-Q@R,2)) 
    


