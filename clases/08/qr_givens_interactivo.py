import numpy as np

def givens_rotation(a, b):
    """Calcula c (coseno) y s (seno) para la rotación de Givens."""
    if b == 0:
        return 1.0, 0.0
    elif abs(b) > abs(a):
        tau = -a / b
        s = -np.sign(b) / np.sqrt(1 + tau**2)
        c = s * tau
    else:
        tau = -b / a
        c = np.sign(a) / np.sqrt(1 + tau**2)
        s = c * tau
    return c, s

def qr_givens_demo(A_orig):
    A = A_orig.copy().astype(float)
    m, n = A.shape
    Q = np.eye(m)
    
    print("Matriz Original A:")
    print(np.round(A, 4))
    print("-" * 60)
    
    step = 1
    p = min(m - 1, n)
    for j in range(p):
        for i in range(j + 1, m):
            if A[i, j] != 0:
                c, s = givens_rotation(A[j, j], A[i, j])
                
                # Matriz de rotación local de 2x2
                G_sub = np.array([[c, -s],
                                  [s,  c]])
                
                print(f"\n[Paso {step}] Anulando elemento A[{i},{j}] ({A[i,j]:.4f}) usando el pivote A[{j},{j}] ({A[j,j]:.4f})")
                print(f"  -> Coeficientes de Givens: c = {c:.6f}, s = {s:.6f}")
                
                # Actualizar las filas j e i de la matriz A (R en progreso)
                A[[j, i], j:] = G_sub @ A[[j, i], j:]
                
                # Forzamos analíticamente el cero para eliminar error de precisión
                A[i, j] = 0.0
                
                # Actualizar la matriz ortogonal Q
                Q[:, [j, i]] = Q[:, [j, i]] @ G_sub.T
                
                print("  Matriz A actualmente:")
                print(np.round(A, 4))
                step += 1
                
    print("\n" + "=" * 60)
    print("Factor R (Triangular Superior):")
    print(np.round(A, 4))
    print("\nFactor Q (Ortogonal):")
    print(np.round(Q, 4))

    print("\nChequeo Q Ortogonal")
    print(f"Q Q^T = {Q@Q.T}")
    print(np.allclose(Q @ Q.T, np.eye(m)))

if __name__ == "__main__":
    # Matriz con primera columna pitagórica [3-5]^T (Norma = 13)
    A = np.array([[3.0,  5.0,  1.0],
                  [4.0,  1.0,  2.0],
                  [12.0, 2.0,  8.0]])
    qr_givens_demo(A)
