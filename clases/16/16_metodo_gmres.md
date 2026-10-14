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
## Clase 16: Método GMRES
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# La Iteración de Arnoldi
## Construcción de Bases Ortonormales en Subespacios de Krylov

* **Origen:** Algoritmo desarrollado por Walter Edwin Arnoldi (1951).
* **Propósito:** Construir una base ortonormal para un subespacio de Krylov y proyectar matrices de gran dimensión.
* **Aplicación:** Cálculo de valores propios y resolución de sistemas lineales de gran escala (ej. GMRES).

---

## Recordemos: Subespacios de Krylov

Para una matriz $A \in \mathbb{R}^{n \times n}$ y un vector inicial $b \in \mathbb{R}^n \setminus \{0\}$, el **subespacio de Krylov** de orden $k$ se define como:

$$\mathcal{K}_k(A, b) = \operatorname{span}\{b, Ab, A^2 b, \dots, A^{k-1} b\}$$

* Representa el espacio formado por polinomios aplicados a la matriz: $\mathcal{K}_k(A, b) = \{p(A)b : \operatorname{grado}(p) \le k-1\}$.
* Para $n$ muy grande, operar directamente sobre $\mathbb{R}^n$ es costoso; reducir el problema a $\mathcal{K}_k(A, b)$ permite aproximar soluciones con $k \ll n$.

---

## El Problema de la Base Monomial

La secuencia de vectores $\{b, Ab, A^2 b, \dots, A^{k-1} b\}$ presenta graves problemas numéricos:

* **Inestabilidad por mal condicionamiento:** A medida que $k$ crece, los vectores $A^j b$ se alinean paulatinamente con el autovector dominante de $A$ (comportamiento del método de las potencias).
* **Pérdida de independencia lineal:** La base natural se vuelve casi linealmente dependiente.
* **Solución:** Ortogonalizar la secuencia a medida que se genera utilizando el método de **Gram-Schmidt Modificado**.

---

## Algoritmo de la Iteración de Arnoldi

Dado $A \in \mathbb{R}^{n \times n}$ y vector de inicio $b$:

1. Normalizar el vector inicial: $q_1 = \frac{b}{\|b\|_2}$

2. Para $k = 1, 2, \dots, m$:
   * Calcular nuevo candidato: $v = A q^k$
   * Ortogonalizar frente a la base previa $q^1, \dots, q^k$:
     $$h_{j,k} = (q^j)^T v, \quad v \leftarrow v - h_{j,k} q^j \quad (j = 1, \dots, k)$$
   * Normalizar el nuevo vector ortogonal:
     $$h_{k+1,k} = \|v\|_2, \quad q^{k+1} = \frac{v}{h_{k+1,k}}$$

---

## Relación Matricial

De la ortogonalización se deriva la relación paso a paso:

$$A q^k = \sum_{j=1}^{k+1} h_{j,k} q^j$$

Agrupando en forma matricial para las primeras $k$ iteraciones:

$$A Q_k = Q_k H_k + h_{k+1,k} q^{k+1} (e^k)^T$$

* $Q_k = [q^1, q^2, \dots, q^k] \in \mathbb{R}^{n \times k}$ tiene columnas ortonormales ($Q_k^* Q_k = I_k$).
* $H_k \in \mathbb{R}^{k \times k}$ es una matriz **Hessenberg superior**.
* $e^k = [0, \dots, 0, 1]^T \in \mathbb{R}^k$.

---

## Estructura de la Matriz Hessenberg $H_k$

Dado que $Q_k^* Q_k = I_k$, la proyección de Rayleigh-Ritz de $A$ sobre $\mathcal{K}_k(A, b)$ resulta en: $H_k = Q_k^* A Q_k$

$$H_k = \begin{bmatrix}
h_{1,1} & h_{1,2} & h_{1,3} & \dots & h_{1,k} \\
h_{2,1} & h_{2,2} & h_{2,3} & \dots & h_{2,k} \\
0 & h_{3,2} & h_{3,3} & \dots & h_{3,k} \\
\vdots & \ddots & \ddots & \ddots & \vdots \\
0 & \dots & 0 & h_{k,k-1} & h_{k,k}
\end{bmatrix}$$

