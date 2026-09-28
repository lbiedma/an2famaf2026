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
## Clase 13: Iteración QR para Autovalores
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Motivación: De las potencias a la versión matricial

El **método de las potencias** halla autovalores y autovectores de a uno, pero requiere:
- Iniciar con un $q^0$ con coordenada no nula en la dirección dominante.

**Idea clave:**
- Si $Q \in \mathbb{R}^{n \times n}$ es ortogonal, sus columnas generan $\mathbb{R}^n$.
- Alguna columna de $Q$ tiene coordenada no nula en la dirección dominante.
- En vez de correr potencias por columna, consideramos una **versión matricial**:

$$
\begin{aligned}
\text{Potencia:}& \quad z^k = A q^{k-1} \quad\longrightarrow\quad Z_k = A Q_{k-1} \quad (Q_0 \text{ ortogonal}) \\
\text{Escalado:}& \quad q^k = z^k / \sigma_k \quad\longrightarrow\quad \text{Preservar } \operatorname{Im}(Z_k) \text{ con } Q_k \text{ ortogonal}
\end{aligned}
$$

El escalado matricial se obtiene con la descomposición QR: $Z_k = Q_k R_k$.

---

# Método de iteraciones ortogonales

**Esquema iterativo:**
0. Dar $Q_0 \in \mathbb{R}^{n \times n}$ ortogonal y $k = 1$.
1. Definir $Z_k = A Q_{k-1}$.
2. Obtener $Q_k, R_k$ tal que $Q_k R_k = Z_k$ con la descomposición QR de $Z_k$.
3. Hacer $k \leftarrow k + 1$ y regresar al paso 1.

**Propiedades:**
- Genera sucesiones $\{Q_k\}$ ortogonales y $\{R_k\}$ triangulares superiores:
  $$
  R_k = Q_k^T Z_k = Q_k^T A Q_{k-1}
  $$
- Como $\|Q_k\|_2 = 1$, tomando subsucesiones se obtiene que $R_k$ converge a $Q^T A \hat{Q}$ triangular superior, donde $Q$ y $\hat{Q}$ son puntos límite de $Q_k$ y $Q_{k-1}$.

---

# La sucesión $T_k$ y el obstáculo del espectro real

Si en el método de iteraciones ortogonales definimos:
$$
T_k = Q_k^T A Q_k
$$
Tomando límite se obtendría $T = Q^T A Q$ con $Q$ ortogonal. Si $T$ fuera triangular superior, **sus autovalores estarían en la diagonal**.

> **Obstáculo fundamental:**
> Una matriz $A \in \mathbb{R}^{n \times n}$ **no necesariamente tiene todos sus autovalores reales**.
> En $\mathbb{R}$, no siempre existe una matriz semejante que sea triangular superior pura.

---

# Teorema: Descomposición de Schur (en $\mathbb{C}$)

Si $A \in \mathbb{C}^{n \times n}$, existe $Q \in \mathbb{C}^{n \times n}$ unitaria tal que:
$$
T = Q^* A Q \quad \text{es triangular superior.}
$$

**Demostración (Inducción en $n$):**
- **Base ($n=1$):** Inmediato ($A = a \in \mathbb{C}$, tomando $Q = 1 \implies T = a$).
- **Paso inductivo:** Sea $(\lambda, v)$ con $A v = \lambda v$, $\|v\|_2 = 1$.
  Por Gram–Schmidt completamos $v$ a una base ortonormal $U = [v \quad V] \in \mathbb{C}^{n \times n}$ unitaria:
  $$
  U^* A U = \begin{bmatrix} v^* \\ V^* \end{bmatrix} [A v \quad A V] = \begin{bmatrix} \lambda & w^* \\ 0 & B \end{bmatrix}
  $$
  donde $w^* = v^* A V \in \mathbb{C}^{1 \times (n-1)}$ y $B = V^* A V \in \mathbb{C}^{(n-1) \times (n-1)}$.

---

## Demostración del Teorema de Schur (cont.)

