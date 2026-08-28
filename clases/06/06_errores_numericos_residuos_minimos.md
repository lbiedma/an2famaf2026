---
marp: true
theme: default
paginate: true

---

# Análisis Numérico II / Álgebra Lineal Numérica
## Clase 06: Errores Numéricos y Residuos Mínimos
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Definición de Norma

**Definición 3.1 (Norma):** Una norma en un espacio vectorial $X$ es una función $\|\cdot\|: X \to \mathbb{R}$ que satisface, para todo $x, y \in X$ y todo escalar $\alpha \in \mathbb{R}$:

1. **Positividad y No Degeneración:** $\|x\| \ge 0 \quad \text{y} \quad \|x\| = 0 \iff x = 0 \quad$
2. **Propiedad Subaditiva (Desigualdad Triangular):** $\|x + y\| \le \|x\| + \|y\| \quad$
3. **Homogeneidad Absoluta:** $\|\alpha x\| = |\alpha| \|x\| \quad$

Para Normas Matriciales, se agrega:

4. **Submultiplicatividad:** $\|AB\| \le \|A\| \|B\| \quad$

---

# Otros Ejemplos de Normas Vectoriales

1. Si $A \in R^{n \times n}$ es SDP, entonces $\| x \|_A = \sqrt{x^T A x}$ es una norma en $R^n$.
2. Si $B \in R^{m \times n}$ tiene rango completo $n$ y $\| . \|$ es una norma en $R^m$, entonces $\| x \|_B = \| B x \|$ es una norma en $R^n$.
3. Dada una norma $\| . \|$ se define la norma dual como $\| y \|_* = \sup_{x \ne 0} \frac{x^T y}{\| x \|}$. En particular, $\| . \|_p$ y $\| . \|_q$ son normas duales si $\frac{1}{p} + \frac{1}{q} = 1$.
    - $\| . \|_\infty$ y $\| . \|_1$ son normas duales.
    - $\| . \|_2$ y $\| . \|_2$ son normas duales.

---

# Número de Condición $\kappa(A)$

**Definición:** Para una matriz no singular $A \in \mathbb{R}^{n \times n}$, su __número de condición__ es:
$$\kappa(A) = \|A\| \|A^{-1}\| $$

### Interpretación Geométrica
Como $\|A^{-1}\| = 1 / \min_{\|x\|=1} \|Ax\|$, el número de condición mide la relación entre la distorsión máxima y mínima de la esfera unidad bajo $A$:
$$\kappa(A) = \frac{\max_{\|x\|=1} \|Ax\|}{\min_{\|x\|=1} \|Ax\|} $$

---

# Ejemplo Numérico de Mal Condicionamiento

Considere la matriz $A \in \mathbb{R}^{2 \times 2}$ y su inversa:
$$A = \begin{bmatrix} 1000 & 999 \\ 999 & 998 \end{bmatrix}, \quad A^{-1} = \begin{bmatrix} -998 & 999 \\ 999 & -1000 \end{bmatrix}$$

En norma infinito: $\|A\|_\infty = 1999$ y $\|A^{-1}\|_\infty = 1999$.
Por lo tanto, el número de condición es extremadamente alto:
$$\kappa_\infty(A) = 1999 \times 1999 = 3,996,001$$

### Consecuencia:
- El vector $x = [1, 1]^T$ es la dirección de máxima magnificación: $\|Ax\|_\infty = 1999 = \|A\|_\infty$.
- Un cambio infinitesimal en la dirección de mínima magnificación alterará drásticamente la solución.

---

# Sensibilidad de Sistemas Lineales

**Teorema (Perturbación en el término independiente $b$):** Sea $A \in \mathbb{R}^{n \times n}$ no singular y $b \neq 0$. Si $A\bar{x} = b$ y $A\hat{x} = b + \vartheta$, entonces:
$$\frac{\|\hat{x} - \bar{x}\|}{\|\bar{x}\|} \le \kappa(A) \frac{\|\vartheta\|}{\|b\|} $$

