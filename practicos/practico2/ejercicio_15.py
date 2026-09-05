
import numpy as np 

import matplotlib.pyplot as plt

import sys
sys.path.append('..')
from ejercicio_11 import sol_egauss

# Obtener el circulo máximo no era tan facil,
# ya que existen infinitos ciruculos maximos y hace falta 
# coordenada mas para achicar las posibilidades de generar un circulo max 
# Para quesea mas facil podemos usar un polo de la esfera,
# que se lo calcula una vez conocido la solución
# Ya con este dato podemos generar un único circulo max


def circulo_max(centro, radio, polo, punto_es):
    # vector del centro al polo 
    vec_polo_c = polo - centro
    # vector del centro al polo
    vec_punto_c = punto_es - centro
    
    # Necesitamos la base ortonormal del plano formado por centro, el polo y el punto
    vec_norm = vec_polo_c / np.linalg.norm(vec_polo_c)
    vec_ort = vec_punto_c - np.dot(vec_punto_c, vec_norm) * vec_norm
    # Si el punto aleatorio cae justo en los polos vec_ort puede ser muy pequeño,
    # por lo que se elige un eje auxiliar
    if np.linalg.norm(vec_ort) < 1e-6:
        # producto vectorial 
        vec_ort = np.cross(vec_norm, [1, 0, 0])

    vec_ = vec_ort / np.linalg.norm(vec_ort)
    
    # Parametrización del círculo completo
    theta = np.linspace(0, 2 * np.pi, 100)

    cx = centro[0] + radio * (vec_norm[0] * np.cos(theta) + vec_[0] * np.sin(theta))
    cy = centro[1] + radio * (vec_norm[1] * np.cos(theta) + vec_[1] * np.sin(theta))
    cz = centro[2] + radio * (vec_norm[2] * np.cos(theta) + vec_[2] * np.sin(theta))

    return cx, cy, cz


def graficar_esfera(t, u, v, w):

    A = np.array([[t[0], t[1], t[2], 1], 
                  [u[0], u[1], u[2], 1],
                  [v[0], v[1], v[2], 1], 
                  [w[0], w[1], w[2], 1]]).astype("float")

    # Validar que no sean coplanares
    if np.abs(np.linalg.det(A)) < 1e-10:
        print("Los puntos son coplanares. Generar nuevos puntos.")
        return   

    b = -np.array([t[0]**2+ t[1]**2+ t[2]**2,
                   u[0]**2+ u[1]**2+ u[2]**2,
                   v[0]**2+ v[1]**2+ v[2]**2,
                   w[0]**2+ w[1]**2+ w[2]**2]).astype("float")
    sol_esfera = sol_egauss(A, b)
    D, E, F, G = sol_esfera[0], sol_esfera[1], sol_esfera[2], sol_esfera[3]

    centro_es = -np.array([D, E, F])/2.0
    r = np.sqrt(np.sum(centro_es**2) -G)

    # Podemos usar el Polo Norte como referencia
    polo_norte = centro_es + np.array([0, 0, r])

    # Generamos una malla para graficar 
    x = np.linspace(0, 2*np.pi, 100)
    y = np.linspace(0, np.pi, 100)        
    x_es = r * np.outer(np.cos(x), np.sin(y))- D/2  
    y_es = r *  np.outer(np.sin(x), np.sin(y))- E/2
    z_es = r *  np.outer(np.ones(np.size(100)), np.cos(y))- F/2


   # Generamos un Figure en 3d  
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Esfera
    ax.plot_surface(x_es, y_es, z_es, color='cyan', alpha=0.2, edgecolor='k', linewidth=0.1)

    # Graficar el Polo Norte
    ax.scatter(polo_norte[0], polo_norte[1], polo_norte[2], color='black', s=100, marker='^')

    # Graficar los 4 puntos dados y los circulos max
    puntos_es = np.array([t, u, v, w])
    colores = ['red', 'green', 'blue', 'orange']

    for i in range(4):
        # Graficar el punto
        ax.scatter(puntos_es[i, 0], puntos_es[i,1], puntos_es[i, 2], color=colores[i], s=70)
        
        # Graficamos su único círculo máximo pasando por el polo
        cx, cy, cz = circulo_max(centro_es, r, polo_norte, puntos_es[i,:])
        ax.plot(cx, cy, cz, color=colores[i], linewidth=1.8)

    ax.set_box_aspect([1, 1, 1])
    plt.tight_layout()
    plt.show()

t = np.random.rand(3)    
u =  np.random.rand(3)
v =  np.random.rand(3)
w = np.random.rand(3)

graficar_esfera(t,u,v,w)


