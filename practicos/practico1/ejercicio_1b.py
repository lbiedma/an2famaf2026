import numpy as np

def sol_trinf_col(A,b):
    b_ = b.copy()
    n = len(b)
    x = np.zeros(n)

    for i, elem in enumerate(b):
        if elem!=0:
           k = i   
           break         

    for j in range(k,n):
        if A[j,j] == 0:
            print("existen ceros en la diagonal")
            break
        else:
            x[j] = b_[j]/A[j,j] 
            b_[j+1:] = b_[j+1:] - A[j+1:, j]*x[j]

    return x 

A = np.tril(np.random.rand(3,3))+0.5*np.eye(3)
b = np.random.rand(3)

x_sol = sol_trinf_col(A,b)

# print(b-A@x_sol)
# print(x_sol)

def sol_trisup_col(A,b):
    b_ = b.copy()
    n = len(b)
    x = np.zeros(n)

    for i in reversed(range(n)):
        if b[i]!=0:
           k = i   
           break         

    for j in range(k, -1, -1):
        if A[j,j] == 0:
            print("existen ceros en la diagonal")
            break
        else:
            x[j] = b_[j]/A[j,j] 
            b_[:j] = b_[:j] - A[:j, j]*x[j]

    return x 

A = np.triu(np.random.rand(3,3))+0.5*np.eye(3)
b = np.random.rand(3)

x_sol = sol_trisup_col(A,b)

print(b-A@x_sol)
print(x_sol)