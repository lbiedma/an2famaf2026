---
marp: true
theme: default
paginate: true
style: |
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }

---

# Análisis Numérico II / Álgebra Lineal Numérica
## Clase 17: GMRES Revisitado
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Marco General de los Métodos de Proyección

Para resolver el sistema lineal $Ax = b$ con $A \in \mathbb{R}^{n \times n}$ no singular y solución exacta $x^*$:

- Se construye $\{x^k\}$ proyectando $x^*$ sobre $\mathcal{M}_k \subseteq \mathbb{R}^n$.
- Las variedades afines son $z + \mathcal{K} = \{z + v \mid v \in \mathcal{K}\}$, donde $\mathcal{K} \subseteq \mathbb{R}^n$ es un subespacio vectorial y $z \in \mathbb{R}^n$.
- No se conoce $x^*$, entonces se plantea minimizar $f(x) = \frac{1}{2} x^T Q x + x^T q + c$ con $Q \in \mathbb{R}^{n \times n}$ simétrica semidefinida positiva, $q \in \mathbb{R}^n$ y $c \in \mathbb{R}$.
- El esquema iterativo es:
  1. Si $\|\nabla f(x^k)\| = 0$, detener.
  2. Obtener $x^{k+1}$ como la solución de minimizar $f(x)$ sobre $\mathcal{M}_k$.
  3. Definir $\mathcal{M}_{k+1}$, hacer $k \leftarrow k + 1$ y repetir.

---

# Teorema: Minimización sobre Variedades Afines

Sea $z \in \mathbb{R}^n$, $\mathcal{K} \subseteq \mathbb{R}^n$ un subespacio vectorial, y $f: \mathbb{R}^n \to \mathbb{R}$ definida anteriormente. El vector $\bar{x}$ es solución del problema de minimización:
$$\min_{x \in z + \mathcal{K}} f(x) \quad$$
si y solo si $\bar{x} \in z + \mathcal{K}$ y satisface la condición de ortogonalidad:
$$\nabla f(\bar{x})^T v = 0, \quad \forall v \in \mathcal{K} \quad$$

---

# Demostración: Necesidad ($\Rightarrow$)

Sea $\bar{x}$ solución de $\min_{x \in z + \mathcal{K}} f(x)$, de modo que existe $\bar{v} \in \mathcal{K}$ con $\bar{x} = z + \bar{v}$.

- Dado $v \in \mathcal{K}$ arbitrario y $t \in \mathbb{R}$, como $\mathcal{K}$ es subespacio, el vector perturbado pertenece a la variedad afín: $\bar{x} + tv = z + (\bar{v} + tv) \in z + \mathcal{K}$.
- Dado que $\bar{x}$ minimiza a $f$ en la variedad, vale $f(\bar{x}) \le f(\bar{x} + tv)$ para todo $t \in \mathbb{R}$.
- Tomando $t > 0$ y la diferenciabilidad de $f$:
   $$0 \le \lim_{t \to 0^+} \frac{f(\bar{x} + tv) - f(\bar{x})}{t} = \nabla f(\bar{x})^T v \quad$$
- Repitiendo el argumento para $-v \in \mathcal{K}$, queda $\nabla f(\bar{x})^T (-v) \ge 0$, es decir, $\nabla f(\bar{x})^T v \le 0$. Por lo tanto, $\nabla f(\bar{x})^T v = 0$ para todo $v \in \mathcal{K}$.

---

# Demostración: Suficiencia ($\Leftarrow$)

Sea $\bar{x} \in z + \mathcal{K}$ tal que $\nabla f(\bar{x})^T v = 0$ $\forall v \in \mathcal{K}$. Entonces $\bar{x} = z + \bar{v}$ con $\bar{v} \in \mathcal{K}$.