---

# Demostración:
Definiendo el error $\zeta = \hat{x} - \bar{x}$, restamos las ecuaciones y obtenemos $A\zeta = \vartheta \implies \zeta = A^{-1}\vartheta$. Tomando norma:
$$\|\zeta\| \le \|A^{-1}\| \|\vartheta\| $$

Por otro lado, como $b = A\bar{x}$, se cumple que $\|b\| \le \|A\| \|\bar{x}\|$, lo que equivale a $\frac{1}{\|\bar{x}\|} \le \frac{\|A\|}{\|b\|}$. Combinando ambas desigualdades:
$$\frac{\|\zeta\|}{\|\bar{x}\|} \le \|A^{-1}\| \|\vartheta\| \frac{\|A\|}{\|b\|} = \kappa(A) \frac{\|\vartheta\|}{\|b\|} \quad \blacksquare$$

---

# Invertibilidad Bajo Perturbaciones

Para analizar perturbaciones en la matriz del sistema, primero se requiere acotar la perturbación sobre la matriz identidad:

**Lema:** Si $F \in \mathbb{R}^{n \times n}$ cumple que $\|F\| < 1$, entonces $I - F$ es no singular y:
$$(I - F)^{-1} = \sum_{k=0}^\infty F^k, \quad \text{con} \quad \|(I - F)^{-1}\| \le \frac{1}{1 - \|F\|}$$

Esto nos permite analizar matrices arbitrarias no singulares bajo una perturbación $\Theta$:

---

# Continuamos

**Teorema:** Si $A$ es no singular y $\|A^{-1}\Theta\| < 1$, entonces $A + \Theta$ es no singular, cumpliéndose:
$$\|(A + \Theta)^{-1}\| \le \frac{\|A^{-1}\|}{1 - \|A^{-1}\Theta\|} $$

---

# Perturbaciones Simultáneas en $A$ y $b$

**Teorema:** Sea $A \in \mathbb{R}^{n \times n}$ no singular, $b \neq 0$ y $\|A^{-1}\Theta\| < 1$. Si $A\bar{x} = b$ y $(A + \Theta)\hat{x} = b + \vartheta$, entonces el error relativo está acotado por:

$$\frac{\|\hat{x} - \bar{x}\|}{\|\bar{x}\|} \le \frac{\kappa(A)}{1 - \kappa(A) \frac{\|\Theta\|}{\|A\|}} \left( \frac{\|\Theta\|}{\|A\|} + \frac{\|\vartheta\|}{\|b\|} \right)$$

### Significado del Denominador:
El término $1 - \kappa(A) \frac{\|\Theta\|}{\|A\|}$ en el denominador actúa como un factor de seguridad. Si la perturbación sobre la matriz $\Theta$ es lo suficientemente grande como para acercar la matriz a la singularidad, el denominador tiende a cero, haciendo que la cota de error crezca indefinidamente.

---

# Demostración

Sea el error de la solución $\zeta = \hat{x} - \bar{x}$. Sustituyendo y operando en el sistema perturbado:
$$(A + \Theta)(\bar{x} + \zeta) = b + \vartheta \implies A\zeta = \vartheta - \Theta\bar{x} - \Theta\zeta \implies \zeta = A^{-1}(\vartheta - \Theta\bar{x} - \Theta\zeta)$$

Tomando normas y aplicando la desigualdad triangular:
$$\|\zeta\| \le \|A^{-1}\| \left( \|\vartheta\| + \|\Theta\| \|\bar{x}\| + \|\Theta\| \|\zeta\| \right)$$

---

# Demostración (continuación)
Agrupando los términos con $\|\zeta\|$ a la izquierda de la desigualdad:
$$\left(1 - \|A^{-1}\| \|\Theta\|\right) \|\zeta\| \le \|A^{-1}\| \left( \|\Theta\| \|\bar{x}\| + \|\vartheta\| \right)$$

