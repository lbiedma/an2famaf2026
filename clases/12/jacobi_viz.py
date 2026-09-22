import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def jacobi_rot(app: float, apq: float, aqq: float):
    """
    Calcula cos(theta) y sin(theta) para anular el elemento apq
    siguiendo la parametrización estable del algoritmo de Jacobi 2x2.
    """
    if np.isclose(apq, 0.0):
        return 1.0, 0.0
    
    tau = (aqq - app) / (2.0 * apq)
    if tau >= 0:
        t = -1.0 / (tau + np.sqrt(tau**2 + 1.0))
    else:
        t = 1.0 / (-tau + np.sqrt(tau**2 + 1.0))
        
    c = 1.0 / np.sqrt(1.0 + t**2)
    s = t * c
    return c, s


def off_norm(A: np.ndarray, user_formula: bool = False) -> float:
    """
    Calcula la norma fuera de la diagonal:
      - Estándar: sqrt(sum_{i!=j} a_ij^2) = ||A - diag(diag(A))||_F
      - user_formula: ||A||_F - ||diag(A)||_2
    """
    if user_formula:
        return float(np.linalg.norm(A, 'fro') - np.linalg.norm(np.diag(A)))
    return float(np.linalg.norm(A - np.diag(np.diag(A)), 'fro'))


