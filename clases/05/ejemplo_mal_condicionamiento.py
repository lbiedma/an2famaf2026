import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
    # -------------------------------------------------------------
    # 1. Definición de la matriz A y cálculo de propiedades
    # -------------------------------------------------------------
    A = np.array([[1000.0, 999.0], 
                  [999.0,  998.0]])
    
    # Inversa analítica y numérica
    A_inv = np.linalg.inv(A)
    det_A = np.linalg.det(A)
    
    # Normas y números de condición
    norm_inf_A = np.linalg.norm(A, np.inf)
    norm_inf_Ainv = np.linalg.norm(A_inv, np.inf)
    cond_inf = norm_inf_A * norm_inf_Ainv
    
    norm_2_A = np.linalg.norm(A, 2)
    norm_2_Ainv = np.linalg.norm(A_inv, 2)
    cond_2 = np.linalg.cond(A, 2)
    
    print("=" * 60)
    print("ANÁLISIS DE LA MATRIZ DE EJEMPLO")
    print("=" * 60)
    print(f"Matriz A:\n{A}\n")
    print(f"Determinante det(A) = {det_A:.4f} (¡Determinante -1 pero mal condicionada!)\n")
    print(f"Matriz A^(-1):\n{A_inv}\n")
    print(f"||A||_inf     = {norm_inf_A:.1f}")
    print(f"||A^(-1)||_inf = {norm_inf_Ainv:.1f}")
    print(f"kappa_inf(A)  = {cond_inf:,.0f}\n")
    print(f"kappa_2(A)    = {cond_2:,.2f}")
    print("=" * 60)

    # -------------------------------------------------------------
    # 2. Ejemplo de perturbación en Ax = b
    # -------------------------------------------------------------
    # Solución exacta x_bar
    x_bar = np.array([1.0, 1.0])
    b = A @ x_bar  # b = [1999.0, 1997.0]
    
    # Perturbación minúscula en b: delta_b = [0.001, -0.001]
    delta_b = np.array([0.001, -0.001])
    b_pert = b + delta_b
    
    # Solución perturbada x_hat
    x_hat = A_inv @ b_pert
    delta_x = x_hat - x_bar
    
    rel_error_b = np.linalg.norm(delta_b, np.inf) / np.linalg.norm(b, np.inf)
    rel_error_x = np.linalg.norm(delta_x, np.inf) / np.linalg.norm(x_bar, np.inf)
    
    print("\nSIMULACIÓN DE SENSIBILIDAD (Ax = b):")
    print(f"Vector b original:         {b}")
    print(f"Perturbación delta_b:      {delta_b}")
    print(f"Error relativo en b:       {rel_error_b:.2e} ({rel_error_b * 100:.6f}%)")
    print("-" * 60)
    print(f"Solución original x:       {x_bar}")
    print(f"Solución perturbada x_hat: {x_hat}")
    print(f"Error en x (delta_x):      {delta_x}")
    print(f"Error relativo en x:       {rel_error_x:.2e} ({rel_error_x * 100:.2f}%)")
    print(f"Factor de amplificación:   {rel_error_x / rel_error_b:,.0f} (Cota teórica: kappa_inf = {cond_inf:,.0f})")
    print("=" * 60)

    # -------------------------------------------------------------
    # 3. Visualización Gráfica Didáctica
    # -------------------------------------------------------------
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig = plt.figure(figsize=(16, 5), dpi=150)

    # -----------------------------------------
    # Panel 1: Interpretación Geométrica (Rectas casi paralelas)
    # -----------------------------------------
    ax1 = fig.add_subplot(1, 3, 1)
    # Ecuación 1: 1000*x1 + 999*x2 = b1 => x2 = (b1 - 1000*x1)/999
    # Ecuación 2:  999*x1 + 998*x2 = b2 => x2 = (b2 - 999*x1)/998
    x1_vals = np.linspace(-3, 5, 200)
    
    # Rectas originales
    x2_eq1 = (b[0] - A[0,0]*x1_vals) / A[0,1]
    x2_eq2 = (b[1] - A[1,0]*x1_vals) / A[1,1]
    
    # Rectas perturbadas
    x2_eq1_pert = (b_pert[0] - A[0,0]*x1_vals) / A[0,1]
    x2_eq2_pert = (b_pert[1] - A[1,0]*x1_vals) / A[1,1]
    
    ax1.plot(x1_vals, x2_eq1, color='#1f77b4', lw=2, label=r'Eq 1: $1000x_1 + 999x_2 = 1999$')
    ax1.plot(x1_vals, x2_eq2, color='#2ca02c', lw=2, linestyle='--', label=r'Eq 2: $999x_1 + 998x_2 = 1997$')
    ax1.plot(x1_vals, x2_eq1_pert, color='#ff7f0e', lw=1.5, linestyle=':', alpha=0.8, label=r'Eq 1 perturbada ($b_1+0.001$)')
    ax1.plot(x1_vals, x2_eq2_pert, color='#d62728', lw=1.5, linestyle=':', alpha=0.8, label=r'Eq 2 perturbada ($b_2-0.001$)')
    
    # Puntos de intersección
    ax1.scatter([x_bar[0]], [x_bar[1]], color='blue', s=80, zorder=5, label=r'$\bar{x} = [1, 1]^T$')
    ax1.scatter([x_hat[0]], [x_hat[1]], color='red', s=80, marker='X', zorder=5, label=r'$\hat{x} \approx [-0.997, 2.999]^T$')
    
    ax1.set_xlim(-3, 5)
    ax1.set_ylim(-3, 5)
    ax1.set_xlabel(r'$x_1$', fontsize=11)
    ax1.set_ylabel(r'$x_2$', fontsize=11)
    ax1.set_title("1. Rectas Casi Paralelas\n(Pendientes: -1.001001 vs -1.001002)", fontsize=11, fontweight='bold')
    ax1.legend(loc='lower left', fontsize=7.5, framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    # -----------------------------------------
    # Panel 2: Deformación de la Bola Unidad en Norma Infinito
    # -----------------------------------------
    ax2 = fig.add_subplot(1, 3, 2)
    # Bola unidad norma infinito: cuadrado [-1, 1] x [-1, 1]
    square = np.array([
        [-1, -1],
        [ 1, -1],
        [ 1,  1],
        [-1,  1],
        [-1, -1]
    ])
    
    # Imagen de la bola unidad bajo A: A @ x
    transformed_square = (A @ square.T).T
    
    # Graficar la imagen transformada
    ax2.plot(transformed_square[:, 0], transformed_square[:, 1], color='#9467bd', lw=2, label=r'$A(\mathcal{B}_\infty)$')
    
    # Vectores clave
    x_max = np.array([1.0, 1.0])       # Máxima magnificación
    x_min = np.array([1.0, -1.0])      # Mínima magnificación
    Ax_max = A @ x_max                 # [1999, 1997]
    Ax_min = A @ x_min                 # [1, 1]
    
    ax2.quiver(0, 0, Ax_max[0], Ax_max[1], angles='xy', scale_units='xy', scale=1, 
               color='#d62728', lw=2, label=r'$A x_{\max} = [1999, 1997]^T$ ($\|\cdot\|_\infty = 1999$)')
    ax2.quiver(0, 0, Ax_min[0]*200, Ax_min[1]*200, angles='xy', scale_units='xy', scale=1, 
               color='#1f77b4', lw=2, label=r'$A x_{\min} \times 200 = [200, 200]^T$ ($\|\cdot\|_\infty = 1$)')
    
    ax2.set_title(r"2. Deformación de la Bola Unidad $\mathcal{B}_\infty$" + "\n" + r"$\|Ax_{\max}\|_\infty / \|Ax_{\min}\|_\infty = 1999$", fontsize=11, fontweight='bold')
    ax2.set_xlabel(r'$y_1$', fontsize=11)
    ax2.set_ylabel(r'$y_2$', fontsize=11)
    ax2.legend(loc='upper left', fontsize=8, framealpha=0.9)
    ax2.grid(True, alpha=0.3)

    # -----------------------------------------
    # Panel 3: Comparación de Magnitudes de Error
    # -----------------------------------------
    ax3 = fig.add_subplot(1, 3, 3)
    categories = [r'Perturbación en $b$' + '\n' + r'$\frac{\|\delta b\|_\infty}{\|b\|_\infty}$', 
                  r'Error inducido en $x$' + '\n' + r'$\frac{\|\delta x\|_\infty}{\|x\|_\infty}$']
    values = [rel_error_b, rel_error_x]
    colors = ['#2ca02c', '#d62728']
    
    bars = ax3.bar(categories, values, color=colors, width=0.5, edgecolor='black', alpha=0.85)
    ax3.set_yscale('log')
    ax3.set_ylabel('Error Relativo (Escala Logarítmica)', fontsize=11)
    ax3.set_title(f"3. Amplificación del Error\nFactor: ~{rel_error_x/rel_error_b:,.0f}x " + r"($\approx \kappa_\infty(A)$)", fontsize=11, fontweight='bold')
    
    # Anotaciones numéricas sobre las barras
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.5,
                 f'{val:.2e}\n({val*100:.4f}%)' if val < 0.01 else f'{val:.2e}\n({val*100:.1f}%)',
                 ha='center', va='bottom', fontsize=9, fontweight='bold')
                 
    ax3.set_ylim(1e-8, 10)
    ax3.grid(True, which="both", ls="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig('clases/05/ejemplo_mal_condicionamiento.png', dpi=200, bbox_inches='tight')
    print("\nGráfico guardado en 'clases/05/ejemplo_mal_condicionamiento.png'")

if __name__ == "__main__":
    main()
