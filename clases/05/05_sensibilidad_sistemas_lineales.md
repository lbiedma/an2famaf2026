---
marp: true
theme: default
paginate: true
_class: invert
---

# Sensibilidad de Sistemas Lineales
## Análisis de Estabilidad y Teoría de Normas
### Notas de Álgebra Lineal Numérica (FAMAF)

---

# 1. Introducción: ¿Por qué importa la sensibilidad numérica?

Al resolver un sistema lineal $Ax = b$ mediante una computadora, existen limitaciones físicas inevitables debido a la representación finita de los números [105].

- El sistema que realmente se termina resolviendo es un sistema perturbado [105]:
  $$(A + \Theta)\hat{x} = b + \vartheta$$
  donde $\Theta \in \mathbb{R}^{n \times n}$ y $\vartheta \in \mathbb{R}^n$ representan pequeñas perturbaciones producidas por la aritmética de punto flotante de doble precisión [105].
- Para cuantificar analíticamente cómo estas perturbaciones alteran la solución exacta, es indispensable introducir herramientas matemáticas que midan la magnitud de vectores y matrices: las **normas** [105].

---

# 2. Definición de Norma (Axiomas)

**Definición 3.1 (Norma):** Una norma en un espacio vectorial $X$ (que en nuestro caso puede ser $\mathbb{R}^n$ o $\mathbb{R}^{m \times n}$) es una función $\|\cdot\|: X \to \mathbb{R}$ que satisface para todo $x, y \in X$ y todo escalar $\alpha \in \mathbb{R}$ [105, 106]:

1. **Positividad y No Degeneración:**
   $$\|x\| \ge 0 \quad \text{y} \quad \|x\| = 0 \iff x = 0 \quad [106]$$
2. **Propiedad Subaditiva (Desigualdad Triangular):**
   $$\|x + y\| \le \|x\| + \|y\| \quad [106]$$
3. **Homogeneidad Absoluta:**
   $$\|\alpha x\| = |\alpha| \|x\| \quad [106]$$

---

# Normas Vectoriales $p$

Dentro de las normas vectoriales en $\mathbb{R}^n$, las de mayor uso en computación científica son las **normas $p$** para $p \ge 1$ [106]:

- Para un valor finito de $p \in [1, \infty)$ [106]:
  $$\|x\|_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p}$$
- El caso límite $p = \infty$ (norma de Chebyshev o del máximo) [107, 112]:
  $$\|x\|_\infty = \max_{1 \le i \le n} |x_i|$$
- Casos particulares clásicos: la **norma de Manhattan** ($p=1$) [111], la **norma Euclídea** ($p=2$) [111], y la **norma de Chebyshev** ($p=\infty$) [112].

---

# 3. Demostración: Las normas $p$ son normas

**Teorema 3.2:** Si $1 \le p \le \infty$, entonces $\|\cdot\|_p$ es una norma vectorial legítima [107].

### Demostración para $p = \infty$:
- **Positividad:** Es evidente que $\|x\|_\infty = \max |x_i| \ge 0$, y es cero si y solo si todos los $x_i = 0$ [107].
- **Homogeneidad:** 
  $$\|\alpha x\|_\infty = \max_{1 \le i \le n} |\alpha x_i| = \max_{1 \le i \le n} \left( |\alpha| |x_i| \right) = |\alpha| \max_{1 \le i \le n} |x_i| = |\alpha| \|x\|_\infty \quad [107]$$
- **Desigualdad Triangular:** Como $|x_i + y_i| \le |x_i| + |y_i| \le \|x\|_\infty + \|y\|_\infty$ para todo $i$ [107]:
  $$\|x+y\|_\infty = \max_{1 \le i \le n} |x_i + y_i| \le \|x\|_\infty + \|y\|_\infty \quad [107]$$

---

# Demostración para $p \in [1, \infty)$

Las propiedades de positividad, no degeneración y homogeneidad absoluta se heredan directamente de las propiedades del valor absoluto [107]. 

