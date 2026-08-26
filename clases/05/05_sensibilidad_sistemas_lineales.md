---
marp: true
theme: default
paginate: true

---

# Análisis Numérico II / Álgebra Lineal Numérica
## Clase 05: Sensibilidad de Sistemas Lineales
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Introducción: ¿Por qué importa la sensibilidad numérica?

Al resolver un sistema lineal $Ax = b$ mediante una computadora, existen limitaciones inevitables debido a la representación finita de los números.

- El sistema que realmente se termina resolviendo es un sistema perturbado:
  $$(A + \Theta)\hat{x} = b + \vartheta$$
  donde $\Theta \in \mathbb{R}^{n \times n}$ y $\vartheta \in \mathbb{R}^n$ representan pequeñas perturbaciones producidas por la aritmética de punto flotante de doble precisión.
- Para cuantificar analíticamente cómo estas perturbaciones alteran la solución exacta, es indispensable introducir herramientas matemáticas que midan la magnitud de vectores y matrices: las **normas**.

---

# Definición de Norma

**Definición 3.1 (Norma):** Una norma en un espacio vectorial $X$ es una función $\|\cdot\|: X \to \mathbb{R}$ que satisface, para todo $x, y \in X$ y todo escalar $\alpha \in \mathbb{R}$:

1. **Positividad y No Degeneración:**
   $$\|x\| \ge 0 \quad \text{y} \quad \|x\| = 0 \iff x = 0 \quad$$
2. **Propiedad Subaditiva (Desigualdad Triangular):**
   $$\|x + y\| \le \|x\| + \|y\| \quad$$
3. **Homogeneidad Absoluta:**
   $$\|\alpha x\| = |\alpha| \|x\| \quad$$

---

# Normas Vectoriales $p$

Dentro de las normas vectoriales en $\mathbb{R}^n$, las de mayor uso en computación científica son las **normas $p$** para $p \ge 1$:

- Para un valor finito de $p \in [1, \infty)$:
  $$\|x\|_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p}$$
- El caso límite $p = \infty$ (norma de Chebyshev o del máximo):
  $$\|x\|_\infty = \max_{1 \le i \le n} |x_i|$$
- Casos particulares clásicos: la **norma de Manhattan** ($p=1$), la **norma Euclídea** ($p=2$), y la **norma de Chebyshev** ($p=\infty$).

---

# Demostración: Las normas $p$ son normas

**Teorema:** Si $1 \le p \le \infty$, entonces $\|\cdot\|_p$ es una norma vectorial legítima.

### Demostración para $p = \infty$:
- **Positividad:** Es evidente que $\|x\|_\infty = \max |x_i| \ge 0$, y es cero si y solo si todos los $x_i = 0$.
- **Homogeneidad:** 
  $$\|\alpha x\|_\infty = \max_{1 \le i \le n} |\alpha x_i| = \max_{1 \le i \le n} \left( |\alpha| |x_i| \right) = |\alpha| \max_{1 \le i \le n} |x_i| = |\alpha| \|x\|_\infty \quad$$
- **Desigualdad Triangular:** Como $|x_i + y_i| \le |x_i| + |y_i| \le \|x\|_\infty + \|y\|_\infty$ para todo $i$:
  $$\|x+y\|_\infty = \max_{1 \le i \le n} |x_i + y_i| \le \|x\|_\infty + \|y\|_\infty \quad$$

---

# Demostración para $p \in [1, \infty)$

Las propiedades de positividad, no degeneración y homogeneidad absoluta se heredan directamente de las propiedades del valor absoluto.

Para probar la **desigualdad triangular (Desigualdad de Minkowski)**, recurrimos a la propiedad de convexidad de la función $t \mapsto |t|^p$ para $p \ge 1$:
$$|(1-\lambda)t_0 + \lambda t_1|^p \le (1-\lambda)|t_0|^p + \lambda |t_1|^p \quad \forall \lambda \in [0, 1]$$

Sean $x, y \in \mathbb{R}^n$ vectores no nulos. Definimos:
$$\hat{x} = \frac{x}{\|x\|_p}, \quad \hat{y} = \frac{y}{\|y\|_p}, \quad \lambda = \frac{\|y\|_p}{\|x\|_p + \|y\|_p}$$
De esta manera, $1 - \lambda = \frac{\|x\|_p}{\|x\|_p + \|y\|_p}$.

---

# Demostración para $p \in [1, \infty)$ (Continuación)

