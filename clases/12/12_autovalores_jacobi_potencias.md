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
## Clase 12: Autovalores: Métodos de Jacobi (Final) y Potencias
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Método de Jacobi

Basado en la diagonalización de matrices simétricas en $\mathbb{R}^{2 \times 2}$.

$$

\begin{bmatrix}
  \cos(\theta) & -\sin(\theta) \\ 
  \sin(\theta) & \cos(\theta)
\end{bmatrix}
\begin{bmatrix}
  a & b \\ 
  b & c
\end{bmatrix}
\begin{bmatrix}
  \cos(\theta) & \sin(\theta) \\ 
  -\sin(\theta) & \cos(\theta)
\end{bmatrix} = 
\begin{bmatrix}
  \lambda_1 & 0 \\ 
  0 & \lambda_2
\end{bmatrix}
$$

Para matrices de cualquier tamaño, intentamos llevar a $0$ al $off(A_k) = \sqrt{\sum_{i \ne j} a_{ij}^2}$ mediante rotaciones similares a las de Givens (matrices ortogonales).

Si en cada iteración elegimos el par $(i, j)$ con el mayor valor absoluto, entonces el método converge a la diagonalización de $A$.

$$
off(A_{k})^2 \le \left(1 - \frac{1}{N}\right) off(A_{k-1})^2 \le \left(1 - \frac{1}{N}\right)^k off(A_{0})^2
$$

---

# Algoritmo *(Diagonalización de $A \in \mathbb{R}^{2 \times 2}$ simétrica)*

**Entrada:** Matriz simétrica $A \in \mathbb{R}^{2 \times 2}$. **Salida:** $c, s \in \mathbb{R}$. 

1. Si $a_{12} = 0$, retornar $c = 1$ y $s = 0$.
2. Definir:
  $$
  \tau = (a_{22} - a_{11})/(2a_{12}),
  $$
  $$
  t = \begin{cases} 
  -1 / \left(\tau + \sqrt{\tau^2 + 1}\right), & \text{si } \tau \ge 0, \\ 
  1 / \left(-\tau + \sqrt{\tau^2 + 1}\right), & \text{si } \tau < 0. 
  \end{cases}
  $$
  $$
  c = 1/\sqrt{1 + t^2},
  $$
  $$
  s = tc.
  $$
3. Retornar $c$ y $s$

---

# Algoritmo *(Método de Jacobi para diagonalización)*

**Entrada:** $A \in \mathbb{R}^{n \times n}$ simétrica, $\epsilon > 0$ y $m \in \mathbb{N}$. **Salidas:** $B, Q \in \mathbb{R}^{n \times n}$ t.q. $B = Q^T A Q$ con $\text{off}(B) \le \epsilon$.

1. Definir $Q = I$.
2. Para $k = 1, \dots, m$, si $\color{blue}\text{off}(A) \le \epsilon$ ir al paso 3.
   Sino, definir $\mathcal{I} = \{i, j\}$ t.q. $|A_{ij}| = \operatorname{m\acute{a}x}_{r \ne s} |A_{rs}|$,
   $$
   J = \begin{bmatrix} c & -s \\ s & c \end{bmatrix} \text{ aplicando el algoritmo anterior a } A_{\mathcal{I}\mathcal{I}},
   $$
   $$
   \begin{aligned}
   A_{\mathcal{I} *} &\leftarrow J^T A_{\mathcal{I} *}, \\
   A_{* \mathcal{I}} &\leftarrow A_{* \mathcal{I}} J, \\
   Q_{* \mathcal{I}} &\leftarrow Q_{* \mathcal{I}} J.
   \end{aligned}
   $$
3. Retornar $B = A$ y $Q$.

---

- Dada una tolerancia $\epsilon$ podemos realizar una cantidad máxima $m$ de rotaciones hasta obtener una matriz diagonal con $\text{off}(A) \le \epsilon$.

- Una cota para $m$ está dada por:

$$
m \ge \frac{log(\epsilon^2 / \text{off}(A)^2)}{log(1 - 2/(n^2 - n))}
$$

- Estamos en condiciones de estimar la descomposición SVD, cómo lo hacemos?

- Si cortamos en algún instante $m$, podemos estimar qué tan lejos estamos de los autovalores verdaderos?

---
# Teorema (Discos de Gershgorin)

Si $X^{-1}AX = D + F$ con $D$ diagonal y $F$ con ceros en la diagonal, entonces cada autovalor $\lambda$ de $A$ satisface

$$
\lambda \in \bigcup_{i=1}^n D_i,
$$

donde $D_i = \{z \in \mathbb{C} \mid |z - d_i| \le \sum_{j=1}^n |f_{ij}|\}$.