- Para cualquier $x \in z + \mathcal{K}$ arbitrario, existe $v \in \mathcal{K}$ tal que $x = z + v$.
- Como $v - \bar{v} \in \mathcal{K}$, se cumple que $\nabla f(\bar{x})^T (v - \bar{v}) = 0$.
- Notando que $x - \bar{x} = v - \bar{v}$, $\nabla^2 f(x) = Q$ es semidefinida positiva y las derivadas de orden superior son nulas, realizamos la expansión exacta de Taylor:
   $$f(x) = f(\bar{x}) + \nabla f(\bar{x})^T (x - \bar{x}) + \frac{1}{2} (x - \bar{x})^T \nabla^2 f(\bar{x}) (x - \bar{x}) \quad$$
   $$f(x) = f(\bar{x}) + \underbrace{\nabla f(\bar{x})^T (v - \bar{v})}_{= 0} + \frac{1}{2} \underbrace{(v - \bar{v})^T Q (v - \bar{v})}_{\ge 0} \ge f(\bar{x}) \quad$$
- Por lo tanto, $f(x) \ge f(\bar{x}) \forall x \in z + \mathcal{K}$, y $\bar{x}$ es minimizador global sobre $z + \mathcal{K}$. $\blacksquare$

---

# Caso Matriz General

Cuando $A \in \mathbb{R}^{m \times n}$ no es simétrica ni definida positiva:

- **Función Objetivo:** Se minimiza la norma Euclídea del residuo $\|A x - b\|_2$, lo que equivale a considerar la norma $\|x - x^*\|_{A^T A}^2 = \|A x - b\|_2^2$.
- **Formulación:** Se minimiza la función cuadrática:
  $$f(x) = \frac{1}{2} x^T A^T A x - x^T A^T b \quad$$
- **Corolario** Dado $z \in \mathbb{R}^n$ y $V \in \mathbb{R}^{n \times p}$, el vector $\bar{x} = z + V \bar{\alpha}$ minimiza $f(x)$ sobre $z + \text{Im}(V)$ si y solo si $\bar{\alpha}$ satisface el sistema:
  $$(V^T A^T A V) \bar{\alpha} = V^T A^T r, \quad \text{con } r = b - A z \quad$$

---

# Método de Arnoldi: Construcción de la Base

Para evitar problemas numéricos, el método de Arnoldi construye iterativamente una base ortonormal $V = [v_1 \dots v_p]$ tal que $H = V^T A V$ sea Hessenberg superior:

- Partiendo de $v_1 = v / \|v\|_2$, se exige $A V = V H$ con
  $$A v_j = \sum_{i=1}^{j+1} h_{ij} v_i = \sum_{i=1}^j h_{ij} v_i + h_{j+1, j} v_{j+1} \quad$$
  donde $h_{lj} = v_l^T A v_j$ para $l = 1, \dots, j$, y $h_{j+1, j} v_{j+1} = A v_j - \sum_{i=1}^j h_{ij} v_i$.
- **Teorema:** Si el método de Arnoldi no se detiene antes del paso $m$ ($h_{j+1, j} \neq 0$), los vectores $\{v_1, v_2, \dots, v_m\}$ forman una **base ortonormal** del subespacio $\mathcal{K}_m(A, v)$.

---

# Algoritmo (Método de Arnoldi)

**Entradas:** $A \in \mathbb{R}^{n \times n}$, $v \in \mathbb{R}^n$, $m \le n$.
**Salidas:** $H \in \mathbb{R}^{(m+1) \times m}$ Hessenberg superior y base ortonormal $V \in \mathbb{R}^{n \times m}$.

1. Si $\|v\|_2 = 0$, definir $H = 0$, $V = 0$ y terminar.
2. Para $j = 1, \dots, m$:
   1. $V_{*, j} = v / \|v\|_2$, $v = A V_{*, j}$.
   2. Para $i = 1, \dots, j$:
       $$H_{ij} = v^T V_{*, i}, \quad v \leftarrow v - H_{ij} V_{*, i} \quad$$
   3. Si $\|v\|_2 = 0$, terminar. Sino, definir $H_{j+1, j} = \|v\|_2$.
