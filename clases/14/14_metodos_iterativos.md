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
## Clase 14: Métodos Iterativos de Separación
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---


# Por qué Métodos Iterativos?

Para resolver sistemas lineales $Ax = b$ de gran dimensión, los **métodos directos** (descomposiciones matriciales) presentan limitaciones computacionales:

- **Pérdida de Dispersión:** Aunque $A$ sea una matriz rala o dispersa (con la gran mayoría de sus entradas nulas), los factores $L$ y $U$ suelen ser densos.
- **Costo de Almacenamiento:** Guardar factores densos exige $O(n^2)$ lugares de memoria, complicado para sistemas de gran porte en computación científica.
- **Costo Operacional:** Una factorización directa escala como $O(n^3)$ flops, sin importar los ceros que haya.
- **Alternativa:** Generar una sucesión de aproximaciones $\{x^{(k)}\}$ que converja a la solución exacta $x^*$ conservando la matriz $A$ intacta.

---

# Métodos de Separación

La estrategia para construir un algoritmo iterativo estacionario consiste en realizar una **separación o descomposición de la matriz** $A \in \mathbb{R}^{n \times n}$ de la forma:

$$A = M - N$$

Reescribiendo el sistema original $Ax = b$ mediante esta separación:

$$(M - N)x = b \implies Mx = Nx + b$$

- **Matriz Precondicionadora ($M$):** Fácil de invertir (ej. diagonal o triangular).
- **Ecuación de Recurrencia:** Se define el esquema iterativo:
  $$M x^{(k+1)} = N x^{(k)} + b$$
  $$ x^{(k+1)} = M^{-1}N x^{(k)} + M^{-1}b = G(x^{(k)}) $$

---

# Punto Fijo!
**Teorema:** Sea $\Vert{}\cdot\Vert{}$ una norma en $\mathbb{R}^n$, $F : \mathbb{R}^n \to \mathbb{R}^n$ y suponga que existe $\tau \in [0,1)$ tal que $\Vert{}F(y) - F(x)\Vert{} \le \tau \Vert{}y - x\Vert{}$ para todo $x,y \in \mathbb{R}^n$. Entonces existe $x^*$ tal que $x^* = F(x^*)$ y dicho punto es único. Más aún, para cualquier $x^0 \in \mathbb{R}^n$ la sucesión $\{x^k\}$ generada por $x^{k+1} = F(x^k)$ converge a $x^*$.

**Corolario:** Sea $\{x^k\}$ generada por (7.1). Si $M$ es no singular y para alguna norma matricial inducida vale que $\Vert{}M^{-1}N\Vert{} < 1$, entonces para cualquier $x^0 \in \mathbb{R}^n$ la sucesión $\{x^k\}$ converge a $x^*$ con $Ax^* = b$. Además, vale que
$$\Vert{}x^{k+1} - x^*\Vert{} \le \frac{\Vert{}M^{-1}N\Vert{}}{1 - \Vert{}M^{-1}N\Vert{}} \Vert{}x^{k+1} - x^k\Vert{}.$$

---

## Demostración:
- Como la sucesión cumple que $x^{k+1} = G(x^k)$ con $G(x) = M^{-1}Nx + M^{-1}b$, si $\tau = \Vert{}M^{-1}N\Vert{} < 1$ entonces
$$\Vert{}G(y) - G(x)\Vert{} = \Vert{}M^{-1}N(y - x)\Vert{} \le \tau \Vert{}y - x\Vert{}.$$

- El Teorema anterior garantiza que $\lim_{k \to \infty} x^k = x^*$ con $Ax^* = b$.

- Como $x^*$ es un punto fijo de $G$,
$$\begin{aligned} \Vert{}x^{k+1} - x^*\Vert{} &= \Vert{}G(x^k) - G(x^*)\Vert{} \le \tau \Vert{}x^k - x^*\Vert{} \\ &\le \tau \Vert{}x^{k+1} - x^k\Vert{} + \tau \Vert{}x^{k+1} - x^*\Vert{}. \end{aligned}$$

- Usando que $\tau < 1$, despejamos $\Vert{}x^{k+1} - x^*\Vert{}$ y obtenemos lo deseado. $\blacksquare$