Para probar la **desigualdad triangular (Desigualdad de Minkowski)**, recurrimos a la propiedad de convexidad de la función $t \mapsto |t|^p$ para $p \ge 1$ [107]:
$$|(1-\lambda)t_0 + \lambda t_1|^p \le (1-\lambda)|t_0|^p + \lambda |t_1|^p \quad \forall \lambda \in [0, 1] \quad [107, 108]$$

Sean $x, y \in \mathbb{R}^n$ vectores no nulos. Definimos [108]:
$$\hat{x} = \frac{x}{\|x\|_p}, \quad \hat{y} = \frac{y}{\|y\|_p}, \quad \lambda = \frac{\|y\|_p}{\|x\|_p + \|y\|_p} \quad [108]$$
De esta manera, $1 - \lambda = \frac{\|x\|_p}{\|x\|_p + \|y\|_p}$ [108].

---

# Demostración para $p \in [1, \infty)$ (Continuación)

Al evaluar la norma del vector normalizado combinado, obtenemos [108]:
$$\left( \frac{\|x + y\|_p}{\|x\|_p + \|y\|_p} \right)^p = \left\| \frac{\|x\|_p}{\|x\|_p + \|y\|_p} \hat{x} + \frac{\|y\|_p}{\|x\|_p + \|y\|_p} \hat{y} \right\|_p^p = \left\| (1-\lambda)\hat{x} + \lambda\hat{y} \right\|_p^p$$

Desglosando en componentes y aplicando la desigualdad de convexidad [108]:
$$\left\| (1-\lambda)\hat{x} + \lambda\hat{y} \right\|_p^p = \sum_{i=1}^n |(1-\lambda)\hat{x}_i + \lambda\hat{y}_i|^p$$
$$\le \sum_{i=1}^n \left( (1-\lambda)|\hat{x}_i|^p + \lambda|\hat{y}_i|^p \right) \quad [108]$$
$$= (1-\lambda)\|\hat{x}\|_p^p + \lambda\|\hat{y}\|_p^p \quad [108]$$

Dado que $\|\hat{x}\|_p = \|\hat{y}\|_p = 1$, la suma se reduce a $(1-\lambda) + \lambda = 1$, lo que demuestra que $\|x+y\|_p \le \|x\|_p + \|y\|_p$ [108]. $\blacksquare$

---

# 4. Equivalencia de Normas en $\mathbb{R}^n$

**Teorema 3.6:** Si $\||\cdot\||$ es una norma arbitraria en $\mathbb{R}^n$, entonces existen constantes positivas $\alpha, \beta > 0$ tales que para todo $x \in \mathbb{R}^n$ [112]:
$$\alpha \|x\|_2 \le \||x\|| \le \beta \|x\|_2 \quad [112]$$

### Demostración (Cota Superior):
Utilizando la desigualdad de Cauchy-Schwarz, es posible acotar la norma $1$ por la norma Euclídea [108, 113]:
$$\sum_{i=1}^n |x_i| = \sum_{i=1}^n x_i y_i \le \|x\|_2 \|y\|_2 = \sqrt{n} \|x\|_2 \quad [112, 113]$$
Si expresamos $x = \sum_{i=1}^n x_i e_i$ y definimos $\mu = \max_{1 \le i \le n} \|e_i\||$ y $\beta = \sqrt{n}\mu$, por desigualdad triangular obtenemos [113]:
$$\|x\|| = \left\| \sum_{i=1}^n x_i e_i \right\|| \le \sum_{i=1}^n |x_i| \|e_i\|| \le \mu \sum_{i=1}^n |x_i| \le \beta \|x\|_2 \quad [113]$$

---

# Equivalencia de Normas (Cota Inferior)

Por la desigualdad triangular reversa e intercalando la cota superior obtenida [113]:
$$\left| \|y\|| - \|x\|| \right| \le \|y - x\|| \le \beta \|y - x\|_2 \quad [113]$$
Esto demuestra que la función $\||\cdot\||: \mathbb{R}^n \to \mathbb{R}$ es **continua** bajo la métrica Euclídea [113].