3. Retornar $H$ y $V$.

---

# Propiedades Matriciales y la Relación de Arnoldi

Al agrupar los $m$ pasos del algoritmo se deduce la identidad del subespacio de Krylov:

**Proposición** Sea $A \in \mathbb{R}^{n \times n}$ y suponga que Arnoldi realiza $m$ pasos ($m \le n$). Sea $\bar{H}_m \in \mathbb{R}^{(m+1) \times m}$ la matriz generada, y $H_m \in \mathbb{R}^{m \times m}$ $\bar{H}_m$ sin la última fila.
- **Demostración:** se genera la *Identidad de Arnoldi*:
  $$A V_m = V_m H_m + h_{m+1, m} v^{m+1} (e^m)^T = V_{m+1} \bar{H}_m \quad$$
  donde $e^m = [0, \dots, 0, 1]^T \in \mathbb{R}^m$.
- Multiplicando por $(V_m)^T$ a izquierda y utilizando que $(V_m)^T V_m = I_m$ y $(V_m)^T v^{m+1} = 0$, se obtiene $H_m$, la *Proyección de Galerkin* de $A$ sobre $\mathcal{K}_m(A, v)$:
  $$(V_m)^T A V_m = H_m \quad$$

---

# El Método GMRES

Se resuelve el problema de minimización del residuo sobre $\mathcal{K}_m(A, r_0)$ reduciéndolo a un problema equivalente de cuadrados mínimos de dimensión pequeña.

**Teorema:** Para $A \in \mathbb{R}^{n \times n}$, el vector $\bar{x}$ es solución del problema de minimización:
  $$\min_{x \in x_0 + \mathcal{K}_m(A, r_0)} \|Ax - b\|_2 \quad$$
  si y solo si $\bar{x} = x_0 + V_m \bar{\alpha}$, donde $\bar{\alpha} \in \mathbb{R}^m$ es la solución del problema de cuadrados mínimos reducido:
  $$\min_{\alpha \in \mathbb{R}^m} \|\bar{H}_m \alpha - \sigma e_1\|_2 \quad$$
  donde $\sigma = \|r_0\|_2$, $e_1 = [1, 0, \dots, 0]^T \in \mathbb{R}^{m+1}$, y $\bar{H}_m \in \mathbb{R}^{(m+1) \times m}, V_m \in \mathbb{R}^{n \times m}$ son generadas por el método de Arnoldi a partir de $v = r_0$.

---

# Demostración

Dado que $\mathcal{K}_m(A, r_0) = \text{Im}(V_m)$, cualquier vector $x \in x_0 + \mathcal{K}_m(A, r_0)$ se representa como $x = x_0 + V_m \alpha$ para algún $\alpha \in \mathbb{R}^m$.

1. Sustituyendo  $A V_m = V_{m+1} \bar{H}_m$ y viendo que $r^0 = \sigma v^1 = \sigma V_{m+1} e^1$:
   $$Ax - b = A(x_0 + V_m \alpha) - b = A V_m \alpha - r_0 \quad$$
   $$Ax - b = V_{m+1} \bar{H}_m \alpha - \sigma V_{m+1} e^1 = V_{m+1}(\bar{H}_m \alpha - \sigma e^1) \quad$$
2. Como las columnas de $V_{m+1}$ son ortonormales, se preserva la norma 2:
   $$\|Ax - b\|_2 = \|V_{m+1}(\bar{H}_m \alpha - \sigma e^1)\|_2 = \|\bar{H}_m \alpha - \sigma e^1\|_2 \quad$$
3. Minimizar $\|Ax - b\|_2$ sobre $x_0 + \mathcal{K}_m(A, r_0)$ equivale a resolver un problema de cuadrados mínimos de dimensión $(m+1) \times m$ sobre $\mathbb{R}^m$. $\blacksquare$

---

# Algoritmo: Método GMRES

