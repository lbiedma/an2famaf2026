import numpy as np 

import matplotlib.pyplot as plt 

# item a)

def matriz_epsilon(input):
    det_A = []
    cond_A = []
    matriz_A = "A"
    matriz_B = "B"
    # generamos 100 matrices para cada epsilon
    for i in range(100):
        eps = 2**(-i) 
        if input == matriz_A:
            M = np.array([[1., 1-eps], 
                            [0,     1]]) # Matriz A
        if input==matriz_B:
            M = np.array([[1 / eps, 0], # Matriz B 
                          [0,   eps]])

        det = M[0, 0] * M[1,1] - M[1, 0] * M[0, 1]
        cond = np.linalg.cond(M, 2)
        det_A.append(det)
        cond_A.append(cond)
    
    plt.plot(det_A)
    plt.plot(cond_A)
    plt.legend([f"determiantes de {input} (eps)", f"numero de condicion de {input} (eps)"])
    plt.show()

matriz_epsilon("B")

#item b

def matrices_esferas(eps):
    A = np.array([[1., 1-eps], 
                  [0, 1]])
    B = np.array([[1 / eps, 0], 
                  [0, eps]])

    r =  np.linspace(0, 2*np.pi, 100)
    x = np.cos(r)
    y = np.sin(r)
    xy = np.block([[x],
                   [y]])
    A_es = A @ xy
    B_es = B @ xy
    
    plt.plot(x, y, label = "bola unidad")
    plt.plot(A_es[0, :], A_es[1, :], label = "tranformacion de A")
    plt.plot(B_es[0, :], B_es[1, :], label = "tranformacion de B")
    plt.axis("equal")
    plt.legend()
    plt.show()


print(matrices_esferas(0.25))

print(matrices_esferas(0.125))

print(matrices_esferas(0.0625))

print(matrices_esferas(1e-5))
    