Alternativamente, usando $\tilde{H}_k \in \mathbb{R}^{(k+1) \times k}$:

$$A Q_k = Q_{k+1} \tilde{H}_k$$

---

## Fenómeno de Ruptura (Breakdown)

Si en el paso $k$ el coeficiente subdiagonal se anula ($h_{k+1,k} = 0$):

$$A Q_k = Q_k H_k$$

### Implicaciones teóricas y prácticas:
* El subespacio $\mathcal{K}_k(A, b)$ es **estrictamente invariante** bajo $A$.
* Los $k$ autovalores de $H_k$ coinciden **exactamente** con un subconjunto de autovalores de $A$.
* En algoritmos como GMRES, esto representa la convergencia exacta de la solución.

---

## Valores de Ritz y Convergencia Espectral

Los autovalores $\theta_j$ de la matriz reducida $H_k \in \mathbb{R}^{k \times k}$ se denominan **valores de Ritz**.

* A medida que $k$ aumenta, los valores de Ritz convergen rápidamente hacia los autovalores extremales (de mayor módulo o en los bordes del espectro) de $A$.
* Si $H_k y^j = \theta_j y^j$, entonces $x^j = Q_k y^j$ es el **vector de Ritz** que aproxima al autovector correspondiente de $A$.

---

## Casos Particulares y Extensiones

1. **Matriz Simétrica / Hermitiana ($A = A^*$):**
   * $H_k$ se vuelve tridiagonal simétrica.
   * La iteración de Arnoldi se reduce al **Algoritmo de Lanczos**, reduciendo drásticamente el costo computacional por paso.

2. **Resolución de Sistemas $A x = b$:**
   * Base del método **GMRES** (Generalized Minimal Residual), el cual minimiza $\|b - A x_k\|_2$ sobre el subespacio de Krylov.

3. **Reinicio Implicito:**
   * En problemas muy grandes, $k$ no puede crecer indefinidamente por restricciones de memoria; se aplican técnicas de reinicio (ej. IRAM / ARPACK).

---

# Convergencia del Proceso de Arnoldi
## Análisis Polinomial y Comportamiento Espectral

* **Objetivo:** Comprender la rapidez y el modo en que los valores de Ritz aproximan a los autovalores de la matriz $A$.
* **Marco Teórico:** La convergencia se analiza mediante la teoría de **aproximación polinomial** sobre el espectro $\Lambda(A)$.
* **Idea Clave:** La iteración de Arnoldi resuelve implícitamente un problema de minimización de norma sobre polinomios mónicos.

---

## El Residuo de un Par de Ritz

Sea $(y_k, \theta_k)$ un par propio de la matriz reducida $H_k \in \mathbb{R}^{k \times k}$, es decir, $H_k y_k = \theta_k y_k$ con $\|y_k\|_2 = 1$.

* El **vector de Ritz** correspondiente en $\mathbb{R}^n$ es $u_k = Q_k y_k$ (con $\|u_k\|_2 = 1$).
* Aplicando la relación fundamental $A Q_k = Q_k H_k + h_{k+1,k} q_{k+1} e_k^T$:

$$A u_k - \theta_k u_k = A Q_k y_k - \theta_k Q_k y_k = h_{k+1,k} (e_k^T y_k) q_{k+1}$$

* **Norma del Residuo:**
  $$\|A u_k - \theta_k u_k\|_2 = h_{k+1,k} |e_k^T y_k|$$

> **Conclusión:** El par de Ritz es una solución exacta si $h_{k+1,k} = 0$ (ruptura) o si la última componente del autovector $y_k$ es prácticamente nula.

---

## Propiedad de Minimización Polinomial

