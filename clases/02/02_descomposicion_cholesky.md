---
marp: true
theme: default
paginate: true

---
# Análisis Numérico II / Álgebra Lineal Numérica
## Clase 02: Descomposición de Cholesky
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Sistemas (Semi) Definidos Positivos

**Definición**: Un sistema lineal $Ax=b$ con $A \in \mathbb{R}^{n \times n}$ es __simétrica__ (semi) __definida positiva__ (SDP) si $A^T = A$ y $x^T A x (\ge)\gt 0$ para todo $x \in \mathbb{R}^n$, $x \ne 0$.

**Teorema:** Si $A$ es SDP, entonces todos sus autovalores son positivos y por lo tanto $A$ es invertible.

**Demostración:** Sea $v \ne 0$ autovector de $A$ con autovalor $\lambda$. Entonces $Av = \lambda v$. Multiplicando por la izquierda por $v^T$ se tiene $v^T A v = \lambda v^T v$. Como $A$ es SDP, $v^T A v > 0$, y como $v \ne 0$, $v^T v > 0$. Por lo tanto $\lambda > 0$.

---

# **Proposición:** Si $A \in \mathbb{R}^{n \times n}$ es SDP entonces:
i. $a_{ii} > 0$ para todo $i=1,\dots,n$.
ii. Las submatrices principales $A_k = \begin{bmatrix} a_{11} & \dots & a_{1k} \\ \vdots & \ddots & \vdots \\ a_{k1} & \dots & a_{kk} \end{bmatrix}$ son SDP para $k=1,\dots,n$.
iii. Si $X \in \mathbb{R}^{n \times m}$ con $rank(X)=m$, entonces $X^T A X$ es SDP.

**PIZARRÓN**

---

# **Demostración:**
i. Tomo $e^i$ vector canónico de $\mathbb{R}^n$ ($e^i = \begin{bmatrix} 0, \dots, 0, 1, 0, \dots, 0 \end{bmatrix}^T$, con $1$ en la posición $i$)

$A e^i = \begin{bmatrix} a^1 \dots a^n \end{bmatrix} \begin{bmatrix} 0 \\ . \\ 1 \\ . \\ 0 \end{bmatrix} = 0 a^1 + 0 a^2 + \dots + 1 a^i + \dots + 0 a^n = a^i$.

Entonces, $(e^i)^T A e^i = (e^i)^T a^i = a_{ii} > 0$ para todo $i=1,\dots,n$.

---

# **Demostración:**

ii. Sea $E_k = \begin{bmatrix} e^1 & \dots & e^k \end{bmatrix} = \begin{bmatrix} I_{k \times k} \\ 0_{(n-k) \times k} \end{bmatrix}$. 
Entonces, si $\mathcal{I} = \{1,\dots,k\}$ y $\mathcal{J} = \{k+1,\dots,n\}$,

$A_k = E_k^T A E_k = \begin{bmatrix} I_{k \times k} & 0_{k \times (n-k)} \end{bmatrix} \begin{bmatrix} A_{\mathcal{I}\mathcal{I}} & A_{\mathcal{I}\mathcal{J}} \\ A_{\mathcal{J}\mathcal{I}} & A_{\mathcal{J}\mathcal{J}} \end{bmatrix} \begin{bmatrix} I_{k \times k} \\ 0_{(n-k) \times k} \end{bmatrix} = A_{\mathcal{I}\mathcal{I}}$.

Ahora, si $y \in \mathbb{R}^k$, $y \ne 0$, entonces $x = E_k y \ne 0$ y $x^T A x = y^T E_k^T A E_k y = y^T A_k y > 0$, con lo que $A_k$ es SDP.

iii. se hace en el Práctico :D

---
# **Datos Útiles de Álgebra III**

Hay un par de cosas super importantes que no vamos a demostrar y asumimos sabidas.

1. Todos los autovalores de una matriz simétrica real son reales.
2. Una matriz simétrica es ORTOGONALMENTE DIAGONALIZABLE, ie. existe $Q \in \mathbb{R}^{n \times n}$ matriz ortogonal (columnas ortogonales entre sí) tal que $Q^T A Q = D$ es diagonal con los autovalores de $A$.

---
# Descomposición de Cholesky

- Supongamos que queremos resolver $Ax = b$ con $A \in \mathbb{R}^{n \times n}$ que es **simétrica** y **definida positiva**.
- Buscaremos una matriz $G \in \mathbb{R}^{n \times n}$ **triangular superior** tal que se cumpla la igualdad $A = G^T G$.
- Si pudiera obtener $G$, entonces $Ax = G^T G x = b$.
- Resolvamos en dos pasos: primero resolvemos $G^T y = b$ y luego $Gx = y$. Como $G$ es triangular superior, ambos sistemas son fáciles de resolver (por sustitución!).
- Existe esta descomposición? **SI!** y es **ÚNICA**!

---

# **Teorema** (Existencia y Unicidad de Cholesky)

Sea $A \in \mathbb{R}^{n \times n}$ simétrica y definida positiva.

Entonces existe una **única** matriz $G \in \mathbb{R}^{n \times n}$ triangular superior con elementos diagonales positivos tal que $A = G^T G$.

**PIZARRÓN**
Demostración en [Notas ALN Damián Fernandez (Teorema 2.7)](https://drive.google.com/file/d/10h9BvK-P0b4l9-1D7G2T4Q1R9sX6u5M9/view?usp=sharing)

---

# **Demostración** (Existencia)

Usamos inducción en $n$.

**Caso Base:**

Si $n=1$, $A = [a_{11}]$. Como $A$ es SDP, $a_{11} > 0$. Entonces $G = [\sqrt{a_{11}}]$ es la descomposición de Cholesky.

**Hipótesis Inductiva:**

Supongamos que el teorema es válido para matrices de tamaño $n-1$. Es decir, toda matriz $(n-1)\times(n-1)$ simétrica y definida positiva tiene una única descomposición de Cholesky.

**Paso Inductivo:**

Consideremos $A \in \mathbb{R}^{n \times n}$ simétrica y definida positiva.

--- 

# **Demostración** (Unicidad)

--- 

# Algoritmo de Cálculo (Producto Interior)

- El **Algoritmo 6** describe cómo obtener $G$ fila por fila utilizando productos internos [6].
- El proceso define iterativamente cada elemento de la diagonal como $G_{ii} = \sqrt{A_{ii} - \sum_{k=1}^{i-1} G_{ki}^2}$ [7].
- Para que el algoritmo sea correcto, es imperativo controlar que la entrada diagonal sea **positiva** antes de extraer la raíz cuadrada [7].
- Si durante la ejecución se encuentra una entrada diagonal no positiva, se deduce que la matriz original **no es definida positiva** y el proceso debe detenerse [7].

---

# Aplicación y Costo Computacional

- La principal aplicación es resolver sistemas lineales $Ax = b$ descomponiendo el problema en dos sistemas triangulares: $G^T y = b$ y $Gx = y$ [2, 8].
- Este método es fundamental en ingeniería y física, por ejemplo, para modelar la **distribución de temperatura** en una placa de acero [8, 9].
- El costo operacional de la descomposición de Cholesky es de aproximadamente **$O(n^3/3)$ flops** [10].
- En términos de eficiencia, este algoritmo requiere aproximadamente la **mitad de operaciones** que una descomposición LU estándar [10, 11].
