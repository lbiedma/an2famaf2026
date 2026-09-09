import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')

#importamos las funciones que necesitamos
from practico2.ejercicio_11 import sol_egauss

# Leemos los datos usando loadtxt 
A = np.loadtxt("A_dataset.txt")
b = np.loadtxt("b_dataset.txt")

def matriz_per(A,b):

    n = A.shape[0]

    x_exact = sol_egauss(A,b)

    E = np.random.randn(n)

    delta_x = []
    delta_A = []

    for beta in range(1, 11):

        epsilon = 10**(-beta)

        A_tilde = A + epsilon*E

        x_tilde = sol_egauss(A_tilde, b)

        err_x = np.linalg.norm(x_tilde - x_exact, 2) / np.linalg.norm( x_exact, 2)

        err_A = np.linalg.norm(A_tilde - A, 2) / np.linalg.norm(A, 2)

        delta_x.append(err_x)
        delta_A.append(err_A)

        plt.loglog(delta_A, delta_x, 'o-', color='r')

    plt.xlabel("delta A")
    plt.ylabel("delta x")
    plt.title('Sensibilidad de la solución frente a perturbaciones en A')
    plt.show()

#matriz_per(A,b)
# La matriz de datos no es mal condicionada por lo que esta bien que la gráfica sea lineal
# voy a dejar un ejemplo de una matriz mal condicionada 

n = len(b)

A_mal_cond = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        A_mal_cond[i, j] = 1 / (i + j + 1)

matriz_per(A_mal_cond, b)