Dividiendo por $\|\bar{x}\|$ e introduciendo el término $\|A\|$ de manera conveniente:
$$\left(1 - \kappa(A) \frac{\|\Theta\|}{\|A\|}\right) \frac{\|\zeta\|}{\|\bar{x}\|} \le \kappa(A) \left( \frac{\|\Theta\|}{\|A\|} + \frac{\|\vartheta\|}{\|A\| \|\bar{x}\|} \right)$$

Dado que $\|b\| = \|A\bar{x}\| \le \|A\|\|\bar{x}\|$, se cumple $\frac{1}{\|A\|\|\bar{x}\|} \le \frac{1}{\|b\|}$. Al despejar, se verifica la cota del teorema. $\blacksquare$

---

# Recuento: Descomposición de Cholesky

Para sistemas lineales cuya matriz es **simétrica y definida positiva (SPD)**, disponemos de una herramienta eficiente:

- **El Teorema de Cholesky:** Garantiza que toda matriz SPD puede factorizarse de manera única como $A = G^T G$, donde $G$ es triangular superior con elementos diagonales positivos.
- **Eficiencia por Simetría:** Al explotar la estructura simétrica, el costo de Cholesky es de aproximadamente **$\frac{1}{3}n^3$ flops**.
- **Estabilidad Intrínseca:** El algoritmo es extremadamente estable ante errores de redondeo en punto flotante (*backward stable*), prescindiendo de estrategias de pivoteo.

---

# Recuento: Descomposición LU

Hasta ahora hemos estudiado la resolución de **sistemas de ecuaciones cuadrados** ($Ax = b$ con $A \in \mathbb{R}^{n \times n}$):

- **Eliminación Gaussiana:** Permite reducir la matriz a una forma triangular superior $U$ aplicando transformaciones de Gauss $M_k$.
- **Existencia y Unicidad:** La factorización $A = LU$ (con $L$ triangular inferior unitaria) existe y es única si y solo si todos los menores principales de $A$ son no singulares.
- **Pivoteo Parcial:** Ante pivotes nulos o muy pequeños, el intercambio de filas (permutación $PA = LU$) evita fallas y controla el error.
- **Costo Computacional:** El proceso de factorización requiere aproximadamente **$\frac{2}{3}n^3$ flops**.

---

# Recuento: Sensibilidad y Estabilidad Numérica

En la práctica computacional con aritmética de precisión finita (doble precisión, 64 bits), las soluciones exactas se ven afectadas por perturbaciones inevitables:

- **Propagación del Error:** Al resolver el sistema perturbado $(A+\Theta)\hat{x} = b+\vartheta$, el error relativo de la solución queda acotado por:
  $$\frac{\|\hat{x} - \bar{x}\|}{\|\bar{x}\|} \le \frac{\kappa(A)}{1 - \kappa(A)\frac{\|\Theta\|}{\|A\|}} \left( \frac{\|\Theta\|}{\|A\|} + \frac{\|\vartheta\|}{\|b\|} \right)$$
- **Número de Condición:** Definido como $\kappa(A) = \|A\|\|A^{-1}\|$, mide la sensibilidad del sistema. Un valor elevado de $\kappa(A)$ significa que pequeñas perturbaciones de redondeo destruirán la precisión de la solución calculada.

---

# El Problema de Residuos Mínimos

Con frecuencia, un sistema lineal $Ax = b$ con $A \in \mathbb{R}^{m \times n}$ y $b \in \mathbb{R}^m$ (particularmente cuando $m > n$, un sistema sobredeterminado) **no posee solución exacta**.

- En tales escenarios, la mejor opción consiste en hacer que el **vector residuo** $r(x) = b - Ax$ sea lo más pequeño posible en alguna norma:
  $$\min_{x \in \mathbb{R}^n} \|Ax - b\|$$