Consideremos ahora la esfera unidad Euclídea $S = \{x \in \mathbb{R}^n \mid \|x\|_2 = 1\}$, que es un conjunto cerrado y acotado (compacto) [113]. Por el **Teorema de Weierstrass**, la función continua $\||\cdot\||$ alcanza su valor mínimo en un punto $\bar{x} \in S$ [113, 409]:
$$\alpha = \|\bar{x}\|| > 0 \quad (\text{dado que } \bar{x} \neq 0) \quad [113]$$

Para cualquier $x \neq 0$, el vector normalizado $\frac{x}{\|x\|_2} \in S$, por lo que [113, 114]:
$$\left\| \frac{x}{\|x\|_2} \right\|| \ge \alpha \implies \|x\|| \ge \alpha \|x\|_2 \quad [114]$$
Esto completa las cotas y demuestra que toda norma es equivalente a la Euclídea [114].

---

# Equivalencia entre dos normas cualesquiera

**Corolario 3.7:** Si $\||\cdot\||$ y $\|\cdot\|$ son dos normas cualesquiera en $\mathbb{R}^n$, existen constantes $\alpha, \beta > 0$ tales que para todo $x \in \mathbb{R}^n$ [114]:
$$\alpha \|x\| \le \|x\|| \le \beta \|x\| \quad [114]$$

### Demostración:
Aplicando el Teorema 3.6, sabemos que existen constantes positivas tales que ambas normas se comparan con la norma Euclídea $\|\cdot\|_2$ [114]:
$$\alpha_3 \|x\|_2 \le \|x\|| \le \beta_3 \|x\|_2 \quad [114]$$
$$\alpha_2 \|x\|_2 \le \|x\| \le \beta_2 \|x\|_2 \quad [114]$$

Por lo tanto, encadenando las desigualdades, obtenemos [114, 115]:
$$\frac{\alpha_3}{\beta_2} \|x\| \le \alpha_3 \|x\|_2 \le \|x\|| \le \beta_3 \|x\|_2 \le \frac{\beta_3}{\alpha_2} \|x\| \quad [114, 115]$$
Definiendo $\alpha = \alpha_3 / \beta_2$ y $\beta = \beta_3 / \alpha_2$, se verifica el resultado [114, 115]. $\blacksquare$

---

# 5. Introducción a las Normas Matriciales

Para estudiar el error de sensibilidad en sistemas matriciales, necesitamos extender el concepto de norma al espacio de matrices $X = \mathbb{R}^{m \times n}$ [105, 116].

**Definición 3.10 (Submultiplicatividad):** Se dice que una norma matricial $\|\cdot\|$ es **submultiplicativa** si para cualesquiera matrices compatibles $A$ y $B$ se cumple que [117]:
$$\|AB\| \le \|A\|\|B\| \quad [117]$$

- Esta propiedad es de vital importancia en el análisis de sensibilidad y la convergencia de algoritmos iterativos, ya que nos permite acotar el crecimiento del error en productos matriciales sucesivos.

---

# Ejemplos de Normas Matriciales

1. **Norma de Frobenius (submultiplicativa por construcción) [117]:**
   Identifica la matriz con un vector de dimensión $m \times n$ (usando el operador vec) [116, 117]:
   $$\|A\|_F = \|vec(A)\|_2 = \sqrt{\text{tr}(A^T A)} = \left( \sum_{i=1}^m \sum_{j=1}^n |a_{ij}|^2 \right)^{1/2} \quad [117]$$
2. **Normas Matriciales Inducidas (por normas vectoriales) [119]:**
   Miden el factor de amplificación máxima de un vector bajo la transformación lineal $A$ [119]:
   $$\|A\| = \sup_{x \neq 0} \frac{\|Ax\|}{\|x\|} = \max_{\|x\|=1} \|Ax\| \quad [119, 120]$$
   - *Nota:* Toda norma inducida satisface la propiedad de consistencia $\|Ax\| \le \|A\|\|x\|$ y es estrictamente submultiplicativa [119].