- Por hipótesis inductiva sobre $B$, existe $\tilde{U} \in \mathbb{C}^{(n-1) \times (n-1)}$ unitaria tal que $\tilde{U}^* B \tilde{U} = \tilde{T}$ es triangular superior.
- Definimos la matriz unitaria:
  $$
  Q = U \begin{bmatrix} 1 & 0 \\ 0 & \tilde{U} \end{bmatrix} \in \mathbb{C}^{n \times n}
  $$
- Efectuando el producto por bloques:
  $$
  Q^* A Q = \begin{bmatrix} 1 & 0 \\ 0 & \tilde{U}^* \end{bmatrix} \begin{bmatrix} \lambda & w^* \\ 0 & B \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & \tilde{U} \end{bmatrix} = \begin{bmatrix} \lambda & w^* \tilde{U} \\ 0 & \tilde{T} \end{bmatrix} = T
  $$
  que es triangular superior. $\blacksquare$

---

# De iteraciones ortogonales a iteraciones QR

Queremos generar $T_k = Q_k^* A Q_k$ sin arrastrar las matrices de la iteración ortogonal:

1. **Por un lado:**
   $$
   T_{k-1} = Q_{k-1}^* A Q_{k-1} = Q_{k-1}^* Z_k = Q_{k-1}^* (Q_k R_k) = (Q_{k-1}^* Q_k) R_k
   $$
   Como $U_k = Q_{k-1}^* Q_k$ es unitaria y $R_k$ es triangular superior:
   $$
   \boxed{T_{k-1} = U_k R_k \quad \text{es la descomposición QR de } T_{k-1}}
   $$

2. **Por otro lado:**
   $$
   T_k = Q_k^* A Q_k = Q_k^* A Q_{k-1} (Q_{k-1}^* Q_k) = Q_k^* Z_k U_k = (Q_k^* Q_k R_k) U_k = \boxed{R_k U_k}
   $$

> Para pasar de $T_{k-1}$ a $T_k$: calculamos la QR de $T_{k-1}$ y multiplicamos los factores al revés.

---

## Método de Iteraciones QR

**Esquema iterativo:**
1. Dar $U_0$ unitaria, definir $T_0 = U_0^* A U_0$ (típicamente $U_0 = I \implies T_0 = A$) y $k = 1$.
2. Obtener $U_k, R_k$ tal que $U_k R_k = T_{k-1}$ con la descomposición QR de $T_{k-1}$.
3. Definir $T_k = R_k U_k$.
4. Hacer $k \leftarrow k + 1$ y regresar al paso 1.

**Propiedades:**
- **Semejanza unitaria:** $T_k = R_k U_k = U_k^* T_{k-1} U_k = \dots = Q_k^* A Q_k$, donde $Q_k = U_0 U_1 \cdots U_k$.
- Si $|\lambda_1| > |\lambda_2| > \dots > |\lambda_n|$, $\{T_k\}$ converge a una matriz $T$ **triangular superior** con los autovalores en la diagonal.
- No requiere almacenar $\{Q_k\}$ ni calcular potencias explícitas.

---

# Algoritmo QR en código y relación con $A^k$

```python
T = A.copy()
for k in range(num_iter):
    U, R = np.linalg.qr(T)
    T = R @ U
```

**Relación con potencias $A^k$:**
Definiendo $\tilde{Q}_k = U_1 U_2 \cdots U_k$ y $\tilde{R}_k = R_k R_{k-1} \cdots R_1$:
$$
A^k = \tilde{Q}_k \tilde{R}_k
$$
- La iteración QR produce la misma sucesión de factores $R$ que la iteración ortogonal iniciada con $Q_0 = I$.
- El algoritmo genera implícitamente la descomposición QR de la potencia $A^k$.

---

# Teorema: Descomposición de Schur en $\mathbb{R}$

Si $A \in \mathbb{R}^{n \times n}$, existe $Q \in \mathbb{R}^{n \times n}$ ortogonal tal que:
$$
Q^T A Q = \begin{bmatrix}
R_{11} & R_{12} & \cdots & R_{1s} \\
0 & R_{22} & \cdots & R_{2s} \\
\vdots & \ddots & \ddots & \vdots \\
0 & \cdots & 0 & R_{ss}
\end{bmatrix}
$$
donde cada bloque diagonal $R_{ll}$ es:
- $R_{ll} \in \mathbb{R}^{1 \times 1}$: autovalor real de $A$.
- $R_{ll} \in \mathbb{R}^{2 \times 2}$: con autovalores complejos conjugados $(\lambda, \bar{\lambda})$.

