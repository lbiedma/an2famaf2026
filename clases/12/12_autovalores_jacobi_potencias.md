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

El **método de las potencias** busca el autovalor $\lambda_1$ **estrictamente dominante** (mayor magnitud) y su autovector $v^1$ asociado.

- Consideremos $A$ diagonalizable. Un vector $q$ puede escribirse como combinación lineal de los autovectores:
  $$q = c_1 v^1 + c_2 v^2 + \dots + c_n v^n$$
- Aplicando la transformación $A$ sucesivamente $k$ veces:
  $$A^k q = c_1 \lambda_1^k v^1 + c_2 \lambda_2^k v^2 + \dots + c_n \lambda_n^k v^n$$
- Si $|\lambda_1| > |\lambda_2| \ge \dots$, el término $\lambda_1^k$ crece más rápido. Para $k$ grande:
  $$A^k q \approx c_1 \lambda_1^k v^1$$

---

# Método de las Potencias: Derivación Formal

- **Hipótesis:**
  1. $A \in \mathbb{C}^{n \times n}$ es diagonalizable con base de autovectores $\{v^1, \dots, v^n\}$.
  2. Existe un **autovalor estrictamente dominante**:
     $$|\lambda_1| > |\lambda_2| \ge |\lambda_3| \ge \dots \ge |\lambda_n|$$
  3. Elegimos un vector inicial $q_0 = \sum_{i=1}^n c_i v^i$ tal que $c_1 \ne 0$.
     *(Elegir $q_0$ aleatorio garantiza esto casi seguramente).*

---

# Método de las Potencias: Detalles

- Analizamos el vector $z_k = A^k q_0$:
  $$z_k = A^k \left(\sum_{i=1}^n c_i x_i\right) = \sum_{i=1}^n c_i \lambda_i^k x_i$$
- Factorizando el término dominante $\lambda_1^k$:
  $$z_k = \lambda_1^k \left( c_1 x_1 + \sum_{i=2}^n c_i \left(\frac{\lambda_i}{\lambda_1}\right)^k x_i \right)$$
- Qué pasa con $lim_{k\rightarrow \infty} (\lambda_i / \lambda_1)^k$?

---

# En la Práctica

- Calcular $A^k q_0$ de forma directa es **numéricamente inestable**.
  - Si $|\lambda_1| > 1$, el vector $z_k$ **desborda** (*overflow*).
  - Si $|\lambda_1| < 1$, **subdesborda** a cero (*underflow*).
- **Solución:** normalizar el vector en **cada** iteración.
  - La norma se mantiene en $1$.
  - Solo se conserva la **dirección**, que es lo que nos interesa.
  - Con $q$ unitario, el autovalor se estima con el **cociente de Rayleigh**:
    $$R(A, q) = \frac{q^H A q}{q^H q} = q^H A q.$$
    Si $q$ es autovector, $R(A, q) = \lambda$.

---

# Algoritmo *(Iteración de potencias Norma 2)*

**Entrada:** $A \in \mathbb{C}^{n \times n}$. **Salidas:** $\lambda \in \mathbb{C}$ y $q \in \mathbb{C}^n$.

1. Elegir un vector unitario aleatorio $q$ (i.e., $\|q\|_2 = 1$).
2. Iterar hasta convergencia (p. ej., hasta que $\lambda$ deje de cambiar):
   1. $z = A q$
   2. $\lambda = q^H z$ (estimar el autovalor con el **cociente de Rayleigh**)
   3. $q = z / \|z\|_2$ (normalizar para la siguiente iteración)
3. Retornar $\lambda$ (autovalor dominante) y $q$ (autovector dominante).

---

# Teorema (Error del cociente de Rayleigh)

Sea $A \in \mathbb{C}^{n \times n}$ tal que $Av = \lambda v$ con $\|v\|_2 = 1$, y sea $\rho = q^H A q$ con $q^H q = \|q\|_2^2 = 1$. Entonces
$$|\lambda - \rho| \le 2\|A\|_2 \|v - q\|_2.$$

**Demostración.** Como $v^H A v = \lambda \|v\|_2^2 = \lambda$,
$$\lambda - \rho = v^H A v - q^H A q = v^H A(v - q) + (v - q)^H A q.$$
Por lo tanto,
$$|\lambda - \rho| \le \|v\|_2 \|A\|_2 \|v - q\|_2 + \|v - q\|_2 \|A\|_2 \|q\|_2 = 2\|A\|_2 \|v - q\|_2.$$

---

# Método de las Potencias: Convergencia

- Dado que $|\lambda_i / \lambda_1| < 1$ para todo $i \ge 2$, cuando $k \to \infty$:
  $$\left(\frac{\lambda_i}{\lambda_1}\right)^k \to 0 \implies z_k \approx \lambda_1^k c_1 x_1$$