Al evaluar la norma del vector normalizado combinado, obtenemos:
$$\left( \frac{\|x + y\|_p}{\|x\|_p + \|y\|_p} \right)^p = \left\| \frac{\|x\|_p}{\|x\|_p + \|y\|_p} \hat{x} + \frac{\|y\|_p}{\|x\|_p + \|y\|_p} \hat{y} \right\|_p^p = \left\| (1-\lambda)\hat{x} + \lambda\hat{y} \right\|_p^p$$

Desglosando en componentes y aplicando la desigualdad de convexidad:
$$\left\| (1-\lambda)\hat{x} + \lambda\hat{y} \right\|_p^p = \sum_{i=1}^n |(1-\lambda)\hat{x}_i + \lambda\hat{y}_i|^p$$
$$\le \sum_{i=1}^n \left( (1-\lambda)|\hat{x}_i|^p + \lambda|\hat{y}_i|^p \right) = (1-\lambda)\|\hat{x}\|_p^p + \lambda\|\hat{y}\|_p^p$$

Dado que $\|\hat{x}\|_p = \|\hat{y}\|_p = 1$, la suma se reduce a $(1-\lambda) + \lambda = 1$, lo que demuestra que $\|x+y\|_p \le \|x\|_p + \|y\|_p$. $\blacksquare$

---

# Equivalencia de Normas en $\mathbb{R}^n$

**Teorema:** Si $\||\cdot\||$ es una norma arbitraria en $\mathbb{R}^n$, entonces existen constantes positivas $\alpha, \beta > 0$ tales que para todo $x \in \mathbb{R}^n$:
$$\alpha \|x\|_2 \le \||x\|| \le \beta \|x\|_2$$

### Demostración (Cota Superior):
Utilizando la desigualdad de Cauchy-Schwarz, es posible acotar la norma $1$ por la norma Euclídea:
$$\sum_{i=1}^n |x_i| = \sum_{i=1}^n x_i y_i \le \|x\|_2 \|y\|_2 = \sqrt{n} \|x\|_2$$
Si expresamos $x = \sum_{i=1}^n x_i e_i$ y definimos $\mu = \max_{1 \le i \le n} \|e_i\||$ y $\beta = \sqrt{n}\mu$, por desigualdad triangular obtenemos:

---

# Equivalencia de Normas (Cota Inferior)

$$\|x\|| = \left\| \sum_{i=1}^n x_i e_i \right\|| \le \sum_{i=1}^n |x_i| \|e_i\|| \le \mu \sum_{i=1}^n |x_i| \le \beta \|x\|_2$$

Por la desigualdad triangular reversa e intercalando la cota superior obtenida:
$$\left| \|y\|| - \|x\|| \right| \le \|y - x\|| \le \beta \|y - x\|_2$$
Esto demuestra que la función $\||\cdot\||: \mathbb{R}^n \to \mathbb{R}$ es **continua** bajo la métrica Euclídea.

Consideremos ahora la esfera unidad Euclídea $S = \{x \in \mathbb{R}^n \mid \|x\|_2 = 1\}$, que es un conjunto cerrado y acotado (compacto). Por el **Teorema de Weierstrass**, la función continua $\||\cdot\||$ alcanza su valor mínimo en un punto $\bar{x} \in S$:
$$\alpha = \|\bar{x}\|| > 0 \quad (\text{dado que } \bar{x} \neq 0)$$

---

# Equivalencia de Normas (Conclusión)

Para cualquier $x \neq 0$, el vector normalizado $\frac{x}{\|x\|_2} \in S$, por lo que:
$$\left\| \frac{x}{\|x\|_2} \right\|| \ge \alpha \implies \|x\|| \ge \alpha \|x\|_2$$
Esto demuestra que toda norma es equivalente a la Euclídea. $\blacksquare$

**Corolario 3.7:** Si $\||\cdot\||$ y $\|\cdot\|$ son dos normas cualesquiera en $\mathbb{R}^n$, existen constantes $\alpha, \beta > 0$ tales que para todo $x \in \mathbb{R}^n$:
$$\alpha \|x\| \le \|x\|| \le \beta \|x\|$$

---

# El Significado de la Equivalencia de Normas
¿Para qué hacemos esta demostración en Álgebra Lineal Numérica?

***Independencia Cualitativa de la Convergencia***
En análisis, la equivalencia de normas significa que la convergencia cualitativa de una sucesión no depende de la norma elegida.

