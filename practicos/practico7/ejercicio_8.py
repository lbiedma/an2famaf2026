import numpy as np 

def sol_grandcon(A, b, x, err, M):
    r = b - A @ x 
    sigma = np.linalg.norm(r, 2)
    d = r
    for k in range(M):
        if sigma <= err:
            print("Llegamos a la solucion", k)
            break
        v = A @ d
        t = sigma**2 / (d.T @ v)
        x = x + t * d 
        r = r - t * v 
        sigma_mas = np.linalg.norm(r, 2)
        s = sigma_mas**2 / (sigma**2)
        d = r + s * d 
        sigma = sigma_mas
    
    return x 

# TEST 

# A = np.random.random((5,5))
# A = np.eye(5)+A
# A = 0.5 * (A+A.T) 
# b = np.random.random(5)
# x_0 = np.zeros(5)
# x_sol = sol_grandcon(A, b, x_0, 1e-20, 500) 
# print(A@x_sol-b)
    
