"""
Demostración de Estabilidad Numérica: Factorización QR vs. Ecuaciones Normales
==============================================================================

Este script compara la estabilidad numérica al resolver el problema de mínimos
cuadrados (Ax ≈ b) mediante dos enfoques:
  1. Ecuaciones Normales: (A^T A) x = A^T b
  2. Factorización QR: A = Q R  =>  R x = Q^T b

Motivo Teórico:
---------------
Las Ecuaciones Normales requieren calcular A^T A, lo cual eleva al cuadrado
el número de condición: cond(A^T A) = (cond(A))^2.
Esto produce una pérdida drástica de precisión de máquina o incluso singularidad.
La factorización QR opera directamente sobre A sin elevar al cuadrado cond(A).
"""

import numpy as np


def ejemplo_vandermonde():
    """
    Ejemplo 1: Ajuste polinómico de grado 10 con una matriz de Vandermonde.
    Muestra la degradación de precisión en Ecuaciones Normales por mal condicionamiento.
    """
    print("=" * 70)
    print(" EJEMPLO 1: Ajuste Polinómico con Matriz de Vandermonde (Grado 10)")
    print("=" * 70)

    np.random.seed(42)

    # 15 puntos equidistantes en [0, 1]
    x_pts = np.linspace(0, 1, 15)

    # Matriz de Vandermonde A de 15 x 11
    A = np.vander(x_pts, 11, increasing=True)

    # Solución exacta conocida x* = [1, 1, ..., 1]^T
    x_exact = np.ones(11)
    b = A @ x_exact

    # -------------------------------------------------------------------------
    # Método 1: Ecuaciones Normales (A^T A x = A^T b)
    # -------------------------------------------------------------------------
    ATA = A.T @ A
    ATb = A.T @ b
    x_normales = np.linalg.solve(ATA, ATb)

    # -------------------------------------------------------------------------
    # Método 2: Descomposición QR (A = Q R  =>  R x = Q^T b)
    # -------------------------------------------------------------------------
    Q, R = np.linalg.qr(A)
    x_qr = np.linalg.solve(R, Q.T @ b)

    # -------------------------------------------------------------------------
    # Métricas y Comparación
    # -------------------------------------------------------------------------
    cond_A = np.linalg.cond(A)
    cond_ATA = np.linalg.cond(ATA)

    err_normales = np.linalg.norm(x_normales - x_exact) / np.linalg.norm(x_exact)
    err_qr = np.linalg.norm(x_qr - x_exact) / np.linalg.norm(x_exact)

    print(f"Número de condición cond(A):     {cond_A:.4e}")
    print(f"Número de condición cond(A^T A): {cond_ATA:.4e}  [cond(A)^2]")
    print("-" * 70)
    print(f"Error relativo Ecuaciones Normales: {err_normales:.4e}  (~{err_normales*100:.2f}% de error)")
    print(f"Error relativo Factorización QR:    {err_qr:.4e}")
    print("-" * 70)


if __name__ == "__main__":
    ejemplo_vandermonde()