Si una sucesión de vectores ${x^k}$ converge a un vector límite $x^*$ bajo la norma $|\cdot|_a$, entonces se garantiza que converge a $x^*$ bajo cualquier otra norma $|\cdot|_b$ en $\mathbb{R}^n$.
Conceptos topológicos fundamentales (abiertos, cerrados, límites, continuidad de operadores) son los mismos en cualquier norma en dimensión finita.

---

# Conveniencia Matemática en Algoritmos
***Demostrar convergencia donde sea más sencillo***

En el diseño de algoritmos iterativos (ej. métodos de separación para resolver $Ax=b$), a menudo es mucho más fácil probar la convergencia bajo una norma específica. Los veremos en detalle más adelante.

**La garantía:** Gracias a la equivalencia, si el error $e^k \to 0$ en la norma conveniente de la prueba, converge a $0$ en todas las demás normas del espacio (como la física o la Euclídea).

---

# La Trampa Numérica: El Efecto de la Dimensión ($n$)
Aunque todas las normas en $\mathbb{R}^n$ son equivalentes analíticamente, no son equivalentes **numéricamente**.

Las constantes de equivalencia $\alpha$ y $\beta$ **dependen de** $n$:
$$|x|_2 \le |x|_1 \le \sqrt{n} |x|_2 \quad \text{y} \quad |x|_\infty \le |x|_2 \le \sqrt{n} |x|_\infty \quad$$

En sistemas grandes: $\sqrt{n} = \sqrt{10^6} = 1000$
Un error de tamaño $1$ en norma $\infty$ podría transformarse en un error de hasta $1000$ en norma $2$.
Por lo tanto, en precisión finita, la dependencia de $n$ en las cotas puede destruir la estabilidad numérica real.

---

# ¿Cómo elegir la norma en la práctica?

Cada norma vectorial se selecciona según el aspecto físico o computacional que se desea controlar:

- Norma Infinito ($|\cdot|_\infty$): Excelente para el control del "peor caso" o error máximo admisible en componentes individuales.
- Norma Euclídea ($|\cdot|_2$): Representa conceptos físicos directos como la distancia mínima geométrica o la energía del sistema.
- Norma Uno ($|\cdot|_1$): Útil para medir la acumulación absoluta de errores o flujos totales en una red de nodos.

---

# Introducción a las Normas Matriciales

Para estudiar el error de sensibilidad en sistemas matriciales, necesitamos extender el concepto de norma al espacio de matrices $\mathbb{R}^{m \times n}$.

**Definición:** Se dice que una norma matricial $\|\cdot\|$ es **submultiplicativa** si para cualesquiera matrices compatibles $A$ y $B$ se cumple que:
$$\|AB\| \le \|A\|\|B\| $$

- Esta propiedad es de vital importancia en el análisis de sensibilidad y la convergencia de algoritmos iterativos, ya que nos permite acotar el crecimiento del error en productos matriciales sucesivos.

---

# La Norma de Frobenius

La **Norma de Frobenius** identifica una matriz $A \in \mathbb{R}^{m \times n}$ con un vector en $\mathbb{R}^{mn}$ a través del operador de vectorización $\text{vec}(A)$ (transforma matriz en un vector de columnas concatenadas):

$$\|A\|_F = \sqrt{\text{tr}(A^T A)} = \left( \sum_{i=1}^m \sum_{j=1}^n |a_{ij}|^2 \right)^{1/2} = \|\text{vec}(A)\|_2 $$

### Propiedades:
1. **Positividad y No Degeneración:** $\|A\|_F \ge 0$, y $\|A\|_F = 0 \iff A = 0$.
2. **Homogeneidad Absoluta:** $\|\alpha A\|_F = |\alpha| \|A\|_F$.
3. **Desigualdad Triangular:** $\|A + B\|_F \le \|A\|_F + \|B\|_F$.

---

# Demostración: Propiedades

Debido a la linealidad del operador $\text{vec}$ (es decir, $\text{vec}(A + \alpha B) = \text{vec}(A) + \alpha \text{vec}(B)$), las propiedades se heredan directamente de la norma vectorial Euclídea:

- **Positividad:** Es claro que $\|\text{vec}(A)\|_2 \ge 0$, y es cero si y solo si todos los componentes de la matriz son nulos.
- **Homogeneidad:** 
  $$\|\alpha A\|_F = \|\text{vec}(\alpha A)\|_2 = \|\alpha \text{vec}(A)\|_2 = |\alpha| \|\text{vec}(A)\|_2 = |\alpha| \|A\|_F$$
