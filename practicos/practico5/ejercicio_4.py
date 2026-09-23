import numpy as np 

def cuad_min_svd(A,b):
    m, n = A.shape

    y = np.zeros(n)
    U, S, Vt = np.linalg.svd(A)

    tol = 1e-10
    c = U.T@b
    r = min(m,n)

    elem_corte = np.where(S <tol)[0] # Uso np.where para encontrar los indices de aquellos valores iguales de cero
    if len(elem_corte)> 0: # si existe al menos un cero obtengo su indice  
        r = elem_corte[0] # se toma el primer indice donde empieza los ceros

    S_inv = np.zeros((r,r))

    for i in range(r):
        S_inv[i,i] = 1/S[i]

    y[:r] = S_inv@c[:r] 
    x_sol = Vt.T@y

    residuo = np.linalg.norm(c[r+1:], 2)

    return x_sol, residuo

A = np.loadtxt("/home/ganyc/Desktop/an2famaf2026/practicos/practico5/A_p5e4.txt")
b = np.loadtxt("/home/ganyc/Desktop/an2famaf2026/practicos/practico5/b_p5e4.txt")

sol, residuo = cuad_min_svd(A,b)

# U, S, V = np.linalg.svd(A)

print(residuo)