def jacobi_diagonalization_animated(
    A: np.ndarray,
    tol: float = 1e-6,
    max_iter: int = 50,
    interval: int = 300,
    save_path: str = None,
    user_formula: bool = False,
    use_abs: bool = True,
    cmap: str = "viridis"
):
    """
    Diagonaliza una matriz real simétrica A mediante el método de Jacobi y
    genera una animación interactiva con un heatmap y la curva de convergencia.
    
    Parámetros:
    -----------
    A : np.ndarray
        Matriz cuadrada simétrica real (n x n).
    tol : float
        Tolerancia para la condición de parada sobre off(A).
    max_iter : int
        Cantidad máxima de rotaciones (iteraciones).
    interval : int
        Milisegundos entre frames de la animación.
    save_path : str, opcional
        Ruta para exportar (ej: 'jacobi.gif' o 'jacobi.mp4').
    user_formula : bool
        Si True usa norm(A, 'frob') - norm(diag(A)), sino la norma off(A) estándar.
    use_abs : bool
        Si True, el color del heatmap se basa en el módulo |A_ij| en [0, max|A|].
        Si False, usa el valor con signo A_ij con mapa centrado en 0.
    cmap : str
        Colormap de matplotlib (ej: 'viridis', 'magma', 'plasma', 'coolwarm').
        
    Retorna:
    --------
    D : np.ndarray
        Matriz diagonal resultante con los autovalores aproximados.
    Q : np.ndarray
        Matriz ortogonal acumulada (sus columnas son los autovectores).
    ani : FuncAnimation
        Objeto de animación de matplotlib.
    """
    A = np.copy(A).astype(float)
    n = A.shape[0]
    assert A.shape[0] == A.shape[1], "La matriz debe ser cuadrada."
    assert np.allclose(A, A.T), "La matriz debe ser simétrica."

    # Matriz de autovectores acumulada
    Q = np.eye(n)

    # Registro de pasos para la animación
    history_A = [np.copy(A)]
    history_off = [off_norm(A, user_formula=user_formula)]
    history_pairs = [(None, None)]

    # --- Bucle de Jacobi ---
    for k in range(max_iter):
        current_off = history_off[-1]
        if current_off <= tol:
            break

        # 1. Encontrar el par (p, q) con p != q de mayor valor absoluto
        A_nodiag = np.copy(A)
        np.fill_diagonal(A_nodiag, 0.0)
        idx_max = np.argmax(np.abs(A_nodiag))
        p, q = np.unravel_index(idx_max, A.shape)
        if p > q:
            p, q = q, p

        # 2. Calcular rotación 2x2
        c, s = jacobi_rot(A[p, p], A[p, q], A[q, q])

        # 3. Aplicar rotación ortogonal a A y acumular en Q
        J = np.array([[c, -s],
                      [s,  c]])
        
        # A_I* <- J.T @ A_I*
        A[[p, q], :] = J.T @ A[[p, q], :]
        # A_*I <- A_*I @ J
        A[:, [p, q]] = A[:, [p, q]] @ J

        # Q_*I <- Q_*I @ J
        Q[:, [p, q]] = Q[:, [p, q]] @ J

        # Guardar estado
        history_A.append(np.copy(A))
        history_off.append(off_norm(A, user_formula=user_formula))
        history_pairs.append((p, q))

    # --- Configuración de la Animación (Heatmap + Gráfico de convergencia) ---
    fig, (ax_heat, ax_conv) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Escala y datos según si se usa el módulo o el valor con signo
    vmax = np.max(np.abs(history_A[0]))
    if use_abs:
        vmin = 0.0
        init_data = np.abs(history_A[0])
        cbar_label = r'$|A_{ij}|$'
    else:
        vmin = -vmax
        init_data = history_A[0]
        cbar_label = r'$A_{ij}$'
        if cmap == "viridis":
            cmap = "coolwarm"

    im = ax_heat.imshow(init_data, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar = fig.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
    cbar.set_label(cbar_label, rotation=270, labelpad=15)

    ax_heat.set_xticks(range(n))
    ax_heat.set_yticks(range(n))
    
    # Textos de valores si n <= 8 para que sea legible
    texts = []
    if n <= 8:
        for i in range(n):
            for j in range(n):
                val = history_A[0][i, j]
                cell_intensity = abs(val) / vmax if vmax > 0 else 0
                txt = ax_heat.text(
                    j, i, f"{val:.2f}", ha="center", va="center", 
                    color="white" if cell_intensity > 0.5 and use_abs else ("black" if cell_intensity < 0.6 else "white"),
                    fontsize=9
                )
                texts.append(txt)

    title_heat = ax_heat.set_title(f"Iteración: 0 | off(A): {history_off[0]:.2e}")

    # Subplot de convergencia
    iters = list(range(len(history_off)))
    ax_conv.set_xlim(0, max(1, len(history_off) - 1))
    ax_conv.set_ylim(max(1e-16, min(history_off) * 0.5), max(history_off) * 1.5)
    ax_conv.set_yscale('log')
    ax_conv.set_xlabel("Rotaciones (k)")
    ax_conv.set_ylabel("off(A)")
    ax_conv.set_title("Convergencia de off(A)")
    ax_conv.axhline(tol, color='red', linestyle='--', alpha=0.7, label=f"Tolerancia = {tol}")
    ax_conv.grid(True, which="both", ls=":", alpha=0.6)
    ax_conv.legend(loc="upper right")
    line_conv, = ax_conv.plot([], [], marker='o', color='navy', markersize=4)

    def update(frame):
        mat = history_A[frame]
        off_k = history_off[frame]
        p, q = history_pairs[frame]

        # Actualizar datos del heatmap según use_abs
        im.set_data(np.abs(mat) if use_abs else mat)
        
        pair_str = f" | Anulado: ({p}, {q})" if p is not None else ""
        title_heat.set_text(f"Iteración: {frame}/{len(history_A)-1} | off(A): {off_k:.2e}{pair_str}")

        if n <= 8 and texts:
            idx = 0
            for i in range(n):
                for j in range(n):
                    val = mat[i, j]
                    cell_intensity = abs(val) / vmax if vmax > 0 else 0
                    texts[idx].set_text(f"{val:.2f}" if abs(val) >= 1e-2 else "0.00")
                    # Contraste de texto
                    if use_abs:
                        # En mapas como viridis, valores bajos son oscuros (texto blanco) o viceversa
                        texts[idx].set_color("black" if cell_intensity > 0.6 else "white")
                    else:
                        texts[idx].set_color("black" if cell_intensity < 0.6 else "white")
                    idx += 1

        line_conv.set_data(iters[:frame + 1], history_off[:frame + 1])
        return [im, title_heat, line_conv] + texts

    ani = animation.FuncAnimation(
        fig, update, frames=len(history_A), interval=interval, repeat=True, blit=False
    )

    if save_path:
        if save_path.endswith('.gif'):
            ani.save(save_path, writer='pillow', fps=1000 // interval)
        else:
            ani.save(save_path, writer='ffmpeg', fps=1000 // interval)
        print(f"Animación guardada con éxito en: {save_path}")

    plt.tight_layout()
    return A, Q, ani


if __name__ == "__main__":
    # Generamos una matriz simétrica aleatoria de 5x5
    np.random.seed(42)
    n = 10
    M = np.random.randn(n, n)
    A_sym = (M + M.T)

    print("Matriz inicial A:")
    print(np.round(A_sym, 3))

    # Ejecutamos la función con animación
    # En Jupyter Notebook podés mostrarla con:
    # from IPython.display import HTML; HTML(ani.to_jshtml())
    D, Q, ani = jacobi_diagonalization_animated(
        A_sym,
        tol=1e-5,
        max_iter=40,
        interval=500,
        save_path="jacobi_diagonalizacion.gif"  # O None si no querés guardarla
    )

    print("\nMatriz diagonal obtenida D (autovalores en diagonal):")
    print(np.round(D, 4))

    print("\nAutovalores según np.linalg.eigvalsh:")
    print(np.sort(np.linalg.eigvalsh(A_sym)))
    print("Autovalores con Jacobi:")
    print(np.sort(np.diag(D)))

    print(f"\nError de ortogonalidad ||Q^T Q - I||_F: {np.linalg.norm(Q.T @ Q - np.eye(n)):.2e}")
    print(f"Error de similitud ||Q^T A Q - D||_F: {np.linalg.norm(Q.T @ A_sym @ Q - D):.2e}")

    plt.show()