- **Desigualdad Triangular:**
  $$\|A + B\|_F = \|\text{vec}(A + B)\|_2 = \|\text{vec}(A) + \text{vec}(B)\|_2$$
  $$\le \|\text{vec}(A)\|_2 + \|\text{vec}(B)\|_2 = \|A\|_F + \|B\|_F$$

---

# Demostración: Submultiplicatividad

Queremos probar que para matrices compatibles $A \in \mathbb{R}^{m \times n}$ y $B \in \mathbb{R}^{n \times p}$ se cumple $\|AB\|_F \le \|A\|_F \|B\|_F$.

Sean $a_i \in \mathbb{R}^n$ (las columnas de $A^T$, es decir, las filas de $A$) y $b_j \in \mathbb{R}^n$ (las columnas de $B$). Los elementos del producto $C = AB$ son $c_{ij} = (a_i)^T b_j$. Aplicando Cauchy-Schwarz:

$$\|AB\|_F^2 = \sum_{i=1}^m \sum_{j=1}^p |(a_i)^T b_j|^2 \le \sum_{i=1}^m \sum_{j=1}^p \|a_i\|_2^2 \|b_j\|_2^2$$

$$\|AB\|_F^2 \le \left( \sum_{i=1}^m \|a_i\|_2^2 \right) \left( \sum_{j=1}^p \|b_j\|_2^2 \right) = \|A\|_F^2 \|B\|_F^2$$

$$\implies \|AB\|_F \le \|A\|_F \|B\|_F$$

---

# Radio Espectral y Normas Inducidas

