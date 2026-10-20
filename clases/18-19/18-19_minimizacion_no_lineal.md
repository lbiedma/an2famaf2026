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
## Clase 18: Ecuaciones No Lineales y Minimización
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Aplicación: Control de Vuelo Bajo Viento

![center](https://www.photopills.com/sites/default/files/articles/drone-photography/drone-pitch-es.webp)

---

# Sistema No Lineal: Equilibrio de fuerzas para mantener la posición

Para que el dron flote estacionario (derivadas segundas nulas), la sumatoria de fuerzas debe ser nula. Buscamos el Empuje total ($T$) y la Inclinación ($\theta$):

### Eje Horizontal (Balance de viento y empuje)

$$f_1''(T, \theta) = -T \sin(\theta) + F_{drag}(\theta) = 0$$

### Eje Vertical (Balance de peso y sustentación):

$$f_2''(T, \theta) = T \cos(\theta) - mg = 0$$

⚠️ Solución analítica imposible: El sistema presenta productos fuertemente acoplados entre $T$ y las funciones trigonométricas de $\theta$.

---

# Vuelo estacionario contra ráfagas horizontales

Cuando un dron intenta mantenerse en una posición fija pero se enfrenta a viento horizontal, debe inclinar su estructura:

- 💨 Inclinación obligatoria contra el viento para generar empuje horizontal.
- 📐 Área aerodinámica variable dependiendo del ángulo de inclinación $\theta$.
- 🌊 Fuerza de arrastre no constante (modelo no lineal).

### Modelo de Arrastre Aerodinámico

$$F_{\text{drag}}(\theta) = K_w (\cos(\theta) + \alpha \sin(\theta))$$

(Donde $\alpha$ es la proporción entre el área superior y el área lateral del dron).

---

# Cómo queda nuestro sistema?

$$
\begin{cases}
f_1''(T, \theta) = -T \sin(\theta) + K_w (\cos(\theta) + \alpha \sin(\theta)) = 0 \\
f_2''(T, \theta) = T \cos(\theta) - mg = 0
\end{cases}
$$

- Cómo despejamos $T$ y $\theta$ de este sistema? :thinking:

- Y cómo podemos resolver la ecuación diferencial cada vez que el dron se inclina o cambia la fuerza de arrastre (muchas veces por segundo)? :thinking::thinking::thinking:

---

# Ecuaciones No Lineales

Sea $F : \mathbb{R}^n \to \mathbb{R}^m$. Buscamos un $x^* \in \mathbb{R}^n$ tal que

$$
\begin{cases}
f_1(x^*) = 0 \\
f_2(x^*) = 0 \\
\vdots \\
f_m(x^*) = 0
\end{cases}
$$

Los problemas no lineales pueden resolverse numéricamente mediante una sucesión de subproblemas lineales que aproximan localmente al problema original.

---

# Definiciones
- Sean $\psi : \mathbb{R}^n \to \mathbb{R}^m$ y $\phi : \mathbb{R}^n \to \mathbb{R}^p$ definidas en un entorno de $x^* \in \mathbb{R}^n$. Diremos que $\psi$ es **dominada** por $\phi$ en un entorno de $x^*$, denotado por $\psi(x) = O(\phi(x))$, si existen $\kappa > 0$ y $\delta > 0$ tal que $\|\psi(x)\| \le \kappa \|\phi(x)\|$ para todo $x \in \mathcal{B}(x^*, \delta)$.
- Diremos que $\psi$ es **despreciable** comparada con $\phi$ en un entorno de $x^*$, denotado por $\psi(x) = o(\phi(x))$, si para todo $\varepsilon > 0$ existe $\delta > 0$ tal que $\|\psi(x)\| \le \varepsilon \|\phi(x)\|$ para todo $x \in \mathcal{B}(x^*, \delta)$.


---

# Método de Newton para Sistemas No Lineales

Si $F: \mathbb{R}^n \to \mathbb{R}^m$ es diferenciable en $x^k$, entonces su desarrollo de primer orden es:

$$F(x^k) + F'(x^k)(x - x^k) = 0$$

Por lo tanto, podemos construir la siguiente iteración:

$$x^{k+1} = x^k + d_k$$

donde $d_k$ resuelve el sistema lineal $F'(x^k) d_k = -F(x^k)$.

---

# Algoritmo: Método de Newton

**Entradas:** $F : \mathbb{R}^n \to \mathbb{R}^n$, $x^0 \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$. **Salida:** $x^+$ aprox. de $x^*$.

1. Definir $x = x^0$ y $r = F(x)$, $M = F'(x)$ y $\sigma = \|r\|$.
2. Para $k = 1, \dots, m$, si $\sigma \le \epsilon$, ir al paso 3. Sino, definir
  $$
  \begin{aligned}
  & d \quad \text{t.q. } r + Md = 0 \\
  & x \leftarrow x + d, \\
  & r = F(x), \\
  & M = F'(x), \\
  & \sigma = \|r\|.
  \end{aligned}
  $$
3. Retornar $x^+ = x$.

Cuál es el garrón más grande acá?

---

# Convergencia y Velocidad de Convergencia

**Definiciones:** Diremos que una sucesión $\{x^k\}$ converge a $x^*$ con tasa:
- **Lineal** si $\displaystyle\limsup_{k \to \infty} \frac{\|x^{k+1} - x^*\|}{\|x^k - x^*\|} < 1$,
- **Superlineal** si $\|x^{k+1} - x^*\| = o(\|x^k - x^*\|)$,
- **Cuadrática** si $\|x^{k+1} - x^*\| = O(\|x^k - x^*\|^2)$.

**Teorema:** Sea $F : \mathbb{R}^n \to \mathbb{R}^n$ continuamente diferenciable en un entorno de $x^*$, con $F(x^*) = 0$ y $F'(x^*)$ no singular. Entonces existe $\varepsilon > 0$ tal que si $\|x^0 - x^*\| \le \varepsilon$, la sucesión $\{x^k\}$ generada por el método de Newton converge **superlinealmente** a $x^*$.
Si además $\|F'(\tilde{x}) - F'(x)\| \le \ell \|\tilde{x} - x\|$ para todo $\tilde{x}, x$ en un entorno de $x^*$, entonces $\{x^k\}$ converge **cuadráticamente** a $x^*$.

---

# Método de Newton Truncado (Inexacto)

En problemas de gran dimensión, resolver el sistema lineal de Newton de forma exacta resulta numéricamente costoso.

- Se acepta un paso $d_k$ que satisface $\|F(x_k) + F'(x_k) d_k\| \le \eta_k \|F(x_k)\|$, donde $\{\eta_k\}$ es la "sucesión forzante".
- Se define $\eta_k = \min\{\gamma, \|F(x_k)\|^\delta\}$ con $\gamma, \delta \in (0, 1)$.
- El sistema lineal $F'(x_k) d = -F(x_k)$ se resuelve inexactamente utilizando GMRES, deteniendo la iteración cuando el residuo alcance la tolerancia $\eta_k \|F(x_k)\|$.
- Si $\eta_0 \le \delta$ y $x_0$ está suficientemente cerca de $x^*$, $\{x_k\}$ converge linealmente; si además $\eta_k \to 0^+$, la convergencia es superlineal.

---

# Algoritmo: Método de Newton Truncado

**Entradas:** $F : \mathbb{R}^n \to \mathbb{R}^n$, $x^0 \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$. **Salida:** $x^+$ aprox. de $x^*$.

1. Definir $x = x^0$, $\gamma, \delta \in (0, 1)$, $r = F(x)$, $M = F'(x)$ y $\sigma = \|r\|_2$.
2. Para $k = 1, \dots, m$, si $\sigma \le \epsilon$, ir al paso 3. Sino, definir
  $$
  \begin{aligned}
  & \eta = \min\{\gamma, \sigma^\delta\}, \\
  & d \leftarrow \text{GMRES}(M, -r, 0, \eta\sigma), \\
  & x \leftarrow x + d, \\
  & r = F(x), \\
  & M = F'(x), \\
  & \sigma = \|r\|_2.
  \end{aligned}
  $$
3. Retornar $x^+ = x$.


---

# Métodos Cuasi-Newton

- A veces no tendremos la Jacobiana disponible, o será muy costoso calcularla, entonces debemos aproximarla.
- Los métodos cuasi-Newton evitan el cálculo explícito de la Jacobiana $F'(x^k)$ reemplazándola por una matriz de aproximación $M_k$ en el sistema $M_k d^k = -F(x^k)$.
- En las condiciones correctas, estos métodos convergen con tasa superlineal.

---

# Métodos Cuasi-Newton: Ejemplos
- **Diferencias Finitas:** Aproxima cada columna de $M_k$ mediante $M_{*,j} = \frac{1}{h}[F(x + h e_j) - F(x)]$ tomando $h = \sqrt{\epsilon_{\text{máq}}} \|x\|$.
- **Ecuación Secante:** Exige que la actualización $M_{k+1}$ satisfaga $M_{k+1} d^k = y^k$, donde $y^k = F(x^{k+1}) - F(x^k)$ y $d^k = x^{k+1} - x^k$.
- **Actualización de Broyden:** Actualización de rango 1 sobre matriz inversa $W_k = M_k^{-1}$, permitiendo calcular $d^k = -W_k F(x^k)$ con producto matriz-vector:
$$W_{k+1} = W_k + \frac{(d^k - W_k y^k) (y^k)^T}{(y^k)^T y^k}$$

---

# Algoritmo: Método de Broyden

**Entradas:** $F : \mathbb{R}^n \to \mathbb{R}^n$, $x^0 \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$. **Salida:** $x^+$ aprox. de $x^*$.

1. Definir $x = x^0$, obtener $r = F(x)$, $W = I$.
2. Para $k = 1, \dots, m$, si $\|r\| \le \epsilon$, ir al paso 3. Sino, definir:
  $$
  \begin{aligned}
  d &= -Wr, \\
  x &\leftarrow x + d, \\
  r^+ &= F(x), \\
  y &= r^+ - r, \\
  v &= Wy, \\
  W &\leftarrow W + (d - v)y^{\text{T}} / (y^{\text{T}}y), \\
  r &= r^+.
  \end{aligned}
  $$
3. Retornar $x^+ = x$.

---

# Aplicación: Localización por GPS

![center](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5TJ5UtXQaG5nO4MOVOVbcOgaKvtkDpwTJWImGg0M2kJc9z9dIl-Y8rao&s=10)

---

# Aplicación: Localización por GPS (Trilateración)

- Un receptor GPS se comunica con satélites cuyas posiciones $(x_i, y_i)$ son conocidas con precisión para ubicarse.
- Midiendo el tiempo de llegada de la señal, se calcula la distancia $d_i$ a cada satélite.
- Geométricamente, el receptor sabe que está ubicado en una circunferencia de radio $d_i$ centrada en $(x_i, y_i)$.
- Para 3 satélites (en 2D), plantearíamos el siguiente sistema:

$$f_i(x, y) = \sqrt{(x - x_i)^2 + (y - y_i)^2} - d_i = 0 \quad \text{para } i = 1, 2, 3$$

- Este sistema tiene solución?

---

# Cuadrados Mínimos No Lineales

Cuando $F: \mathbb{R}^n \to \mathbb{R}^m$ con $m \neq n$ o la Jacobiana es singular, se reformula el problema como la minimización de la norma del residuo:
$$\min_{x \in \mathbb{R}^n} f(x) = \frac{1}{2} \|F(x)\|_2^2$$

- $f(x)$ es diferenciable si $F$ es diferenciable.
$$
\begin{aligned}
f(x + h) &= \frac{1}{2} \|F(x + h)\|_2^2 = \frac{1}{2} \|F(x) + F'(x)h + o(\|h\|)\|_2^2 \\
&= \frac{1}{2} \left( \|F(x)\|_2^2 + 2F(x)^{\text{T}} F'(x)h + \|F'(x)h\|_2^2 + o(\|h\|) \right) \\
&= f(x) + \left(F'(x)^{\text{T}} F(x)\right)^{\text{T}} h + o(\|h\|).
\end{aligned}
$$

---

# Cuadrados Mínimos No Lineales

- El gradiente de $f(x)$ satisface $\nabla f(x) = F'(x)^T F(x)$.
- Suponga que $F$ es diferenciable. Se cumple que $F(x^*) = 0$ si y solo si $\nabla f(x^*) = 0$ y existe $d$ tal que $F(x^*) + F'(x^*) d = 0$.
- La función objetivo $f(x)$ puede presentar minimizadores locales donde $F(x) \neq 0$ ($\nabla f(x^*) = 0$ con $F(x^*) \neq 0$).
- **Proposición:** Sea $F: \mathbb{R}^n \to \mathbb{R}^m$ diferenciable y $f(x) = \frac{1}{2} \|F(x)\|_2^2$. Entonces $F(x^*) = 0$ si y solo si $\nabla f(x^*) = 0$ y existe $d$ tal que $\nabla F(x^*) d = -F(x^*)$.


---

# Marco General de la Minimización No Lineal

Dado un problema con dominio $\mathcal{D} \subset \mathbb{R}^n$, se busca hallar un vector $x^*$ que resuelva:
$$\min_{x \in \mathcal{D}} f(x) \quad$$

**Definiciones:**
- **Función Objetivo:** La función $f: \mathbb{R}^n \to \mathbb{R}$ a minimizar.
- **Conjunto Factible:** El subconjunto de $\mathbb{R}^n$ donde se busca la solución.
- **Valor Mínimo:** $v_* = \inf_{x \in \mathcal{D}} f(x) \in [-\infty, +\infty]$.
- **Minimizador Global:** $x^* \in \mathcal{D}$ tal que $f(x^*) \le f(x)$ para todo $x \in \mathcal{D}$.
- **Minimizador Local:** $x^* \in \mathcal{D}$ si existe $\epsilon > 0$ tal que $f(x^*) \le f(x)$ para todo $x \in \mathcal{B}(x^*, \epsilon) \cap \mathcal{D}$.

---

# Condiciones de Optimalidad

### Teorema (Condiciones Necesarias de Optimalidad):
Sea $x^*$ un minimizador local de $f$ en $\mathbb{R}^n$:
1. **Primer orden:** Si $f$ es diferenciable en $x^*$, entonces $\nabla f(x^*) = 0$.
2. **Segundo orden:** Si $f$ es dos veces diferenciable en $x^*$, entonces la matriz Hessiana $\nabla^2 f(x^*)$ es semidefinida positiva.

---

# Condiciones de Optimalidad

### Definición (Punto Estacionario)
Un punto $x^* \in \mathbb{R}^n$ es un punto estacionario si satisface $\nabla f(x^*) = 0$.

### Teorema (Condición Suficiente de Optimalidad)
Si $f$ es dos veces diferenciable en $x^*$, $\nabla f(x^*) = 0$ y $\nabla^2 f(x^*)$ es **definida positiva**, entonces $x^*$ es un minimizador local de $f$. Existen $\epsilon > 0$ y $\gamma > 0$ tales que:
$$f(x) \ge f(x^*) + \frac{\gamma}{2} \|x - x^*\|^2, \quad \forall x \in \mathcal{B}(x^*, \epsilon) \quad$$

---

# Esquema General de Búsqueda Lineal

Los algoritmos de **búsqueda lineal** generan una sucesión $x_{k+1} = x_k + \alpha_k d_k$:

1. Dar $x_0 \in \mathbb{R}^n$ y $k = 0$.
2. Si $\|\nabla f(x_k)\| = 0$, detener el proceso (punto estacionario alcanzado).
3. Obtener una **dirección de descenso** $d_k \in \mathbb{R}^n$ tal que $\nabla f(x_k)^T d_k < 0$.
4. Obtener un **tamaño de paso** $\alpha_k > 0$ tal que $f(x_k + \alpha_k d_k) < f(x_k)$.
5. Definir $x_{k+1} = x_k + \alpha_k d_k$, hacer $k \leftarrow k + 1$ y regresar al Paso 1.

*Al finalizar el proceso, debe verificarse si la Hessiana $\nabla^2 f(x_{k+1})$ es definida positiva.*

---

# Algoritmo: Regla de Armijo (Selección del Paso)

Garantiza un **descenso suficiente** reduciendo el paso inicial $\alpha = 1$ mediante un factor $\beta \in (0, 1)$ hasta satisfacer $\phi(\alpha) \le \phi_0 + \tau \alpha \phi'_0$, con $\tau \in (0, 1)$.

**Entradas:** $f: \mathbb{R}^n \to \mathbb{R}$, $x, d \in \mathbb{R}^n$, $\phi_0 = f(x)$, $\phi'_0 = \nabla f(x)^T d$, $m \in \mathbb{N}$, $\tau, \beta \in (0, 1)$.
**Salida:** $x^+ = x + \alpha d$.
1. Definir $\alpha = 1$.
2. Para $k = 1, \dots, m$, definir $x^+ = x + \alpha d$, $\phi = f(x^+)$.
   Si $\phi \le \phi_0 + \tau \alpha \phi'_0$, ir al paso 3. Sino, hacer $\alpha \leftarrow \beta \alpha$.
3. Retornar $x^+$.

*En la práctica se utilizan típicamente $\beta = 0.5$ y $\tau = 10^{-4}$.*

---

# Algoritmo: Regla de Goldstein (Selección del Paso)

Evita que el paso $\alpha$ sea demasiado pequeño imponiendo una **cota inferior y superior** sobre el incremento funcional mediante el parámetro $\tau \in (0, 1/2)$.

**Entradas:** $f: \mathbb{R}^n \to \mathbb{R}$, $x, d \in \mathbb{R}^n$, $\phi_0, \phi'_0 \in \mathbb{R}$, $m \in \mathbb{N}$, $\tau \in (0, 1/2)$, $\beta \in (0, 1)$, $\rho > 1$.
**Salida:** $x^+ = x + \alpha d$.
1. Definir $\alpha = 1$, $\alpha_l = 0$ y $\alpha_u = +\infty$.
2. Para $k = 1, \dots, m$, definir $x^+ = x + \alpha d$, $\phi = f(x^+)$.
   - Si $\phi \le \phi_0 + \alpha \tau \phi'_0$, ir al paso 2 si $\phi \ge \phi_0 + \alpha (1 - \tau) \phi'_0$ o hacer $\alpha_l = \alpha$ caso contrario. Sino, hacer $\alpha_u = \alpha$.
   - Definir $\alpha = (1 - \beta)\alpha_l + \beta \alpha_u$ si $\alpha_u < +\infty$, o $\rho \alpha_l$ si $\alpha_u = +\infty$.
3. Retornar $x^+.$

---

# Estrategias Alternativas para la Selección del Paso

Además de las reglas de Armijo y Goldstein, existen otras maneras de determinar $\alpha_k$:

- **Paso Exacto:** Se toma $\alpha_k = \arg\min_{\alpha \ge 0} f(x_k + \alpha d_k)$. Se utiliza cuando la minimización unidimensional se deduce analíticamente mediante una fórmula cerrada (ej. métodos de proyección).
- **Paso Menguante:** Se predefine una sucesión $\{\alpha_k\}$ que satisface $\alpha_k \to 0^+$ y $\sum_{k=0}^\infty \alpha_k = +\infty$. Se aplica si la evaluación funcional de $f(x)$ es muy costosa.
- **Paso Constante:** Se fija $\alpha_k = \alpha > 0$ siempre. Sólo se aconseja en problemas con estructura particular y cotas espectrales conocidas.

---

# Algoritmo: Método de Cauchy para Minimización

Utiliza la dirección de **máximo descenso** $d_k = -\nabla f(x_k)$, que resulta de minimizar $\nabla f(x_k)^T d$ sobre la bola $\|\cdot\|_2 \le 1$.

**Entradas:** $f: \mathbb{R}^n \to \mathbb{R}$, $x \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$.
**Salida:** $x^+$ aproximación de $x^*$.
1. Obtener $\phi = f(x)$, $r = \nabla f(x)$ y definir $\sigma = \|r\|_2$.
2. Para $k = 1, \dots, m$, si $\sigma \le \epsilon$, ir al paso 3. Sino, definir:
   - $x$ aplicando el **Algoritmo (Armijo)** con $\phi_0 = \phi$ y $\phi'_0 = -\sigma^2$.
   - $\phi = f(x)$, $r = \nabla f(x)$, $\sigma = \|r\|_2$.
3. Retornar $x^+ = x$.

---

# Algoritmo: Método de Newton para Minimización

Resuelve el sistema de segundo orden $\nabla^2 f(x_k) d_k = -\nabla f(x_k)$ derivado de la condición de estacionariedad $\nabla f(x) = 0$.

**Entradas:** $f: \mathbb{R}^n \to \mathbb{R}$, $x \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$. **Salida:** $x^+$ aproximación de $x^*$.
1. Obtener $\phi = f(x)$, $r = \nabla f(x)$ y $H = \nabla^2 f(x)$.
2. Para $k = 1, \dots, m$, si $\|r\|_2 \le \epsilon$, ir al paso 3. Sino, definir:
   - $d$ tal que $r + H d = 0$ resolviendo el sistema SDP mediante Cholesky.
   - $x$ aplicando Armijo con $\phi_0 = \phi$ y $\phi'_0 = r^T d$.
   - $\phi = f(x)$, $r = \nabla f(x)$, $H = \nabla^2 f(x)$.
3. Retornar $x^+ = x$.

---

# Modificaciones del Método de Newton

Cuando $f$ no es estrictamente convexa, la Hessiana $\nabla^2 f(x_k)$ puede ser indefinida o singular. Se aplican modificaciones para garantizar la definición positiva:

- **Cholesky Modificado:** Reemplaza los pivotes $G_{ii} \le \epsilon_0$ por $\epsilon_1 > \epsilon_0 \ge 0$ antes de calcular la raíz cuadrada, asegurando $G^T G = \nabla^2 f(x_k) + E_k > 0$.
- **Dirección de Gauss-Newton:** Para problemas de cuadrados mínimos no lineales $f(x) = \frac{1}{2}\|F(x)\|_2^2$, se aproxima la Hessiana omitiendo las derivadas de segundo orden: $H_k = F'(x_k)^T F'(x_k) \ge 0$.
- **Método de Levenberg-Marquardt:** Regulariza la matriz de Gauss-Newton sumando un término diagonal $\gamma_k I$ con $\gamma_k > 0$: $H_k = F'(x_k)^T F'(x_k) + \gamma_k I > 0$.

---

# Algoritmo: Método BFGS para Minimización

Implementa la actualización secante de rango 2 para la inversa de la Hessiana $W_k \approx (\nabla^2 f(x_k))^{-1}$, permitiendo calcular $d = -W r$ con un producto matriz-vector.

**Entradas:** $f: \mathbb{R}^n \to \mathbb{R}$, $x \in \mathbb{R}^n$, $\epsilon > 0$ y $m \in \mathbb{N}$.

1. Obtener $\phi = f(x)$, $r = \nabla f(x)$, definir $W = I$ y $x^+ = x$.
2. Para $k = 1, \dots, m$, si $\|r\|_2 \le \epsilon$, ir al paso 2. Sino, definir:
   - $d = -W r$, $x^+$ aplicando Armijo con $\phi_0 = f(x)$ y $\phi'_0 = r^T d$.
   - $\phi = f(x^+)$, $r^+ = \nabla f(x^+)$, $y = r^+ - r$, $v = x^+ - x$, $w = W y$.
   - $\gamma = y^T v$, $\tau = y^T w$, $p = v/\gamma - w/\tau$.
   - $W = W + \frac{v v^T}{\gamma} - \frac{w w^T}{\tau} + \tau p p^T$, $x = x^+$, $r = r^+$.
3. Retornar $x^+$.

---

# Convergencia del Método de Búsqueda Lineal

- **Peligro de las Búsquedas Unidimensionales:**
  Dada $f(x_1, x_2) = (x_2 - p x_1^2)(x_2 - q x_1^2)$ con $0 < p < q$, el origen $(0,0)$ es un minimizador local a lo largo de **toda recta** que pasa por él, pero **no es un minimizador local en $\mathbb{R}^2$**.
- **Teorema:** Sea $f$ continuamente diferenciable y $\{x_k\}$ generada por un método de búsqueda lineal con paso de Armijo y dirección que satisface $\nabla f(x_k)^T d_k \le -\gamma \|\nabla f(x_k)\|^q$ con $\gamma, q > 0$. Entonces todo punto límite $x^*$ de la sucesión $\{x_k\}$ es un **punto estacionario** ($\nabla f(x^*) = 0$).