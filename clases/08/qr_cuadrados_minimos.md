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
## Clase 08: QR por Householder y Cuadrados Mínimos
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Algoritmo **(Reflexión de Householder)**

**Entrada:** $x \in \mathbb{R}^m$. **Salidas:** $u \in \mathbb{R}^m, \ \rho \in \mathbb{R}$ tal que $I - \rho u u^T x = \sigma e^1$

- Definir $\sigma = \sum_{i=2}^m x_i^2$
- Si $\sigma = 0$, **retornar** $u = 0, \ \rho = 0$
- Definir $\mu = \sqrt{\sigma + x_1^2}$
- Si $x_1 \le 0$, definir $\gamma = x_1 - \mu$, sino definir $\gamma = -\sigma / (x_1 + \mu)$
- Definir $\rho = 2 \gamma^2 / (\sigma + \gamma^2)$
- **Retornar** $u = \begin{bmatrix} 1, & x_2 / \gamma, & \dots, & x_m / \gamma \end{bmatrix}^T$ y $\rho$

---

# Algoritmo **(Desc. QR por Refl. de Householder)**

**Entrada:** $A \in \mathbb{R}^{m \times n}$. **Salidas:** $Q \in \mathbb{R}^{m \times m}$ ortogonal, $
R \in \mathbb{R}^{m \times n}$ triangular superior
- Definir $Q = I$, $p = \text{min}(m, n)$
- Para $j = 1 \dots p$, definir $\mathcal{I} = \{j, \dots, m\}$, $\mathcal{J} = \{j, \dots, n\}$
  - $u, \rho$ = Householder($A_{\mathcal{I}, j}$)
  - $w = \rho u$
  - $A_{\mathcal{I}, \mathcal{J}} \leftarrow A_{\mathcal{I}, \mathcal{J}} - w (u^T A_{\mathcal{I}, \mathcal{J}})$ 
  - $Q_{*, \mathcal{I}} \leftarrow Q_{*, \mathcal{I}} - (Q_{*, \mathcal{I}} w) u^T$  
- **Retornar:** $Q$, $R = A$

---

# Implementación Práctica

- Dónde se metió $P$? :eyes:
- Formar explícitamente la matriz de Householder requiere $O(m^2)$ de memoria y $O(m^2 n)$ de operaciones inútiles.
- Explotamos que es una matriz de rango 1 para aplicarla directamente sobre $A$:
  $$PA = (I - \beta v v^T)A = A - \beta v (v^T A)$$

- Este procedimiento reduce el costo a **$2mn$ flops** por aplicación de reflector.

---

# Conteo Operacional (Crear R)

Sumamos el costo de las actualizaciones de rango 1 en cada paso $k$ de dimensión decreciente $m' = m-k+1$ y $n' = n-k+1$:

- **Multiplicación vector-matriz ($w^T = v^T A'$):** $\approx 2m'n'$ flops.
- **Actualización de rango 1 ($A' - \beta v w^T$):** $\approx 2m'n'$ flops.
- **Costo total por paso $k$:** $\approx 4(m-k+1)(n-k+1)$ flops.

Sumando desde $k=1$ hasta $n$, obtenemos el costo $2mn^2 - \frac{2}{3}n^3$ flops.

- Si $m = n$, el costo es de $\frac{4}{3}n^3$ flops.
- Si $m \gg n$, el término $2mn^2$ domina, con un costo aproximado de $2mn^2$ flops.

---

# Algo para notar sobre Q

- En el algoritmo estamos construyendo $Q$, pero en realidad no necesitamos construirla.

- En su lugar, guardamos el vector de Householder $u_k$ dentro de las posiciones que se acaban de anular por debajo de la diagonal (_pierdo información?_).

- El escalar $\rho_k$ se guarda de forma paralela en un vector auxiliar de tamaño $n$.

- Si necesitamos multiplicar por $Q^T$, aplicamos la secuencia de actualizaciones:

$$Q^T b = (Q_n \cdots Q_2 Q_1) b $$

---

# Householder vs. Givens: ¿Cuándo usar cuál?

| Característica | 🔨 **Householder** *(El Martillo)* | 🔪 **Givens** *(El Bisturí)* |
| :--- | :--- | :--- |
| **Acción** | Anula **toda una subcolumna** en un solo paso. | Anula **un único elemento** a la vez (afecta 2 filas). |
| **Geometría** | Reflexión respecto a un hiperplano. | Rotación plana en 2D. |
| **Uso Ideal** | Matrices **densas** (más rápido y estable). | Matrices **dispersas**, en banda o estructuradas. |

---

# **Teorema** (Forma Reducida de QR):

Si $A=QR$ es la descomposición QR de $A \in \mathbb{R}^{m \times n}$ de rango $n$ y $A = \begin{bmatrix} a^1 & \dots & a^n\end{bmatrix}$, $Q = \begin{bmatrix} q^1 & \dots & q^m\end{bmatrix}$, entonces

$$span\{a^1, \dots, a^k\} = span\{q^1, \dots, q^k\}$$

para $k = 1, \dots, n$. En particular, si $Q = \begin{bmatrix} Q_1 & Q_2 \end{bmatrix}$ donde $Q_1 \in \mathbb{R}^{m \times n}$ y $Q_2 \in \mathbb{R}^{m \times (m-n)}$, entonces $A = Q_1 R_1$ donde $R_1 \in \mathbb{R}^{n \times n}$ y $R = \begin{bmatrix} R_1 \\ 0 \end{bmatrix}$.

---

## Demostración:
Comparando columnas se obtiene que si $1 \le j \le n$, entonces:
$$a^j = Q r^j = \begin{bmatrix} q^1 & \dots & q^n \end{bmatrix} \begin{bmatrix} r_{1j} \\ \vdots \\ r_{jj} \\ 0 \\ \vdots \\ 0 \end{bmatrix} = \sum_{i=1}^j r_{ij} q^i \in span\{q^1, \dots, q^j\}$$
luego $span\{a^1, \dots, a^n\} \subseteq span\{q^1, \dots, q^n\}$. Como $A$ tiene rango $n$, entonces $q^1, \dots, q^n$ son linealmente independientes, por lo tanto
$$span\{a^1, \dots, a^n\} = span\{q^1, \dots, q^n\}$$

---

## Demostración (continuación):

Por otro lado,
$$A = QR = \begin{bmatrix} Q_1 & Q_2 \end{bmatrix} \begin{bmatrix} R_1 \\ 0 \end{bmatrix} = Q_1 R_1$$

y luego $Im(A) = Im(Q_1)$. $\blacksquare$

Se dice que $A = Q_1R_1$ es la **Descomposición QR Reducida** de $A$. Bajo ciertas hipótesis es única.

---

# Teorema
Sea $A \in \mathbb{R}^{m \times n}$ de rango $n$. Entonces la descomposición QR reducida $A = Q_1 R_1$ es única si $Q_1$ tiene columnas ortonormales y $R_1$ tiene diagonal estrictamente positiva. Más aún, $R_1$ es el factor de Cholesky de $A^T A$.

## Demostración:
Como $A = Q_1 R_1$ con columnas ortonormales y $R_1$ triangular superior con diagonal positiva, entonces
$$A^T A = R_1^T Q_1^T Q_1 R_1 = R_1^T R_1$$
Como $R_1$ es triangular superior con diagonal positiva, es el factor de Cholesky de $A^T A$. Además, $Q_1 = A R_1^{-1}$ también es única. $\blacksquare$

---

# Entonces, cómo resolvemos Cuadrados Mínimos?

Realizamos la descomposición QR de $A \in \mathbb{R}^{m \times n}$. Si $A$ es de rango $n$, entonces:

$$ Q^T A = \begin{bmatrix} R_1 \\ 0 \end{bmatrix} \quad \text{y} \quad Q^T b = \begin{bmatrix} Q_1^T b \\ Q_2^T b \end{bmatrix} = \begin{bmatrix} c \\ d \end{bmatrix} $$

donde $R_1 \in \mathbb{R}^{n \times n}$ es triangular superior con diagonal estrictamente positiva, $c \in \mathbb{R}^n$ y $d \in \mathbb{R}^{m-n}$. Entonces,

$$
\begin{aligned}
\min_{x} \|Ax - b\|_2^2 &= \min_{x} \|Q^T (Ax - b)\|_2^2 = \\
= \min_{x} \left\| \begin{bmatrix} R_1 \\ 0 \end{bmatrix} x - \begin{bmatrix} c \\ d \end{bmatrix} \right\|_2^2  &= \min_{x} \|R_1 x - c\|_2^2 + \|d\|_2^2
\end{aligned}
$$

Finalmente, si $R \hat{x} = c$ , entonces $\hat{x}$ resuelve el problema de cuadrados mínimos y $\min_x \|Ax - b\|_2^2 = \|d\|_2^2$. **:D**

---

# Algoritmo **(Cuadrados Mínimos por QR)**

**Entrada:** $A \in \mathbb{R}^{m \times n}, b \in \mathbb{R}^m$. **Salidas:** $x \in \mathbb{R}^n$ y residuo mínimo $r_2 = \|Ax - b\|_2$.
- $Q, R = descomposicion\_QR(A)$
- $q = Q^T b$
- Definir $p = max\{i: r_{ii} \ne 0\}$
- Definir $\mathcal{I} = \{1, \dots, p\}, \ \mathcal{J} = \{1, \dots, n\} - \mathcal{I}$
- $y_{\mathcal{I}} = sol\_trsup(R_{\mathcal{I}, \mathcal{I}}, q_{\mathcal{I}})$ y definir $x = \begin{bmatrix} y_{\mathcal{I}} \\ 0 \end{bmatrix}$

**Retornar:** $x$ y $r_2 = \|q_{\mathcal{J}}\|_2$

---

# Teorema (Estabilidad de Givens y Householder)

Cuando la factorización QR se calcula utilizando una secuencia de transformaciones de Householder o Givens en aritmética de punto flotante, los factores calculados $\hat{Q}$ y $\hat{R}$ son los factores ortogonal y triangular superior exactos para una matriz ligeramente perturbada $A + \delta A$. El tamaño de la perturbación es pequeño y está acotado por: 

$$\frac{|\delta A|}{|A|} = O(\epsilon_{\text{maquina}}).$$

:heart:
---

---
# LU vs. QR

| Característica | Descomposición LU | Descomposición QR |
| :--- | :--- | :--- |
| **Caso de uso** | Sistemas cuadrados: $Ax=b$ | Mínimos cuadrados: $Ax \approx b$ |
| **Aplicabilidad** | Matriz $A$ **cuadrada**. | Matriz $A \in \mathbb{R}^{m \times n}$ de rango de columnas completo. |
| **Estabilidad numérica** | Inestable sin pivoteo, pero hay casos patológicos | **Inherentemente estable** (matrices ortogonales) |
| **Costo computacional** |  $\frac{2}{3}n^3$ flops. |  $\frac{4}{3}n^3$ flops. |

---

# Acaso hay algo mejor que QR? :heart:

- Es más estable y permite "solucionar" sistemas lineales de dimensión $m \times n$
- Tenemos una sola contra: necesitamos tener $rank(A) = n$. Esto se puede llegar a evitar intercambiando columnas pero nadie lo hace...
- Existe una descomposición que permite resolver cuadrados mínimos con matrices singulares y es uno de los mayores descubrimientos del álgebra lineal numérica, la ciencia de datos y el machine learning.
- Igualmente no nos olvidemos de QR, la vamos a volver a ver más adelante.