**Definición (Radio Espectral):** Para una matriz cuadrada $A \in \mathbb{R}^{n \times n}$, el radio espectral $\rho(A)$ es el valor máximo de los módulos de sus autovalores $\lambda \in \mathbb{C}$:
$$\rho(A) = \max \{|\lambda| \mid \det(A - \lambda I) = 0$$

**Definición (Norma Inducida):** Una norma vectorial induce una norma matricial que mide la amplificación máxima de un vector:
$$\|A\| = \sup_{x \neq 0} \frac{\|Ax\|}{\|x\|} = \max_{\\|x\\|=1} \|Ax\|$$

Toda norma matricial inducida es submultiplicativa por construcción:
$$\|AB\| \le \|A\| \|B\|$$

---

# Cálculo de Normas Inducidas Clásicas

Para cualquier matriz $A \in \mathbb{R}^{m \times n}$, tenemos:

1. **Norma-1 (Máxima suma absoluta por columnas):**
   $$\|A\|_1 = \max_{1 \le j \le n} \sum_{i=1}^m |a_{ij}|$$
2. **Norma-Infinito (Máxima suma absoluta por filas):**
   $$\|A\|_\infty = \max_{1 \le i \le m} \sum_{j=1}^n |a_{ij}|$$
3. **Norma-2 (Norma Espectral):**
   $$\|A\|_2 = \sqrt{\rho(A^T A)}$$

---

# Demostración: Fórmula de la Norma-1

Queremos probar que $\|A\|_1 = \max_{j} \sum_{i=1}^m |a_{ij}|$.

- **Cota Superior:** Para cualquier $x \in \mathbb{R}^n$, expandiendo $\|Ax\|_1$:
  $$\|Ax\|_1 = \sum_{i=1}^m \left| \sum_{j=1}^n a_{ij} x_j \right| \le \sum_{j=1}^n |x_j| \sum_{i=1}^m |a_{ij}| \le \left( \max_{1 \le j \le n} \sum_{i=1}^m |a_{ij}| \right) \|x\|_1$$
  Dividiendo por $\|x\|_1$ y tomando el supremo para $x \neq 0$, se obtiene $\|A\|_1 \le \max_{j} \sum_{i=1}^m |a_{ij}|$.

- **Cota Inferior:** Sea $l$ la columna donde se alcanza el máximo. Evaluando en el vector canónico $e_l$ (que tiene $\|e_l\|_1 = 1$):
  $$\|A\|_1 \ge \|A e_l\|_1 = \sum_{i=1}^m |a_{il}| = \max_{1 \le j \le n} \sum_{i=1}^m |a_{ij}|\quad \blacksquare$$
---

# Demostración: Fórmula de la Norma-Infinito

Queremos probar que $\|A\|_\infty = \max_{i} \sum_{j=1}^n |a_{ij}|$.

- **Cota Superior:** Para cualquier $x \in \mathbb{R}^n$, expandiendo $\|Ax\|_\infty$:
  $$\|Ax\|_\infty = \max_{1 \le i \le m} \left| \sum_{j=1}^n a_{ij} x_j \right| \le \max_{1 \le i \le m} \sum_{j=1}^n |a_{ij}| |x_j| \le \left( \max_{1 \le i \le m} \sum_{j=1}^n |a_{ij}| \right) \|x\|_\infty$$
  Por lo tanto, al dividir por $\|x\|_\infty$, se obtiene $\|A\|_\infty \le \max_{i} \sum_{j=1}^n |a_{ij}|$.

- **Cota Inferior:** Sea $l$ la fila que maximiza la suma. Definimos $\hat{x}$ tal que $\hat{x}_j = 1$ si $a_{lj} \ge 0$ y $\hat{x}_j = -1$ si $a_{lj} < 0$. Como $\|\hat{x}\|_\infty = 1$:
  $$\|A \hat{x}\|_\infty = \max_i \left| \sum_{j=1}^n a_{ij} \hat{x}_j \right| \ge \left| \sum_{j=1}^n a_{lj} \hat{x}_j \right| = \sum_{j=1}^n |a_{lj}| = \max_{1 \le i \le m} \sum_{j=1}^n |a_{ij}| \quad \blacksquare$$

---

# Demostración: Fórmula de la Norma-2 (Espectral)

Queremos probar que $\|A\|_2^2 = \rho(A^T A)$.

El cuadrado de la norma inducida es la solución del problema de optimización:
$$\|A\|_2^2 = \max_{\\|x\\|_2=1} \|Ax\|_2^2 \quad \text{sujeto a} \quad h(x) = \|x\|_2^2 - 1 = 0$$

Definiendo la lagrangiana $f(x) = -\|Ax\|_2^2$ y aplicando multiplicadores de Lagrange:
$$\nabla f(x) + \bar{\lambda} \nabla h(x) = 0 \implies -2A^T A x + 2\bar{\lambda} x = 0 \implies A^T A x = \bar{\lambda} x$$

Por lo tanto, el vector que alcanza el óptimo es un autovector de $A^T A$. Evaluando la forma cuadrática para un autovector normalizado $v$ asociado al autovalor $\lambda$:
$$\|A v\|_2^2 = v^T A^T A v = v^T (\lambda v) = \lambda \le \rho(A^T A) \implies \|A\|_2^2 = \rho(A^T A) \quad \blacksquare$$

---

# Número de Condición $\kappa(A)$

**Definición:** Para una matriz no singular $A \in \mathbb{R}^{n \times n}$, su __número de condición__ es:
$$\kappa(A) = \|A\| \|A^{-1}\| $$

### Interpretación Geométrica
Como $\|A^{-1}\| = 1 / \min_{\|x\|=1} \|Ax\|$, el número de condición mide la relación entre la distorsión máxima y mínima de la esfera unidad bajo $A$:
$$\kappa(A) = \frac{\max_{\|x\|=1} \|Ax\|}{\min_{\|x\|=1} \|Ax\|} $$

- **En Norma-2:** Se calcula usando los autovalores extremos de $A^T A$:
  $$\kappa_2(A) = \frac{\sigma_{\max}}{\sigma_{\min}} = \sqrt{\frac{\lambda_{\max}(A^T A)}{\lambda_{\min}(A^T A)}} $$

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

### Demostración:
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

Agrupando los términos con $\|\zeta\|$ a la izquierda de la desigualdad:
$$\left(1 - \|A^{-1}\| \|\Theta\|\right) \|\zeta\| \le \|A^{-1}\| \left( \|\Theta\| \|\bar{x}\| + \|\vartheta\| \right)$$

Dividiendo por $\|\bar{x}\|$ e introduciendo el término $\|A\|$ de manera conveniente:
$$\left(1 - \kappa(A) \frac{\|\Theta\|}{\|A\|}\right) \frac{\|\zeta\|}{\|\bar{x}\|} \le \kappa(A) \left( \frac{\|\Theta\|}{\|A\|} + \frac{\|\vartheta\|}{\|A\| \|\bar{x}\|} \right)$$

Dado que $\|b\| = \|A\bar{x}\| \le \|A\|\|\bar{x}\|$, se cumple $\frac{1}{\|A\|\|\bar{x}\|} \le \frac{1}{\|b\|}$. Al despejar, se verifica la cota del teorema. $\blacksquare$