Esto es una condición SUFICIENTE!!!

---

# Descomposición Canónica de $A$

Para derivar los métodos clásicos de separación, particionamos la matriz $A$ en sus tres componentes estructurales:

$$A = D + L + U \quad$$

donde:
- **$D$:** Matriz diagonal con las entradas diagonales de $A$ ($a_{ii}$).
- **$L$:** Matriz triangular inferior estricta con las entradas por debajo de la diagonal ($a_{ij}$ con $i > j$).
- **$U$:** Matriz triangular superior estricta con las entradas por encima de la diagonal ($a_{ij}$ con $i < j$).

---

# Revisemos el Método de Jacobi

La elección de las matrices $M$ y $N$ da origen a distintos algoritmos, por ejemplo:

**Método de Jacobi:** Tomemos $M_J = D$ y $N_J = -(L + U)$.
   $$D x^{(k+1)} = -(L + U) x^{(k)} + b$$

> Definición: Decimos que una matriz $A$ es diagonalmente dominante por filas (columnas) si:
>$$
>|a_{ii}| > \sum_{\substack{j=1 \\ j \neq i}}^n |a_{i,j}| \begin{pmatrix}|a_{ii}| > \sum_{\substack{i=1 \\ j \neq i}}^m |a_{i,j}|\end{pmatrix}
>$$

---

# Iteración de Jacobi

$$x_i^{k+1} = \frac{1}{a_{ii}} \left( b_i - \sum_{\substack{j=1 \\ j \neq i}}^n a_{ij} x_j^k \right) , \quad i = 1, \dots, n.$$
Cuándo converge?

**Proposición:** Si $A \in \mathbb{R}^{n \times n}$ es diagonalmente dominante entonces
$$\Vert{}M_J^{-1} N_J\Vert{}_\infty < 1.$$

**Demostración:** Por definición de $M_J, N_J, \Vert{}\cdot\Vert{}_\infty$ y la hipótesis sobre $A$, tenemos
$$\Vert{}M_J^{-1} N_J\Vert{}_\infty = \max_{1 \le i \le n} \sum_{\substack{j=1 \\ j \neq i}}^n \left\vert{} \frac{a_{ij}}{a_{ii}} \right\vert{} < 1. \blacksquare$$

---

# Algoritmo: Iteración de Jacobi

**Entradas:** $A \in \mathbb{R}^{n \times n}$, $b, x \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$. **Salida:** $x^+$ aproximación de $x^*$.

1. Si $A_{ii} = 0$ para algún $i$, parar y retornar un error.  
  Sino, para $A = L + D + U$, hacer
  $$\begin{aligned}
  b &\leftarrow D^{-1}b, \\
  A &\leftarrow D^{-1}(L + U).
  \end{aligned}$$

2. Para $k = 1, \dots, m$, definir
  $$x^+ = b - Ax.$$
  Si $\|x^+ - x\|_\infty \le \epsilon$ ir al paso 3. Sino, hacer $x = x^+$.

3. Retornar $x^+$.

---

# Iteración de Gauss-Seidel

La iteración de Gauss-Seidel se define tomando $M_{GS} = D + L$ y $N_{GS} = -U$:
$$M_{GS} x^{k+1} = N_{GS} x^k + b$$

Escribiendo las componentes de esta ecuación, se tiene que:
$$x_i^{k+1} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij} x_j^{k+1} - \sum_{j=i+1}^n a_{ij} x_j^k \right), \quad i = 1, \dots, n.$$

- Cada componente actualizada $x_i^{k+1}$ se utiliza inmediatamente en el cálculo de las componentes siguientes dentro de la misma iteración.

---

# Convergencia de Gauss-Seidel

Veamos que se cumple un resultado análogo al de la iteración de Jacobi:

**Proposición:** Si $A \in \mathbb{R}^{n \times n}$ es diagonalmente dominante en sentido estricto entonces:
$$\|M_{GS}^{-1} N_{GS}\|_\infty < 1.$$