La matriz $Q^T A Q$ es **cuasi-triangular superior** (o forma de Schur real).

---

# Demostración de Schur Real (Idea)

Inducción en el número $k$ de pares de autovalores complejos conjugados:
- Si $\lambda = \gamma + i\mu \in \mathbb{C}$ ($\mu \neq 0$) tiene autovector $y + i z \neq 0$ con $y, z \in \mathbb{R}^n$:
  $$
  A(y + i z) = (\gamma + i\mu)(y + i z) = \gamma y - \mu z + i(\mu y + \gamma z)
  $$
- Agrupando parte real e imaginaria:
  $$
  A [y \quad z] = [y \quad z] \begin{bmatrix} \gamma & \mu \\ -\mu & \gamma \end{bmatrix} = [y \quad z] S
  $$
- Los vectores $y, z$ son **linealmente independientes** en $\mathbb{R}^n$.

---

## Continuación...
- Factorizando $[y \quad z] = \hat{Q} \begin{bmatrix} \hat{R} \\ 0 \end{bmatrix}$ (QR con $\hat{R} \in \mathbb{R}^{2 \times 2}$ no singular):
  $$
  \hat{Q}^T A \hat{Q} = \begin{bmatrix} \hat{R}_{11} & \hat{R}_{12} \\ 0 & \hat{R}_{22} \end{bmatrix} \quad \text{con } \hat{R}_{11} = \hat{R} S \hat{R}^{-1}
  $$
- Los autovalores de $\hat{R}_{11}$ son $\gamma \pm i\mu$. Se aplica hipótesis inductiva sobre $\hat{R}_{22}$.

---

# Matrices Hessenberg Superior

**Definición:** Se dice que $H \in \mathbb{R}^{n \times n}$ es una matriz **Hessenberg superior** si:
$$
h_{ij} = 0 \quad \text{para todo } i > j + 1
$$

Una matriz Hessenberg superior $5 \times 5$ tiene la siguiente estructura:
$$
H = \begin{bmatrix}
h_{11} & h_{12} & h_{13} & h_{14} & h_{15} \\
h_{21} & h_{22} & h_{23} & h_{24} & h_{25} \\
0 & h_{32} & h_{33} & h_{34} & h_{35} \\
0 & 0 & h_{43} & h_{44} & h_{45} \\
0 & 0 & 0 & h_{54} & h_{55}
\end{bmatrix}
$$

> La descomposición de Schur en los reales nos garantiza que $Q^T A Q$ es Hessenberg superior (más aún, cuasi-triangular).

---

# Iteración QR en $\mathbb{R}$ con Matrices Hessenberg

El método de iteraciones QR en $\mathbb{R}$ para $A \in \mathbb{R}^{n \times n}$ opera directamente sobre una forma Hessenberg semejante:

**Esquema:**
1. Dar $Q_0$ ortogonal, definir $H_0 = Q_0^T A Q_0$ (Hessenberg superior) y $k = 1$.
2. Obtener $Q_k, R_k$ tal que $Q_k R_k = H_{k-1}$ mediante la descomposición QR de $H_{k-1}$.
3. Definir $H_k = R_k Q_k$.
4. Hacer $k \leftarrow k + 1$ y regresar al paso 1.

> Este procedimiento **preserva estructura Hessenberg superior** en cada iteración $k$.

---

# Teorema: Preservación de la estructura Hessenberg

Si $H \in \mathbb{R}^{n \times n}$ es Hessenberg superior y no singular con $H = QR$ su descomposición QR, entonces $\tilde{H} = RQ$ es Hessenberg superior.

