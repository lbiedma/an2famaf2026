import time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

# 1. Construir un problema SDP mal condicionado (laplaciano anisótropo 2D)
N = 200                # Grilla 200x200 => n = 40.000 incógnitas en el interior
eps = 1e-4             # Fuerte anisotropía
h = 1.0 / (N + 1)

# Derivada segunda 1D con diferencias finitas centradas
main_diag = 2.0 * np.ones(N)
off_diag = -1.0 * np.ones(N - 1)
D2 = sp.diags([off_diag, main_diag, off_diag], [-1, 0, 1]) / (h**2)
I = sp.eye(N)

# Operador 2D: -(u_xx + eps * u_yy) = f
# kron(D2, I) representa la derivada en x; kron(I, D2) representa la derivada en y
A = (sp.kron(D2, I) + eps * sp.kron(I, D2)).tocsc()
b = np.ones(A.shape[0])

# 2. Callbacks para registrar la norma escalar del residuo en cada iteración
norm_b = np.linalg.norm(b)
res_cg = [norm_b]
res_pcg = [norm_b]

def cb_cg(xk):
    res_cg.append(np.linalg.norm(b - A @ xk))

def cb_pcg(xk):
    res_pcg.append(np.linalg.norm(b - A @ xk))

# 3. Resolver con CG estándar (midiendo tiempo)
print("Resolviendo con CG estándar...")
t0_cg = time.perf_counter()
x_cg, info_cg = spla.cg(A, b, rtol=1e-6, maxiter=2000, callback=cb_cg)
time_cg = time.perf_counter() - t0_cg

# 4. Resolver con Gradiente Conjugado Precondicionado (PCG)
# Medimos tanto el cómputo del precondicionador (setup) como la resolución (solve)
print("Construyendo precondicionador y resolviendo con PCG...")
t0_setup = time.perf_counter()
ilu = spla.spilu(A, drop_tol=1e-3, fill_factor=10)
M_inv = spla.LinearOperator(A.shape, matvec=ilu.solve)
time_pcg_setup = time.perf_counter() - t0_setup

t0_solve = time.perf_counter()
x_pcg, info_pcg = spla.cg(A, b, M=M_inv, rtol=1e-6, maxiter=2000, callback=cb_pcg)
time_pcg_solve = time.perf_counter() - t0_solve
time_pcg_total = time_pcg_setup + time_pcg_solve

print(f"CG estándar:         {len(res_cg) - 1:3d} iteraciones | Tiempo: {time_cg:.3f} s")
print(f"PCG (Cholesky Inc.): {len(res_pcg) - 1:3d} iteraciones | Tiempo total: {time_pcg_total:.3f} s (Setup: {time_pcg_setup:.3f} s + Solve: {time_pcg_solve:.3f} s)")
print(f"-> Aceleración (Speedup): {time_cg / time_pcg_total:.1f}x más rápido")

# 4. Reconstrucción de la solución 2D con condiciones de contorno de Dirichlet (u = 0 en los bordes)
U_full = np.zeros((N + 2, N + 2))
# El vector solución corresponde a los nodos internos ordenados (i en x, j en y)
U_full[1:-1, 1:-1] = x_pcg.reshape((N, N))

x_grid = np.linspace(0, 1, N + 2)
y_grid = np.linspace(0, 1, N + 2)
X, Y = np.meshgrid(x_grid, y_grid, indexing='ij')

# 5. Gráficos: Solución de la EDP (3D y Mapa de Calor) + Curva de Convergencia
fig = plt.figure(figsize=(16, 5))

# Subplot 1: Superficie 3D de la solución
ax1 = fig.add_subplot(1, 3, 1, projection='3d')
surf = ax1.plot_surface(X, Y, U_full, cmap='viridis', edgecolor='none', alpha=0.9)
ax1.set_title(f"Solución 3D: -(u_xx + {eps}*u_yy) = 1\nGrilla {N}x{N} ({N**2:,} incógnitas)")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("u(x,y)")
ax1.view_init(elev=30, azim=-60)

# Subplot 2: Mapa de calor 2D mostrando capas límite (boundary layers)
ax2 = fig.add_subplot(1, 3, 2)
im = ax2.contourf(X, Y, U_full, levels=50, cmap='viridis')
plt.colorbar(im, ax=ax2, label="u(x, y)")
ax2.set_title(f"Mapa de Calor y Capa Límite en y\n(Difusión en y reducida por $\\varepsilon={eps}$)")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_aspect('equal')

# Subplot 3: Comparación de convergencia CG vs PCG
ax3 = fig.add_subplot(1, 3, 3)
ax3.semilogy(range(len(res_cg)), res_cg, 'r.-', label=f"CG estándar: {len(res_cg) - 1} iter ({time_cg:.2f} s)")
ax3.semilogy(range(len(res_pcg)), res_pcg, 'b.-', label=f"PCG (Cholesky Inc.): {len(res_pcg) - 1} iter ({time_pcg_total:.2f} s)")
ax3.set_title(f"Convergencia y Tiempo Total\n(Speedup: {time_cg / time_pcg_total:.1f}x más rápido)")
ax3.set_xlabel("Iteración")
ax3.set_ylabel("Norma del residuo $\|r_k\|_2$")
ax3.grid(True, which='both', linestyle='--', alpha=0.6)
ax3.legend(loc="upper right")

plt.tight_layout()
plt.savefig("clases/17/solucion_anisotropa.png", dpi=200)
print("Gráfico guardado en clases/17/solucion_anisotropa.png")
plt.show()