**Corolario:** Si $A \in \mathbb{R}^{n \times n}$ es diagonalmente dominante en sentido estricto, entonces para cualquier $x^0 \in \mathbb{R}^n$ la sucesión $\{x^k\}$ generada por la iteración de Gauss-Seidel converge a $x^*$ con $Ax^* = b$.

---

# Algoritmo: Iteración de Gauss-Seidel

**Entradas:** $A \in \mathbb{R}^{n \times n}$, $b, x \in \mathbb{R}^n$, $\epsilon > 0$ y $k_{\text{máx}} \in \mathbb{N}$. **Salida:** $x^+$ aprox. de $x^*$.

1. Si $A_{ii} = 0$ para algún $i$, parar y retornar un error.  
  Sino, para $A = L + D + U$, hacer
  $$\begin{aligned}
  b &\leftarrow (L+D)^{-1}b, \\
  A &\leftarrow D^{-1}(L + U), \\
  x^+ &\leftarrow x.
  \end{aligned}$$

2. Para $k = 1, \dots, k_{\text{máx}}$:
  - Para $i = 1, \dots, n$, definir $x_i^+ \leftarrow b_i - A_{i*} x^+.$
  - Si $\|x^+ - x\|_\infty \le \epsilon$ ir al paso 3. Sino, hacer $x = x^+$.

3. Retornar $x^+$.

---

# Iteración SOR (Sobrerelajación Sucesiva)

La iteración SOR (*Successive Over Relaxation*) requiere un parámetro de relajación $\omega > 0$ y considera $M_{SOR} = \frac{1}{\omega}D + L$ y $N_{SOR} = \left(\frac{1}{\omega} - 1\right)D - U$, o sea:

- Gauss-Seidel es el caso particular con $\omega = 1$.
- **Convergencia:** Si $A$ es simétrica definida positiva y $0 < \omega < 2$, entonces:
  $$\|M_{SOR}^{-1} N_{SOR}\| < 1$$
  para cierta norma matricial inducida $\|\cdot\|$.

---

# Ventajas de los Métodos de Separación

- **Aprovechamiento de la Dispersión:**
  - Explotan naturalmente matrices ralas, evitan *fill-in* (llenado de matrices).
  - Costo por iteración mínimo: un producto matriz-vector y resolver con $M$.

- **Simplicidad Computacional y Paralelismo:**
  - "Fácil" implementación y requisitos mínimos de memoria.
  - Algunos de ellos son paralelizables ([por ejemplo, Jacobi](https://ericdarve.github.io/NLA/content/jacobi_method.html#implementation-and-parallelism)).

- **Flexibilidad y Precondicionamiento:**
  - La matriz $M$ actúa como matriz precondicionadora.
  - Son piezas fundamentales para métodos modernos más robustos (soon).

---

# Limitaciones de los Métodos de Separación

- **Garantías y Velocidad de Convergencia:**
  - Si $\rho(M^{-1}N) \ge 1$, el método diverge.
  - Convergencia puede ser excesivamente lenta y exigir condiciones fuertes.

- **Rendimiento Subóptimo a Gran Escala:**
  - Para sistemas lineales de gran dimensión ($n$ grande), los esquemas básicos como Jacobi o SOR son inferiores a técnicas avanzadas.

- **Dificultades en Aceleración Polinomial:**
  - Con ciertas separaciones (como en SOR), la matriz de iteración puede tener autovalores sobre círculos o distribuciones complejas, limitando la efectividad.

---

# Casos de Uso y Aplicaciones

- **Discretización de Ecuaciones Diferenciales Parciales (EDPs):**
  - Muy comunes al aplicar diferencias finitas o elementos finitos.
  - Las matrices resultantes son enormes, altamente dispersas y con estructuras bien definidas (p. ej., matrices banda o diagonales dispersas).

- **Precondicionadores en Métodos de Krylov:**
  - Su uso moderno más importante: elegir $M \approx A$ fácil de invertir tal que el sistema precondicionado $M^{-1}Ax = M^{-1}b$ tenga $\kappa(M^{-1}A) \ll \kappa(A)$.
  - Un menor número de condición acelera enormemente la convergencia de métodos como **Gradiente Conjugado** (soon) o **GMRES**.