Como $B = Q^T A Q$ con $\text{off}(B) \le \epsilon$, el teorema nos garantiza que si $\lambda$ es un autovalor de $A$ entonces $|\lambda - b_{ii}| \le \sqrt{n}\epsilon$ para algún índice $i$. Qué pasa si $X$ es la matriz identidad?

---

# Cálculo de Autovalores: Aplicaciones

- **Operaciones y funciones matriciales:** Si la matriz es diagonalizable, podemos calcular fácilmente potencias y funciones generales de matrices:
  $$A^k = X \Lambda^k X^{-1}, \qquad f(A) = X f(\Lambda) X^{-1}$$
- **Sistemas Dinámicos:** La solución de $\frac{dx}{dt} = M x$ es $x(t) = \exp(Mt) x_0$. La estabilidad a largo plazo depende de los términos $\exp(\lambda_i t)$.
- **Enfoque numérico:** Resolver $\det(A - \lambda I) = 0$ **no** es estable ni escalable para matrices generales.

---

# No Existe Solución Directa

- A diferencia de resolver $Ax = b$ con eliminación Gaussiana ($LU$), **no existe un método directo** (fórmula finita) para calcular los autovalores de una matriz general de $n \times n$ para $n \ge 5$.
- La dificultad radica en la conexión fundamental entre autovalores y las **raíces de polinomios**.
- Todo polinomio mónico puede representarse mediante su **matriz compañera** (*companion matrix*), cuyos autovalores coinciden con las raíces del polinomio.

---

# La Necesidad de Métodos Iterativos

- **Teorema de Abel-Ruffini (Siglo XIX):** No existe una fórmula general por radicales (análoga a la fórmula cuadrática) para polinomios de grado 5 o mayor.

- **Consecuencias:**
  1. Si existiera un método directo y exacto para autovalores, resolvería de forma exacta cualquier polinomio.
  2. Como Abel-Ruffini demuestra que esto es imposible, **no puede existir un algoritmo directo y exacto** para matrices generales.
  3. Entonces los métodos para calcular autovalores son necesariamente **iterativos**.

- **En la práctica:** Los algoritmos iterativos convergen muy velozmente a precisión de máquina, siendo indistinguibles de una solución exacta.

---

# Método de las Potencias: Intuición

El **método de las potencias** busca el autovalor **estrictamente dominante** (mayor magnitud) y su autovector asociado.

- Consideremos $A$ diagonalizable. Un vector $q$ puede escribirse como combinación lineal de los autovectores:
  $$q = c_1 x_1 + c_2 x_2 + \dots + c_n x_n$$
- Aplicando la transformación $A$ sucesivamente $k$ veces:
  $$A^k q = c_1 \lambda_1^k x_1 + c_2 \lambda_2^k x_2 + \dots + c_n \lambda_n^k x_n$$
- Si $|\lambda_1| > |\lambda_2| \ge \dots$, el término $\lambda_1^k$ crece más rápido. Para $k$ grande:
  $$A^k q \approx c_1 \lambda_1^k x_1$$

---

# Método de las Potencias: Derivación Formal

- **Hipótesis:**
  1. $A \in \mathbb{C}^{n \times n}$ es diagonalizable con base de autovectores $\{x_1, \dots, x_n\}$.
  2. Existe un **autovalor estrictamente dominante**:
     $$|\lambda_1| > |\lambda_2| \ge |\lambda_3| \ge \dots \ge |\lambda_n|$$
  3. Elegimos un vector inicial $q_0 = \sum_{i=1}^n c_i x_i$ tal que $c_1 \ne 0$.
     *(Elegir $q_0$ aleatorio garantiza esto casi seguramente).*

---

# Método de las Potencias: Convergencia

- Analizamos el vector $z_k = A^k q_0$:
  $$z_k = A^k \left(\sum_{i=1}^n c_i x_i\right) = \sum_{i=1}^n c_i \lambda_i^k x_i$$
- Factorizando el término dominante $\lambda_1^k$:
  $$z_k = \lambda_1^k \left( c_1 x_1 + \sum_{i=2}^n c_i \left(\frac{\lambda_i}{\lambda_1}\right)^k x_i \right)$$
- Dado que $|\lambda_i / \lambda_1| < 1$ para todo $i \ge 2$, cuando $k \to \infty$:
  $$\left(\frac{\lambda_i}{\lambda_1}\right)^k \to 0 \implies z_k \approx \lambda_1^k c_1 x_1$$
- **Velocidad de convergencia:** El error decae según la razón $|\lambda_2 / \lambda_1|^k$. Cuanto más separada esté $\lambda_1$ de $\lambda_2$, más rápida será la convergencia.