**Demostración:** Como $H$ es no singular, $R$ es no singular $\implies r_{ii} \ne 0 \ \forall i$.
- Analizando la columna $j$ de $H = QR$:
  $$
  \begin{bmatrix} h_{1j} \\ \vdots \\ h_{j+1, j} \\ 0 \\ \vdots \\ 0 \end{bmatrix}
  = Q \begin{bmatrix} r_{1j} \\ \vdots \\ r_{jj} \\ 0 \\ \vdots \\ 0 \end{bmatrix}
  = \sum_{l=1}^j r_{lj} \begin{bmatrix} q_{1l} \\ \vdots \\ q_{l+1, l} \\ q_{l+2, l} \\ \vdots \\ q_{nl} \end{bmatrix}
  $$

---

## Demostración (cont.)
- Para $j = 1 \implies q_{i1} = 0$ para $i = 3, \dots, n$.
- Siguiendo por inducción hasta $j = n \implies q_{ij} = 0$ para $i \ge j + 2$. Concluyendo que **$Q$ es Hessenberg superior**.

- Analizando las columnas de $\tilde{H} = RQ$, la columna $j$ es:
  $$
  \begin{bmatrix} \tilde{h}_{1j} \\ \vdots \\ \tilde{h}_{j+1, j} \\ \tilde{h}_{j+2, j} \\ \vdots \\ \tilde{h}_{nj} \end{bmatrix}
  = R \begin{bmatrix} q_{1j} \\ \vdots \\ q_{j+1, j} \\ 0 \\ \vdots \\ 0 \end{bmatrix}
  = \sum_{l=1}^{j+1} q_{lj} \begin{bmatrix} r_{1l} \\ \vdots \\ r_{ll} \\ 0 \\ \vdots \\ 0 \end{bmatrix}
  $$

---
## Demostración (cont.)

- Como $R$ es triangular superior ($r_{il} = 0$ para $i > l$), para cada $l \le j + 1$ los términos $r_{il}$ son cero para $i \ge j + 2$.
- Por lo tanto, $\tilde{h}_{ij} = 0$ para $i \ge j + 2$, concluyendo que **$\tilde{H}$ es Hessenberg superior**. $\blacksquare$

> Si iniciamos con $H_0 = Q_0^T A Q_0$ Hessenberg, todas las matrices de la sucesión $\{H_k\}$ son Hessenberg superior.

---

# Reducción a Hessenberg usando Householder

Para reducir $A$ a Hessenberg superior mediante semejanzas ortogonales ($H_0 = Q_0^T A Q_0$):
- Se aplican reflexiones de Householder para anular los elementos debajo de la subdiagonal en cada columna $j = 1, \dots, n-2$:
  $$
  V_j = I - \frac{2}{\|u^j\|_2^2} u^j (u^j)^T, \quad
  V_j^T \begin{bmatrix} a_{1j} \\ \vdots \\ a_{j+1, j} \\ a_{j+2, j} \\ \vdots \\ a_{nj} \end{bmatrix}
  = \begin{bmatrix} a_{1j} \\ \vdots \\ \tilde{a}_{j+1, j} \\ 0 \\ \vdots \\ 0 \end{bmatrix}
  $$

---

- Como los primeros $j$ elementos quedan invariantes, la multiplicación por derecha $V_j$ preserva los ceros creados:
  $$
  V_1^T A V_1 = \begin{bmatrix} * & * & * & * & * \\ * & * & * & * & * \\ 0 & * & * & * & * \\ 0 & * & * & * & * \\ 0 & * & * & * & * \end{bmatrix}, \quad
  V_2^T V_1^T A V_1 V_2 = \begin{bmatrix} * & * & * & * & * \\ * & * & * & * & * \\ 0 & * & * & * & * \\ 0 & 0 & * & * & * \\ 0 & 0 & * & * & * \end{bmatrix}
  $$
- Tras $n-2$ pasos: $H_0 = V_{n-2}^T \cdots V_1^T A V_1 \cdots V_{n-2} = Q_0^T A Q_0$, con $Q_0 = V_1 \cdots V_{n-2}$.

---

# Algoritmo *(Reducción a Hessenberg con Householder)*

**Entrada:** $A \in \mathbb{R}^{n \times n}$. **Salidas:** $H, Q \in \mathbb{R}^{n \times n}$ t.q. $H = Q^T A Q$.

