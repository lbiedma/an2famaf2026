import numpy as np 

def arnoldi(A, v, m):
    n = A.shape[0]
    if m < n:
        H  = np.zeros((m+1,m))
        V = np.zeros((n,m))
        norm_v = np.linalg.norm(v, 2)
        
        if norm_v == 0:
            return H, V
        for j in range(m):
            V[:, j] = v / norm_v
            v = A @ V[:, j]
            for i in range(j+1):
                H[i,j] = np.inner(v, V[:, i])
                v = v - H[i, j] * V[: , i]
                norm_v = np.linalg.norm(v, 2)
            if norm_v == 0: 
                break
            
            H[j+1, j] = norm_v
        
        return H, V

    else:
        print("No se cumple la condición m<n")
        return None

#TEST
n = 5
m = 4
A = np.random.random((n,n))
A = A.T@A
A = np.eye(n)+A 
v = np.random.random(n)

# H_sol, V_sol = arnoldi(A, v, m) 

# print(np.linalg.norm(H_sol[:m,:]-V_sol.T@A@V_sol,2))

# print(V_sol.T@V_sol)

                
                 
            
         
    