- Si elegimos medir este residuo bajo la norma Euclídea ($p=2$), el problema se conoce como **Cuadrados Mínimos**:
  $$\min_{x \in \mathbb{R}^n} \|Ax - b\|_2^2$$

---

# Resolución Analítica: Ecuaciones Normales

Definiendo la función objetivo diferenciable $f(x) = \frac{1}{2}\|Ax - b\|_2^2$ [182], buscamos su punto crítico igualando su gradiente a cero [21, 182]:

$$\nabla f(x) = A^T(Ax - b) = 0$$

Esto nos conduce de forma directa al célebre sistema lineal:
$$A^T A x = A^T b$$

- Este sistema es conocido como la **ecuación normal**.
- Si la matriz $A$ tiene rango completo $n$, la matriz $A^T A \in \mathbb{R}^{n \times n}$ es simétrica y definida positiva, lo que teóricamente permite resolver el sistema mediante la descomposición de Cholesky.

---

# Qué problemas podemos tener?

Aunque las ecuaciones normales son una herramienta fundamental desde el análisis teórico, **no se recomienda su uso como herramienta computacional directa**.

- **Efecto en el Número de Condición:** El número de condición de la matriz del sistema se eleva al cuadrado: $\kappa_2(A^T A) = (\kappa_2(A))^2$
- **Consecuencia de Precisión Finita:** Si una matriz $A$ está moderadamente mal condicionada (ej. $\kappa_2(A) = 10^4$), el sistema de ecuaciones normales amplificará drásticamente el error de redondeo en aritmética de doble precisión.
- Adicionalmente, el cálculo explícito del producto $A^T A$ puede provocar una pérdida catastrófica de información e independencia lineal en punto flotante.

---

# Descomposición QR

Para evitar construir la matriz $A^T A$, buscamos una transformación que reduzca el sistema preservando la norma Euclídea. Esto nos lleva a las **matrices ortogonales** $Q \in \mathbb{R}^{m \times m}$ ($Q^T Q = I$).

- Las matrices ortogonales **preservan la norma 2** [145]:
  $$\|Q v\|_2 = \|v\|_2 \quad \forall v \in \mathbb{R}^m \quad [145]$$
- El Teorema 4.3 garantiza que para cualquier matriz $A \in \mathbb{R}^{m \times n}$ existe una matriz ortogonal $Q$ y una triangular superior $R \in \mathbb{R}^{m \times n}$ tales que:
  $$A = QR$$

---

# Solución de Cuadrados Mínimos con QR

- En su **factorización QR reducida** (para rango completo $n$):
  $$A = Q_1 R_1$$
donde $Q_1 \in \mathbb{R}^{m \times n}$ tiene columnas ortonormales y $R_1 \in \mathbb{R}^{n \times n}$ es triangular superior.

Utilizando la propiedad de preservación de norma de la matriz ortogonal $Q^T$:

$$\|Ax - b\|_2^2 = \|Q^T(Ax - b)\|_2^2 = \|Q^T Ax - Q^T b\|_2^2$$

Particionando los bloques según las dimensiones del rango:
$$Q^T A = \begin{bmatrix} R_1 \\ 0 \end{bmatrix}, \quad Q^T b = \begin{bmatrix} c \\ d \end{bmatrix} \quad \text{con } R_1 \in \mathbb{R}^{n \times n}, \ c \in \mathbb{R}^n, \ d \in \mathbb{R}^{m-n}$$

---

La norma se reduce algebraicamente a:
$$\|Ax - b\|_2^2 = \left\| \begin{bmatrix} R_1 x - c \\ -d \end{bmatrix} \right\|_2^2 = \|R_1 x - c\|_2^2 + \|d\|_2^2$$

- El residuo mínimo se alcanza resolviendo el sistema triangular:
  $$R_1 \hat{x} = c$$
- El error mínimo absoluto es precisamente $\|d\|_2$.
- **Ventaja Numérica:** El condicionamiento de la matriz resultante es estable: $\kappa_2(R_1) = \kappa_2(A)$.
