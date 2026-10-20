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

Evitan el cálculo explícito de la Jacobiana $F'(x^k)$ reemplazándola por una matriz de aproximación $M_k$ en el sistema $M_k d^k = -F(x^k)$.

- **Diferencias Finitas:** Aproxima cada columna de $M_k$ mediante $M_{*,j} = \frac{1}{h}[F(x + h e_j) - F(x)]$ tomando $h = \sqrt{\epsilon_{\text{máq}}} \|x\|$.
- **Ecuación Secante:** Exige que la actualización $M_{k+1}$ satisfaga $M_{k+1} d^k = y^k$, donde $y^k = F(x^{k+1}) - F(x^k)$ y $d^k = x^{k+1} - x^k$.
- **Actualización de Broyden (Algoritmo 37):** Utiliza una actualización de rango 1 sobre la matriz inversa $W_k = M_k^{-1}$, permitiendo calcular $d^k = -W_k F(x^k)$ directamente con un producto matriz-vector de costo $O(n^2)$:
  $$W_{k+1} = W_k + \frac{(d^k - W_k y^k) (y^k)^T}{(y^k)^T y^k}$$

---

# Aplicación: Localización por GPS (Trilateración)

- **Trilateración ideal:** Un receptor GPS (tu celular) no conoce sus coordenadas $(x, y)$. En cambio, se comunica con satélites cuyas posiciones $(x_i, y_i)$ son conocidas con precisión. Midiendo el tiempo de llegada de la señal, el receptor calcula la distancia $d_i$ a cada satélite. Geométricamente, el celular sabe que está ubicado en una circunferencia de radio $d_i$ centrada en $(x_i, y_i)$.Para 3 satélites (en 2D), plantearíamos el siguiente sistema:

$$f_i(x, y) = \sqrt{(x - x_i)^2 + (y - y_i)^2} - d_i = 0 \quad \text{para } i = 1, 2, 3$$

---

- **Conflicto real:** En la práctica, nos enfrentamos a dos grandes problemas matemáticos y físicos: **Sobredeterminación**: Tenemos 3 ecuaciones pero solo 2 incógnitas ($x, y$). **Ruido en las mediciones**: Las distancias calculadas $d_i$ nunca son perfectas (retrasos atmosféricos, rebotes, desincronización de relojes). Consecuencia geométrica: Las tres circunferencias nunca se intersecan en un único punto. El sistema de ecuaciones $F(x,y) = 0$ no tiene solución exacta.

---

# Cuadrados Mínimos No Lineales

Cuando $F: \mathbb{R}^n \to \mathbb{R}^m$ con $m \neq n$ o la Jacobiana es singular, se reformula el problema como la minimización de la norma del residuo:
$$\min_{x \in \mathbb{R}^n} f(x), \quad \text{donde } f(x) = \frac{1}{2} \|F(x)\|_2^2$$

- El gradiente de $f(x)$ satisface $\nabla f(x) = F'(x)^T F(x)$.
- Suponga que $F$ es diferenciable. Se cumple que $F(x^*) = 0$ si y solo si $\nabla f(x^*) = 0$ y existe $d$ tal que $F(x^*) + F'(x^*) d = 0$.
- La función objetivo $f(x)$ puede presentar minimizadores locales donde $F(x) \neq 0$ ($\nabla f(x^*) = 0$ con $F(x^*) \neq 0$).

---

# Minimización No Lineal: Condiciones de Optimalidad

Para hallar el minimizador de $f: \mathbb{R}^n \to \mathbb{R}$ en problemas sin restricciones ($\min_{x \in \mathbb{R}^n} f(x)$):

- $x^*$ es un minimizador local si existe $\epsilon > 0$ tal que $f(x^*) \le f(x)$ para todo $x \in \mathcal{B}(x^*, \epsilon)$.
- Si $f$ es diferenciable en $x^*$, entonces $\nabla f(x^*) = 0$ (punto estacionario).
- Si $f$ es dos veces diferenciable en $x^*$, la matriz Hessiana $\nabla^2 f(x^*)$ es semidefinida positiva.
- Si $f$ es dos veces diferenciable, $\nabla f(x^*) = 0$ y $\nabla^2 f(x^*)$ es definida positiva, entonces $x^*$ es un minimizador local estricto.

---

# Búsqueda Lineal y Reglas de Selección de Paso

Un algoritmo de búsqueda lineal genera la sucesión $x_{k+1} = x_k + \alpha_k d_k$, con una dirección de descenso $\nabla f(x_k)^T d_k < 0$ y un tamaño de paso $\alpha_k > 0$.

- Si $\nabla f(x)^T d < 0$, para todo $\tau \in (0, 1)$ existe $\delta > 0$ tal que $f(x + \alpha d) \le f(x) + \tau \alpha \nabla f(x)^T d$ para $\alpha \in (0, \delta]$.
- La regla de Armijo inicia con $\alpha = 1$ y reduce el paso por un factor $\beta \in (0, 1)$ hasta satisfacer la condición de descenso suficiente $f(x_k + \alpha d_k) \le f(x_k) + \tau \alpha \nabla f(x_k)^T d_k$.
- La regla de Goldstein agrega una cota inferior al paso para evitar desplazamientos excesivamente pequeños: $f(x_k) + (1-\tau)\alpha \nabla f(x_k)^T d_k \le f(x_k + \alpha d_k) \le f(x_k) + \tau \alpha \nabla f(x_k)^T d_k$.

---

# Elección de Direcciones de Búsqueda Lineal

- La dirección de Cauchy o máximo descenso elige $d_k = -\nabla f(x_k)$, garantizando $\nabla f(x_k)^T d_k = -\|\nabla f(x_k)\|_2^2 < 0$.
- La dirección de Newton resuelve $\nabla^2 f(x_k) d_k = -\nabla f(x_k)$. Si $\nabla^2 f(x_k)$ es definida positiva, $d_k$ es una dirección de descenso.
- Si $\nabla^2 f(x_k)$ no es definida positiva, se modifica la diagonal durante Cholesky reemplazando $G_{ii} \le \epsilon_0$ por $\epsilon_1$, resolviendo el sistema con $G^T G = \nabla^2 f(x_k) + E_k > 0$.

---

# Métodos Específicos de Minimización y Convergencia

- **Dirección de Gauss-Newton:** Para $f(x) = \frac{1}{2}\|F(x)\|_2^2$, aproxima $\nabla^2 f(x_k) \approx F'(x_k)^T F'(x_k)$, evitando calcular $\nabla^2 F_i(x_k)$.
- **Método de Levenberg-Marquardt:** Regulariza Hessiana de Gauss-Newton agregando $H_k = F'(x_k)^T F'(x_k) + \gamma_k I$ con $\gamma_k > 0$ y garantiza definición positiva.
- **Dirección BFGS para Minimización:** Actualiza iterativamente la matriz inversa de la Hessiana $W_k \approx (\nabla^2 f(x_k))^{-1}$ preservando simetría y definición positiva.
- **Teorema:** Si $\{x_k\}$ se genera por Armijo y $\nabla f(x_k)^T d_k \le -\gamma \|\nabla f(x_k)\|^q$, todo punto límite de $\{x_k\}$ es un punto estacionario ($\nabla f(x^*) = 0$).