Sea $\mathcal{P}_k^1$ el conjunto de todos los **polinomios mónicos** de grado $k$ (de la forma $p(z) = z^k + c_{k-1} z^{k-1} + \dots + c_0$).

Si definimos $p_k(z) = \det(z I_k - H_k)$ como el polinomio característico de $H_k$:

1. $p_k$ es un polinomio mónico de grado $k$.
2. Se cumple la propiedad de optimalidad:
   $$\|p_k(A) q_1\|_2 = \min_{p \in \mathcal{P}_k^1} \|p(A) q_1\|_2$$

* La iteración de Arnoldi encuentra el polinomio mónico que **minimiza la norma del vector residual** $p(A) q_1$ en el subespacio de Krylov.

---

## Cota de Error mediante Diagonalización

Si la matriz $A \in \mathbb{R}^{n \times n}$ es diagonalizable ($A = X \Lambda X^{-1}$ con $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$):

* Para cualquier polinomio $p(z)$:
  $$p(A) = X p(\Lambda) X^{-1} = X \operatorname{diag}(p(\lambda_1), \dots, p(\lambda_n)) X^{-1}$$

* Aplicando normas matriciales subordenadas:
  $$\|p_k(A) q_1\|_2 \le \kappa_2(X) \min_{p \in \mathcal{P}_k^1} \max_{\lambda \in \Lambda(A)} |p(\lambda)|$$

donde $\kappa_2(X) = \|X\|_2 \|X^{-1}\|_2$ es el número de condición de la matriz de autovectores.

---

## Convergencia de Autovalores Aislados (Outliers)

El comportamiento de $\min_{p \in \mathcal{P}_k^1} \max_{\lambda \in \Lambda(A)} |p(\lambda)|$ explica qué autovalores se capturan primero:

1. **Autovalores periféricos o aislados:**
   * Si un autovalor $\lambda_1$ está alejado del resto del espectro, un polinomio $p_k$ de grado modesto puede colocar una raíz en $\lambda_1$ haciendo $p_k(\lambda_1) \approx 0$.
   * Esto cancela la componente asociada a $\lambda_1$ rápidamente.

2. **Efecto de "Deflación Implícita":**
   * Una vez que un valor de Ritz converge a $\lambda_1$, los pasos posteriores de Arnoldi se enfocan en los autovalores restantes, convergiendo en orden desde el exterior hacia el interior del espectro.

---

## El Papel de los Polinomios de Chebyshev

Cuando los autovalores no aislados de $A$ están contenidos en una región convexa (como una elipse o un intervalo en $\mathbb{R}$):

* La minimización de $|p(\lambda)|$ se resuelve utilizando **Polinomios de Chebyshev** desplazados y escalados.
* La tasa de convergencia depende de la razón del eje mayor al eje menor de la región espectral.

### Resumen del Comportamiento de Arnoldi
* **Matrices Normales ($\kappa_2(X) = 1$):** La convergencia está completamente determinada por la distribución geométrica de los autovalores en el plano complejo.
* **Matrices No Normales ($\kappa_2(X) \gg 1$):** El término $\kappa_2(X)$ puede retrasar la convergencia inicial (pseudoespectro), aunque el carácter de minimización polinomial se mantiene.

---

# El Método GMRES
## Generalized Minimal Residual Method

* **Origen:** Desarrollado por Yousef Saad y Martin H. Schultz (1986).
* **Propósito:** Resolver sistemas de ecuaciones lineales de gran escala $A x = b$, donde $A \in \mathbb{R}^{n \times n}$ es una matriz no hermitiana (o no simétrica) e invertible.
* **Propiedad Fundamental:** En cada paso $k$, GMRES encuentra la solución aproximada $x_k$ que **minimiza la norma $L_2$ del residuo** sobre el subespacio de Krylov.

---

## Formulación del Problema y Subespacio de Krylov

Dado un sistema $A x = b$ y un vector inicial $x_0$ con residuo $r_0 = b - A x_0$:

* Se considera el subespacio de Krylov generado por el residuo inicial:
  $$\mathcal{K}_k(A, r_0) = \operatorname{span}\{r_0, A r_0, A^2 r_0, \dots, A^{k-1} r_0\}$$

* La solución aproximada en la iteración $k$ se define como:
  $$x_k \in x_0 + \mathcal{K}_k(A, r_0)$$

* **Criterio de minimización del residuo:**
  $$x_k = \arg\min_{x \in x_0 + \mathcal{K}_k(A, r_0)} \|b - A x\|_2$$

---

## Reducción mediante la Iteración de Arnoldi

Cualquier vector en el espacio afín se expresa como $x = x_0 + Q_k y$, donde $Q_k \in \mathbb{R}^{n \times k}$ contiene las columnas ortonormales generadas por Arnoldi con $q_1 = r_0 / \beta$ y $\beta = \|r_0\|_2$.

* Expresión del vector residuo:
  $$r(y) = b - A(x_0 + Q_k y) = r_0 - A Q_k y$$

* Sustituyendo la relación de Arnoldi $A Q_k = Q_{k+1} \tilde{H}_k$, con $\tilde{H}_k \in \mathbb{R}^{(k+1) \times k}$:
  $$r(y) = \beta q_1 - Q_{k+1} \tilde{H}_k y = Q_{k+1} (\beta e_1 - \tilde{H}_k y)$$

---

## El Problema de Mínimos Cuadrados Reducido

Puesto que las columnas de $Q_{k+1}$ son ortonormales ($Q_{k+1}^* Q_{k+1} = I_{k+1}$), se preserva la norma $L_2$:

$$\|b - A x_k\|_2 = \min_{y \in \mathbb{R}^k} \|\beta e_1 - \tilde{H}_k y\|_2$$

* **Ventaja dimensional:** El problema original de dimensión $n$ se transforma en un problema de mínimos cuadrados de dimensión $(k+1) \times k$, donde $k \ll n$.
* **Elementos:**
  * $\beta = \|r_0\|_2$ (escalar).
  * $e_1 = [1, 0, \dots, 0]^T \in \mathbb{R}^{k+1}$.
  * $\tilde{H}_k \in \mathbb{R}^{(k+1) \times k}$ es la matriz de Hessenberg reducida.

---

## Resolución Eficiente mediante Rotaciones de Givens

Para resolver $\min_{y} \|\beta e_1 - \tilde{H}_k y\|_2$ de manera incremental en cada iteración:

1. **Factorización QR acumulativa:** Se aplican rotaciones de Givens $G_1, G_2, \dots, G_k$ para transformar $\tilde{H}_k$ en una matriz triangular superior $R_k$ (con una última fila nula).
2. **Actualización del vector modificado:**
   $$\tilde{g}_k = G_k \dots G_1 (\beta e_1) = \begin{bmatrix} g_k \\ \gamma_{k+1} \end{bmatrix}$$
3. **Cálculo directo del residuo:**
   $$\|b - A x_k\|_2 = |\gamma_{k+1}|$$
   * Permite monitorear la convergencia **sin calcular explícitamente $x_k$ ni resolver el sistema $R_k y_k = g_k$** hasta alcanzar la tolerancia deseada.

---

## GMRES Reiniciado: $GMRES(m)$

### Limitación computacional
A medida que $k$ crece:
* El almacenamiento de las columnas de $Q_k$ requiere $O(k n)$ de memoria.
* El costo de ortogonalización escala como $O(k^2 n)$.

### Algoritmo $GMRES(m)$
* Se fija un número máximo de pasos $m$ (ej. $m = 30$ o $m = 50$).
* Al alcanzar $m$ iteraciones, se calcula $x_m$, se reevalúa el residuo $r_m = b - A x_m$, y se reinicia el proceso tomando $x_0 \leftarrow x_m$.

> **Efecto de estancamiento:** El reinicio pierde la propiedad de optimalidad global sobre el subespacio de Krylov expandido, lo que puede frenar la convergencia si $m$ es demasiado pequeño.
