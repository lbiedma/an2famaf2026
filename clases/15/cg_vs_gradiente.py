"""
Gradiente conjugado vs. descenso por el gradiente (búsqueda lineal exacta)
==========================================================================

Minimizar f(x) = (1/2) x^T A x - b^T x  es equivalente a resolver Ax = b
cuando A es simétrica definida positiva. Las curvas de nivel de f son
elipses. Si A está mal condicionada, esas elipses son muy alargadas.

- Descenso por el gradiente (SD): avanza siempre en la dirección del residuo
  r = b - Ax (el anti-gradiente). Con paso óptimo, cada tramo es ortogonal
  al siguiente: aparece el zig-zag típico.
- Gradiente conjugado (CG): las direcciones son A-ortogonales. En dimensión n,
  en aritmética exacta llega a x* en a lo sumo n iteraciones. En este ejemplo
  n = 2, así que CG termina en 2 pasos.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def quadratic(A, b, X, Y):
    """Evalúa f(x) = (1/2) x^T A x - b^T x sobre una malla 2D."""
    pts = np.stack([X.ravel(), Y.ravel()], axis=0)
    vals = 0.5 * np.sum(pts * (A @ pts), axis=0) - b @ pts
    return vals.reshape(X.shape)


def steepest_descent(A, b, x0, tol=1e-12, maxiter=80):
    """Descenso por el gradiente con búsqueda lineal exacta."""
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    r = b - A @ x
    for _ in range(maxiter):
        if np.linalg.norm(r) <= tol:
            break
        Ar = A @ r
        alpha = float(r @ r) / float(r @ Ar)
        x = x + alpha * r
        r = b - A @ x
        path.append(x.copy())
    return np.array(path)


def conjugate_gradient(A, b, x0, tol=1e-12, maxiter=20):
    """CG clásico (Hestenes–Stiefel / Fletcher–Reeves)."""
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    r = b - A @ x
    p = r.copy()
    rs_old = float(r @ r)
    for _ in range(maxiter):
        if np.sqrt(rs_old) <= tol:
            break
        Ap = A @ p
        alpha = rs_old / float(p @ Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        path.append(x.copy())
        rs_new = float(r @ r)
        p = r + (rs_new / rs_old) * p
        rs_old = rs_new
    return np.array(path)


def build_problem(kappa=25.0, theta=np.pi / 5):
    """Elipse rotada con número de condición kappa, solución x* = (1, 0.6)."""
    D = np.diag([kappa, 1.0])
    c, s = np.cos(theta), np.sin(theta)
    Q = np.array([[c, -s], [s, c]])
    A = Q @ D @ Q.T
    x_star = np.array([1.0, 0.6])
    b = A @ x_star
    x0 = np.array([-1.4, 1.35])
    return A, b, x_star, x0


def main():
    A, b, x_star, x0 = build_problem()
    path_sd = steepest_descent(A, b, x0)
    path_cg = conjugate_gradient(A, b, x0)

    xs = np.linspace(-1.8, 1.8, 400)
    ys = np.linspace(-1.4, 1.8, 400)
    X, Y = np.meshgrid(xs, ys)
    Z = quadratic(A, b, X, Y)
    f_star = 0.5 * x_star @ (A @ x_star) - b @ x_star
    levels = f_star + np.geomspace(1e-3, 40, 14)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), constrained_layout=True)

    ax = axes[0]
    ax.contour(X, Y, Z, levels=levels, colors="0.65", linewidths=0.8)
    ax.plot(path_sd[:, 0], path_sd[:, 1], "o-", color="#c0392b", ms=4,
            lw=1.4, label=f"Descenso por el gradiente ({len(path_sd)-1} pasos)")
    ax.plot(path_cg[:, 0], path_cg[:, 1], "s-", color="#1f6aa5", ms=6,
            lw=2.0, label=f"Gradiente conjugado ({len(path_cg)-1} pasos)")
    ax.plot(*x_star, "*", color="k", ms=14, label=r"$x^\ast$")
    ax.plot(*x0, "k^", ms=8, label=r"$x^0$")
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title("Trayectorias sobre las curvas de nivel de $f$")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.25)

    ax = axes[1]
    res_sd = np.linalg.norm(b - (path_sd @ A.T), axis=1)
    res_cg = np.linalg.norm(b - (path_cg @ A.T), axis=1)
    ax.semilogy(np.arange(len(res_sd)), res_sd, "o-", color="#c0392b",
                label="Descenso por el gradiente")
    ax.semilogy(np.arange(len(res_cg)), res_cg, "s-", color="#1f6aa5",
                label="Gradiente conjugado")
    ax.set_xlabel("iteración $k$")
    ax.set_ylabel(r"$\|r^k\|_2 = \|b - A x^k\|_2$")
    ax.set_title("Caída del residuo")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

    fig.suptitle(
        r"Elipse alargada: SD zigzaguea; CG llega en $n=2$ pasos",
        fontsize=13,
    )
    out = Path(__file__).with_suffix(".png")
    fig.savefig(out, dpi=160)
    print(f"A cond(A) = {np.linalg.cond(A):.1f}")
    print(f"SD: {len(path_sd)-1} iteraciones,  ||r|| = {res_sd[-1]:.2e}")
    print(f"CG: {len(path_cg)-1} iteraciones,  ||r|| = {res_cg[-1]:.2e}")
    print(f"Figura guardada en {out}")
    plt.show()


if __name__ == "__main__":
    main()