1. Definir $Q = I$.
2. Para $j = 1, \dots, n - 2$:
   - Definir $\mathcal{I} = \{j+1, \dots, n\}$, $\mathcal{J} = \{j, \dots, n\}$.
   - Obtener $u, \rho$ aplicando reflexión de Householder al vector $A_{\mathcal{I} j}$.
   - Definir $w = \rho u$.
   - Actualizar bloques por izquierda y por derecha:
     $$
     \begin{aligned}
     A_{\mathcal{I} \mathcal{J}} &\leftarrow A_{\mathcal{I} \mathcal{J}} - w (u^T A_{\mathcal{I} \mathcal{J}}), \\
     A_{* \mathcal{I}} &\leftarrow A_{* \mathcal{I}} - A_{* \mathcal{I}} w u^T, \\
     Q_{* \mathcal{I}} &\leftarrow Q_{* \mathcal{I}} - Q_{* \mathcal{I}} w u^T.
     \end{aligned}
     $$
3. Retornar $H = A$ y $Q$.

---

# Factorización QR de Hessenberg

Cada columna $j$ de una matriz Hessenberg superior tiene **un único elemento no nulo bajo la diagonal** ($h_{j+1, j}$), por lo que su descomposición QR requiere **$n - 1$ rotaciones de Givens** $G_{j+1, j}$:

$$
  R_k = G_{n, n-1} \cdots G_{32} G_{21} H_{k-1}
$$
- La matriz ortogonal es $Q_k = G_{21}^T G_{32}^T \cdots G_{n, n-1}^T$.
- El nuevo paso de la iteración $H_k = R_k Q_k$ se obtiene multiplicando por derecha:
  $$
  H_k = R_k G_{21}^T G_{32}^T \cdots G_{n, n-1}^T
  $$

> **Eficiencia computacional:**
> - Descomposición QR para matriz densa general: $\mathcal{O}(n^3)$ operaciones.
> - Descomposición QR y $RQ$ para Hessenberg: $\mathbf{\mathcal{O}(n^2)}$ operaciones.

---

# Algoritmo *(Método de Iteraciones QR con Givens)*

**Entradas:** $A \in \mathbb{R}^{n \times n}$ y $m \in \mathbb{N}$. **Salidas:** $H, Q \in \mathbb{R}^{n \times n}$ t.q. $H = Q^T A Q$.

1. $H, Q = \text{QR\_Householder}(A)$
2. Para $k = 1, \dots, m$:
   - **(a) Factorización QR:** Para $j = 1, \dots, n - 1$:
     - Definir $\mathcal{I} = \{j, j + 1\}$, $\mathcal{J} = \{j, \dots, n\}$.
     - Calcular $G_j = \text{Givens}(H_{jj}, H_{j+1, j})$.
     - $H_{\mathcal{I} \mathcal{J}} \leftarrow G_j H_{\mathcal{I} \mathcal{J}}$.
   - **(b) Formación de $RQ$ y acumulación:** Para $l = 1, \dots, n - 1$:
     - Definir $\mathcal{I} = \{l, l + 1\}$.
     - $H_{* \mathcal{I}} \leftarrow H_{* \mathcal{I}} G_l^T$, $Q_{* \mathcal{I}} \leftarrow Q_{* \mathcal{I}} G_l^T$.
3. Retornar $H$ y $Q$.

---

# Implementación Práctica del Método QR

- **Convergencia:**
  - La sucesión $\{H_k\}$ converge a una matriz Hessenberg cuasi-triangular con bloques $1 \times 1$ (autovalores reales) y $2 \times 2$ (pares complejos conjugados).
- **Desplazamientos (*shifts*):**
  - Para acelerar la velocidad de convergencia (de lineal a cuadrática o cúbica), se utiliza la iteración con desplazamientos $\mu_k$:
    $$
    H_{k-1} - \mu_k I = Q_k R_k \implies H_k = R_k Q_k + \mu_k I
    $$
  - Desplazamiento de Rayleigh o doble desplazamiento de Francis.
- **Deflación:**
  - Si $|h_{j+1, j}| \le \text{tol}$, se anula a cero y el problema se desacopla en dos subproblemas independientes.