- **Velocidad de convergencia:** El error decae según la razón $|\lambda_2 / \lambda_1|^k$. Cuanto más separada esté $\lambda_1$ de $\lambda_2$, más rápida será la convergencia.
- Vamos siempre al autovalor dominante, qué hacemos con el resto? :thinking:

---

# Deflación: Quitar la Primera Dirección

Supongamos que el método de las potencias encontró **exactamente** el autovector unitario dominante $q^1$. La matriz
$$P_1 = I - q^1 (q^1)^H$$
es la **proyección ortogonal sobre el complemento** de esa dirección.

- Idea: aplicar el método de las potencias a una matriz **deflacionada**, donde $\lambda_1$ ya no es dominante.
- En particular, $P_1 A q^1 = 0$: la dirección dominante fue **eliminada**.

---

# La Siguiente Dirección

En general $q^2$ **no** es autovector de $A$: $A q^2$ puede tener componente en $q^1$. Si $\operatorname{span}\{q^1,q^2\}$ es invariante y $q^2 \perp q^1$,
$$A q^2 = t_{12} q^1 + \lambda_2 q^2.$$

La proyección elimina el primer término y deja intacto el segundo:
$$P_1 A q^2 = \lambda_2 q^2.$$

- $q^2$ **no** tiene por qué ser autovector de $A$.
- **Sí** es autovector de $P_1 A$, con autovalor $\lambda_2$.
- Esta es la idea central de la **deflación**.

---

# Quitar Varias Direcciones

Si ya conocemos las primeras $i$ direcciones (ortonormales), las reunimos en
$$Q_i = [q^1,\ldots,q^i], \qquad P_i = I - Q_i Q_i^H.$$

- El subíndice $i$ cuenta columnas.
- La **matriz deflacionada** es $M_i = P_i A$.
- El subespacio $\operatorname{span}\{q^1,\ldots,q^i\}$ es invariante, así que $P_i A Q_i = 0$.
- En consecuencia, $P_i A = P_i A P_i$: $M_i$ descarta el subespacio conocido y actúa en su complemento ortogonal.

---

# Teorema (Deflación exacta)

Para $1 \le i < n$, los autovalores de $M_i$ son $i$ ceros seguidos de $\lambda_{i+1},\ldots,\lambda_n$, contados con multiplicidad. Además,
$$M_i q^{i+1} = \lambda_{i+1} q^{i+1}.$$

### Demostración
Toda $A$ es unitariamente semejante a una matriz **triangular superior**: existe $Q$ unitaria con
$$Q^H A Q = T = \begin{pmatrix} T_{11} & T_{12} \\ 0 & T_{22} \end{pmatrix},$$
particionada después de las primeras $i$ filas y columnas. En esta base, $P_i$ anula las primeras $i$ coordenadas:

---

### Demostración

$$
\begin{aligned}
Q^H P_i Q &= \begin{pmatrix} 0 & 0 \\ 0 & I_{n-i} \end{pmatrix}, \\
Q^H M_i Q &= \begin{pmatrix} 0 & 0 \\ 0 & I_{n-i} \end{pmatrix}
\begin{pmatrix} T_{11} & T_{12} \\ 0 & T_{22} \end{pmatrix}
= \begin{pmatrix} 0 & 0 \\ 0 & T_{22} \end{pmatrix}.
\end{aligned}
$$
Esta matriz triangular superior tiene los autovalores anunciados. Su primera coordenada restante es autovector con autovalor $\lambda_{i+1}$.

---

# Iteración de Potencias en el Subespacio Restante

Si hay **brecha estricta**, $\lambda_{i+1}$ es el autovalor **estrictamente dominante** de $M_i$.

Partimos de un vector unitario $v^0$ **ortogonal** a las direcciones ya conocidas y repetimos
$$
\begin{aligned}
w^{\ell+1} &= A v^\ell - Q_i\bigl(Q_i^H A v^\ell\bigr), \\
v^{\ell+1} &= \frac{w^{\ell+1}}{\|w^{\ell+1}\|_2}.
\end{aligned}
$$

- **No** hace falta formar $P_i$ ni $M_i$.
- Multiplicamos por $A$, restamos la proyección al subespacio conocido y normalizamos.

---

# Construcción Inductiva

- El vector inicial debe tener coeficiente no nulo en la dirección dominante de $M_i$. Un arranque aleatorio en el complemento lo garantiza con probabilidad $1$.
- Entonces $\operatorname{span}\{v^\ell\}$ converge a $\operatorname{span}\{q^{i+1}\}$.
- Si $i \le n-2$, el factor geométrico es $|\lambda_{i+2}/\lambda_{i+1}|$.
- Con $n-1$ direcciones, el complemento unidimensional da la última.

**Receta:** primera dirección por potencias, proyectar, repetir. Cada vector nuevo es ortogonal a los anteriores y agrandan un subespacio invariante.
$$\lambda_j = (q^j)^H A q^j.$$