**Entradas:** $A \in \mathbb{R}^{n \times n}$, $b, x \in \mathbb{R}^n$, $\varepsilon > 0$, $m \in \mathbb{N}$ (máx. iteraciones externas) y $m_A \ll n$ (dimensión del subespacio de Krylov). **Salida:** $x^+$ aproximación de $x^*$.

1. Definir $r = b - Ax$ y $\sigma = \|b - Ax\|_2$.
2. Para $k = 1, \dots, m$: Si $\sigma \le \varepsilon$, ir al Paso 3.
   - Definir $\bar{H}, V$ aplicando $Arnoldi(A, r, m_A)$.
   - $\alpha, \sigma_+$ aplicando $CuadradosMinimosQR( \bar{H}, \sigma e_1)$.
   - $x \leftarrow x + V \alpha$.
   - $r = b - Ax$.
   - $\sigma = \sigma_+$.
3. Retornar $x^+ = x$.

--- 

# Precondicionamiento

La velocidad de convergencia de los métodos iterativos está fuertemente determinada por las propiedades espectrales de $A$:

- **Mal Condicionamiento:** Si $\kappa(A) \gg 1$, los métodos iterativos requieren un número prohibitivo de pasos para alcanzar una tolerancia deseada.
- **Autovalores:** Un espectro muy amplio frena drásticamente la convergencia.

Podemos reemplazar el sistema original $Ax = b$ por un sistema equivalente que posea un **número de condición cercano a 1** o un **agrupamiento de autovalores** alrededor de $1$.

---

# Formulación Matemática

Buscamos una matriz no singular $M \in \mathbb{R}^{n \times n}$ (el **precondicionador**) que aproxime a $A$:

- **Precondicionamiento por la Izquierda:**
  $$M^{-1} A x = M^{-1} b \quad$$
  *Se modifica el residuo:* $\tilde{r} = M^{-1}(b - Ax)$.

- **Precondicionamiento por la Derecha:**
  $$A M^{-1} y = b, \quad \text{con } x = M^{-1} y \quad$$
  *Conserva la norma del residuo original:* $b - A M^{-1} y = b - Ax$.

- **Precondicionamiento Simétrico (para $A$ SDP):**
  Dado $M = L L^T$, se resuelve $L^{-1} A L^{-T} \hat{x} = L^{-1} b$ con $x = L^{-T} \hat{x}$, preservando la simetría y definición positiva del sistema.

---

# Condiciones de un Buen Precondicionador

La elección de $M$ debe equilibrar eficacia y costo computacional:

1. **Aproximación Espectral ($M \approx A$):**
   - La matriz precondicionada $M^{-1}A$ debe estar bien condicionada: $\kappa(M^{-1}A) \ll \kappa(A)$.
   - Los autovalores de $M^{-1}A$ deben estar agrupados cerca de 1 en $\mathbb{C}$.

2. **Bajo Costo por Iteración:**
   - En cada iteración se debe resolver un sistema auxiliar $M z = r$.
   - La resolución de $M z = r$ debe ser muy rápida, costo $\approx$ **$O(n)$** o **$O(\text{nnz})$**.

---

# Precondicionadores Clásicos y Algebraicos

- **Precondicionador de Jacobi (Diagonal):**
  - $M = D = \text{diag}(A)$, eficaz si $A$ es diagonal dominante.
- **Precondicionadores de Relajación (Gauss-Seidel / SSOR):**
  - Utilizan las partes triangulares de $A$: $M_{SSOR} = \frac{1}{\omega(2-\omega)} (D + \omega L) D^{-1} (D + \omega U)$.
- **Factorizaciones Incompletas (ILU / IC):**
  - **ILU(0):** Realiza una factorización $LU$ ignorando todo elemento fuera del patrón de dispersión de $A$.
  - **Cholesky Incompleto (IC):** Para matrices SDP, calcula $M = R^T R \approx A$ conservando la dispersión original.
