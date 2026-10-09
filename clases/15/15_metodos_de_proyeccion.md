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
## Clase 15: Métodos de Proyección
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Falta de Acceso al Error

Dada la ecuación lineal $Ax = b$ con $A \in \mathbb{R}^{n \times n}$ no singular, busquemos aproximar la solución exacta $x^*$.

- Nos gustaría tener un algoritmo que minimice el **error exacto** en la iteración $k$:
  $$e^k = x^* - x^k \quad$$

- Para medir o evaluar $e^k$, necesitaríamos conocer previamente $x^*$. ¡Pero $x^*$ es justamente la incógnita que deseamos calcular!
- Ningún algoritmo computable puede basar la elección de la dirección de avance en corregir directamente $e^k$.

---

# Una Alternativa Calculable

Al no tener acceso a $x^*$, recurrimos a la única magnitud medible que evalúa la discrepancia del sistema: el **vector residuo** $r^k$.

>  $$r^k = b - A x^k = A (x^* - x^k) = A e^k \implies e^k = A^{-1} r^k \quad$$

- A diferencia del error, $r^k$ es calculable. Pero la norma del residuo no siempre refleja la magnitud del error:
  $$\frac{\|e^k\|}{\|x^*\|} \le \kappa(A) \frac{\|r^k\|}{\|b\|} \quad$$

- Si $\kappa(A) \gg 1$, un residuo pequeño $\|r^k\| \approx 0$ no garantiza que el error $\|e^k\|$ sea pequeño.

---

# Espacios de Krylov

¿Dónde buscamos la corrección para $x^0$ si sólo podemos multiplicar la matriz $A$ por vectores?

- Partimos del único vector con información del error: el residuo inicial $r^0 = b - A x^0$.
- Aplicando el operador $A$ de forma recurrente, extraemos las direcciones principales de variación:
  $$\{r^0, A r^0, A^2 r^0, \dots, A^{k-1} r^0\} \quad$$

- **Definición (Subespacio de Krylov $\mathcal{K}_k(A, r^0)$):**
  $$\mathcal{K}_k(A, r^0) = \text{span}\{r^0, A r^0, A^2 r^0, \dots, A^{k-1} r^0\} \subset \mathbb{R}^n \quad$$

---

# Cómo Resolveríamos el Error?
- **Propuesta de Búsqueda:** Buscamos la nueva aproximación en el espacio afín:
  $$x^k \in x^0 + \mathcal{K}_k(A, r^0) \implies x^k = x^0 + p_{k-1}(A) r^0 \quad$$
  donde $p_{k-1}$ es un polinomio de grado a lo sumo $k-1$.

Al restringir la solución al subespacio $\mathcal{K}_k(A, r^0)$, los algoritmos seleccionan el "mejor" $x^k$ imponiendo condiciones de optimización realizables:

---

# Dos Métodos Insignia

1. **Método de Gradiente Conjugado (CG) [para $A$ SDP]:**
   Impone la **condición de ortogonalidad de Galerkin**: $r^k \perp \mathcal{K}_k(A, r^0)$.
   *Esto equivale geométricamente a minimizar el error inaccesible en la norma-$A$:*
   $$\min_{x^k \in x^0 + \mathcal{K}_k} \|x^* - x^k\|_A \quad$$

2. **Método GMRES [para $A$ general]:**
   Minimiza la norma Euclídea del residuo computable sobre el subespacio:
   $$\min_{x^k \in x^0 + \mathcal{K}_k} \|b - A x^k\|_2 \quad$$

---

# Método de Gradiente Conjugado (CG)

Para resolver $Ax = b$ con $A \in \mathbb{R}^{n \times n}$ **Simétrica Definida Positiva (SDP)**, construiremos la sucesión $\{x^k\}$ en un subespacio de Krylov en expansión:

- Buscamos una base $\{p^1, \dots, p^k\}$ tal que $\text{span}(p^1, \dots, p^k) = \mathcal{K}_k(A, b)$

- Si conocemos la base y los coeficientes escalares $\mu_k$, la solución se escribe:
  $$x^* = \sum_{k=1}^n \mu_k p^k \quad \implies \quad x^k = \sum_{l=1}^k \mu_l p^l$$

- Esto permite una **regla de actualización aditiva simple**:
  $$x^{k+1} = x^k + \mu_{k+1} p^{k+1}$$

> Nuestro objetivo es determinar las **direcciones de búsqueda** $p^k$ y las **longitudes de paso** $\mu_k$ de forma eficiente.

---

# Intento 1: Base Ortogonal Estándar

¿Por qué no elegir una base ortogonal ordinaria $\{q^1, \dots, q^n\}$?

- Tomemos $p^k = q^k$ y agrupemos $P = [p^1, \dots, p^n] \in \mathbb{R}^{n \times n}$ con $P^T P = I$.
- Escribiendo $x^* = P \mu$, con $\mu = [\mu_1, \dots, \mu_n]^T$:
  $$P^T x^* = P^T P \mu = I \mu = \mu \quad \implies \quad \mu_k = (p^k)^T x^*$$
  
  $$\mu_k = (p^k)^T x^* \quad \text{¡requiere conocer } x^* \text{ de antemano!}$$

- Llegamos a la misma paradoja: para calcular los coeficientes necesitaríamos la propia incógnita que deseamos hallar.
- La ortogonalidad usual no es suficiente. Requerimos una base diferente y más astuta.

---

# Intento 2: Una Nueva Condición de Optimalidad

En lugar de proyectar $x^*$, utilicemos la relación del sistema que **sí conocemos**: $Ax^* = b$.

- Multipliquemos por la izquierda por la matriz $P^T$: $P^T A x^* = P^T b$

- Como $b$ es un dato del problema, $P^T b$ es calculable.
- Insertando la descomposición $x^* = P \mu$ en esta ecuación:
  $$P^T A (P \mu) = P^T b \quad \implies \quad (P^T A P) \mu = P^T b$$

- Eliminamos $x^*$ de la ecuación! Resolvemos este sistema lineal para encontrar $\mu$.

---

# $A$-Ortogonalidad (Conjugación)

¿Cómo podemos lograr que el sistema $(P^T A P) \mu = P^T b$ sea trivial de resolver?

- Elegimos la base $\{p^k\}$ de modo que la matriz proyectada sea **diagonal**:
  $$P^T A P = D = \text{diag}(d_1, \dots, d_n)$$

- Esto equivale a exigir que $(p^i)^T A p^j = 0 \quad \text{para todo } i \neq j$

- Esta propiedad se denomina **$A$-ortogonalidad** o **conjugación** respecto de $A$.
- El sistema lineal queda completamente desacoplado y cada coeficiente se calcula directamente :smile:
  $$\mu_k = \frac{(p^k)^T b}{d_k} = \frac{(p^k)^T b}{(p^k)^T A p^k}$$

---

# El $A$-Producto Interno

**Definición:** Dada $A \in \mathbb{R}^{n \times n}$ (SDP), el **$A$-producto interno** entre dos vectores $y, z \in \mathbb{R}^n$ se define como:
$$\langle y, z \rangle_A = y^T A z$$

- Es un producto interno bien definido precisamente porque $A$ es SDP:
  - **Simetría:** $\langle y, z \rangle_A = y^T A z = (y^T A z)^T = z^T A^T y = z^T A y = \langle z, y \rangle_A$.
  - **Bilinealidad:** Directa por la linealidad del producto matricial.
  - **Positividad:** $\langle y, y \rangle_A = y^T A y > 0$ para todo $y \neq 0$.

> Exigir $P^T A P = D$ significa que **los $\{p^k\}$ son ortogonales respecto a la métrica inducida por $A$**.

---

# Interpretación Geométrica (con Cholesky)
Sabemos que $A = G^T G$, luego $\langle y, z \rangle_A = y^T A z = y^T (G^T G) z = (G y)^T (G z) = \langle G y, G z \rangle_2$
- El $A$-producto interno es el **producto escalar euclídeo** de los vectores transformados por el factor de Cholesky.
- **Geometría de la transformación:**
  - $G$ actúa como un cambio de coordenadas que transforma los elipsoides de nivel $y^T A y = \text{cte}$ en esferas estándar $\|G y\|_2^2 = \text{cte}$.
  - Dos vectores son **$A$-ortogonales** si y sólo si sus imágenes por $G$ son **ortogonales euclídeas**:
    $$(p^i)^T A p^j = 0 \iff (G p^i) \perp (G p^j)$$
---

# Norma-$A$ y Garantía de Optimalidad

El $A$-producto interno define la **norma-$A$**: $\|z\|_A = \sqrt{\langle z, z \rangle_A} = \sqrt{z^T A z}$

**Teorema:** En el paso $k$, el error exacto $e^k = x^* - x^k$ es **$A$-ortogonal** a todo $\mathcal{K}_k$. Para cada $l \le k$, tenemos:
$$(p^l)^T A (x^* - x^k) = (p^l)^T b - \sum_{i=1}^k \mu_i ((p^l)^T A p^i) = (p^l)^T b - \mu_l d_l = (p^l)^T b - d_l \left(\frac{(p^l)^T b}{d_l}\right) = 0$$

Al ser el error $A$-ortogonal a $\mathcal{K}_k$, $x^k$ es la **proyección ortogonal** de $x^*$ sobre $\mathcal{K}_k$ bajo la norma-$A$:
  $$x^k = \underset{y \in \mathcal{K}_k}{\operatorname{argmin}} \|x^* - y\|_A$$

> En cada iteración, CG produce la **mejor aproximación posible** a la solución exacta dentro de $\mathcal{K}_k$ en la métrica inducida por $A$.

---

# Generación Eficiente de Direcciones

Para generar las direcciones $\{p^k\}$, un proceso tipo Gram-Schmidt requeriría guardar todos los vectores anteriores.

La clave es usar el **vector residuo**: $r^k = b - A x^k$ (con $r^0 = b$ si $x^0 = 0$)

- Recordemos que $\mathcal{K}_k = \text{span}(b, Ab, \dots, A^{k-1} b)$.
- Si $x^{k-1} \in \mathcal{K}_{k-1}$, entonces por definición de Krylov, $A x^{k-1} \in \mathcal{K}_k$.
- Como $b \in \mathcal{K}_k$ y $A x^{k-1} \in \mathcal{K}_k$, se deduce que $r^{k-1} = b - A x^{k-1} \in \mathcal{K}_k$

- Por lo tanto, todos los residuos previos pertenecen al subespacio:
  $$\text{span}(r^0, \dots, r^{k-1}) \subset \text{span}(p^1, \dots, p^k) = \mathcal{K}_k$$

---

# Ortogonalidad de los Residuos

**Teorema:** El residuo en el paso $k$, $r^k = b - A x^k$, es ortogonal a todo el subespacio $\mathcal{K}_k$.

**Demostración:** Basta verificar que $(p^l)^T r^k = 0$ para todo $1 \le l \le k$:
$$(p^l)^T r^k = (p^l)^T (b - A x^k) = (p^l)^T b - (p^l)^T A \left( \sum_{i=1}^k \mu_i p^i \right) = (p^l)^T b - \sum_{i=1}^k \mu_i ((p^l)^T A p^i)$$

Por la condición de $A$-ortogonalidad, $(p^l)^T A p^i = 0$ si $i \neq l$, y además $(p^l)^T b = \mu_l d_l$:
$$(p^l)^T r^k = (p^l)^T b - \mu_l ((p^l)^T A p^l) = d_l \mu_l - \mu_l d_l = 0$$

Como se anula para todo $l \le k$, el residuo $r^k$ es perpendicular a todo vector de $\mathcal{K}_k$. $\blacksquare$

---

# Equivalencia de Subespacios

**Teorema:** $\text{span}(r^0, \dots, r^{k-1}) = \mathcal{K}_k = \text{span}(p^1, \dots, p^k)$

**Demostración:**
- Como $\text{span}(r^0, \dots, r^{k-1}) \subset \mathcal{K}_k$, para cualquier $l < k$, tenemos $r^l \in \mathcal{K}_{l+1} \subset \mathcal{K}_k$.
- Como $r^k \perp \mathcal{K}_k$, $r^k$ es ortogonal a todo vector dentro de él, en particular a los residuos previos:
  $$(r^k)^T r^l = 0 \quad \text{para todo } l < k$$
- Si el algoritmo no convergió antes ($r^k = 0 \iff x^k = x^*$), todos los residuos son no nulos $\implies$ son linealmente independientes y su dimensión es $k$. $\blacksquare$

---

# La Recurrencia Corta de Tres Términos

Como $r^k \in \mathcal{K}_{k+1} = \text{span}(p^1, \dots, p^{k+1})$, podemos escribir $r^k = \sum_{l=1}^{k+1} u_l p^l$

Tomando producto interno-$A$ con $p^i$ para $i \le k+1$:
$$(p^i)^T A r^k = \sum_{l=1}^{k+1} u_{l, k+1} ((p^i)^T A p^l) = u_{i, k+1} d_i \quad \implies \quad u_{i, k+1} = \frac{(A p^i)^T r^k}{d_i}$$

- $p^i \in \mathcal{K}_i \implies A p^i \in \mathcal{K}_{i+1}$.
- Si $i < k$, entonces $\mathcal{K}_{i+1} \subset \mathcal{K}_k$.
- Como $r^k \perp \mathcal{K}_k$, necesariamente $(A p^i)^T r^k = 0$ para todo $i < k$.
- Por lo tanto: $u_{i, k+1} = 0$ para todo $i < k$

---

# Colapso a Dos Términos

¡Todos los coeficientes anteriores a $k$ se anulan idénticamente! La expansión colapsa a:
$$r^k = u_{k, k+1} p^k + u_{k+1, k+1} p^{k+1}$$

Despejando la nueva dirección $p^{k+1}$ y fijando la normalización estándar $u_{k+1, k+1} = 1$:
$$p^{k+1} = r^k - u_{k, k+1} p^k \quad \text{con } u_{k, k+1} = \frac{(p^k)^T A r^k}{d_k}$$

> Para construir $p^{k+1}$, sólo usamos el residuo actual $r^k$ y la dirección anterior $p^k$.
> No necesitamos almacenar ni ortogonalizar contra toda la historia previa!

Esta recurrencia corta es lo que vuelve a CG rápido y económico en memoria.

---

# Fórmulas Eficientes: El Paso $\mu_k$

Podemos simplificar el cálculo de $\mu_k = \frac{(p^k)^T b}{d_k}$ eliminando productos innecesarios:

- Como $r^{k-1} = b - A x^{k-1}$, tenemos $b = r^{k-1} + A x^{k-1}$. Sustituyendo en el numerador: $(p^k)^T b = (p^k)^T r^{k-1} + (p^k)^T A x^{k-1}$

- Pero $x^{k-1} \in \mathcal{K}_{k-1}$ y por construcción $p^k$ es $A$-ortogonal a $\mathcal{K}_{k-1}$, por lo que $(p^k)^T A x^{k-1} = 0$, de donde $(p^k)^T b = (p^k)^T r^{k-1}$

- Por la recurrencia, $p^k = r^{k-1} - u_{k-1, k} p^{k-1}$. Como $p^{k-1} \perp r^{k-1}$, $(p^k)^T r^{k-1} = (r^{k-1} - u_{k-1, k} p^{k-1})^T r^{k-1} = \|r^{k-1}\|_2^2$

- Obtenemos la fórmula computacional óptima: $\mu_k = \frac{\|r^{k-1}\|_2^2}{(p^k)^T A p^k}$

---

# Fórmulas Eficientes: El Factor de Dirección $\tau_k$

Calculemos ahora el coeficiente de actualización de dirección $u_{k, k+1} = \frac{(A p^k)^T r^k}{d_k}$:

- De la actualización del residuo: $r^k = r^{k-1} - \mu_k A p^k \implies A p^k = \frac{1}{\mu_k} (r^{k-1} - r^k)$
- Sustituyendo este valor en el producto interno: $(A p^k)^T r^k = \frac{1}{\mu_k} (r^{k-1} - r^k)^T r^k = \frac{1}{\mu_k} (\underbrace{(r^{k-1})^T r^k}_{=0} - \|r^k\|_2^2) = -\frac{\|r^k\|_2^2}{\mu_k}$

- Usando que $\mu_k d_k = \|r^{k-1}\|_2^2$: $u_{k, k+1} = \frac{-(1/\mu_k)\|r^k\|_2^2}{d_k} = -\frac{\|r^k\|_2^2}{\mu_k d_k} = -\frac{\|r^k\|_2^2}{\|r^{k-1}\|_2^2}$

- Definiendo el parámetro $\tau_k = -u_{k, k+1}$: $\tau_k = \frac{\|r^k\|_2^2}{\|r^{k-1}\|_2^2}$ y por lo tanto $p^{k+1} = r^k + \tau_k p^k$

---

# Algoritmo: *Gradiente Conjugado (CG)*

**Entradas:** $A \in \mathbb{R}^{n \times n}$ SDP, $b \in \mathbb{R}^n$, $x^0 \in \mathbb{R}^n$, $\epsilon > 0$, $m \in \mathbb{N}$.

1. **Inicialización:**
   $$r^0 = b - A x^0, \quad p^1 = r^0, \quad \rho_0 = \|r^0\|_2^2$$

2. **Para $k = 1, 2, \dots, m$:** Si $\sqrt{\rho_{k-1}} < \epsilon$, parar y retornar $x^{k-1}$.
   - $v^k = A p^k$,  $\mu_k = \frac{\rho_{k-1}}{(p^k)^T v^k}$
   - $x^k = x^{k-1} + \mu_k p^k$
   - $r^k = r^{k-1} - \mu_k v^k$
   - $\rho_k = \|r^k\|_2^2$, $\tau_k = \frac{\rho_k}{\rho_{k-1}}$
   - $p^{k+1} = r^k + \tau_k p^k$

3. **Retornar:** $x^k$.

---

# Eficiencia Computacional y Memoria

Cada iteración de CG requiere un costo mínimo y estrictamente controlado:

- **Operaciones por iteración:**
  - **1 producto matriz-vector ($A p^k$):** En matrices ralas $O(n)$ flops.
  - **2 productos escalares:** $(p^k)^T (A p^k)$ y $\rho_k = (r^k)^T r^k$ ($O(n)$ flops).
  - **3 actualizaciones de vectores tipo saxpy:** $x^k, r^k, p^{k+1}$ ($O(n)$ flops).

- **Requisitos de Almacenamiento:**
  - Sólo requiere almacenar en memoria vectores: $x, r, p$ y $v = Ap$.
  - **No almacena la base de Krylov ni matrices densas intermedias.**

> El método exige que $A$ sea **SDP**. Si no, el producto $(p^k)^T A p^k$ puede anularse o hacerse negativo, y estamos frit@s.

---

# ¿Por qué "Gradiente Conjugado"?

**1. La parte "Gradiente":** CG minimiza el error en norma-$A$:
  $$L(y) = \frac{1}{2} \|x^* - y\|_A^2 = \frac{1}{2} (x^* - y)^T A (x^* - y)$$
- Gradiente respecto de $y$: $\nabla L(y) = Ay - Ax^* = Ay - b = -r(y)$

**2. La parte "Conjugado":** Si sólo vamos por por $r^k$, haríamos zig zag.
- CG corrige el gradiente sumando $\tau_k p^k$:
  $$p^{k+1} = r^k + \tau_k p^k$$
  forzando que la nueva dirección sea **$A$-ortogonal (conjugada)** a las anteriores, garantizando no deshacer el progreso ya optimizado.

---

<!-- # Resumen de Relaciones Matriciales

Definiendo las matrices cuyas columnas agrupan los vectores generados:
- $Q = [q^1, \dots, q^n]$: Vectores ortonormales de Lanczos.
- $P = [p^1, \dots, p^n]$: Direcciones $A$-ortogonales de CG.
- $R = [r^0, \dots, r^{n-1}]$: Residuos de CG.

| Estructura | Relación | Propiedad Fundamental |
| :---: | :---: | :--- |
| **Identidad** | $Q^T Q = I$ | Lanczos ortonormales |
| **Diagonal** | $R^T R = D_R$ | Residuos mutuamente ortogonales |
| **Diagonal** | $P^T A P = D$ | Direcciones $A$-ortogonales (conjugadas) |
| **Tridiagonal Simétrica** | $Q^T A Q = T$ | Reducción tridiagonal del proceso de Lanczos |
| **Tridiagonal Simétrica** | $R^T A R = T_R$ | Los residuos forman una base tridiagonal |

> *Demostración de $R^T A R$ tridiagonal:* Como $r^j \in \mathcal{K}_{j+1}$, se tiene $A r^j \in \mathcal{K}_{j+2}$. Si $i \ge j+2$, como $r^i \perp \mathcal{K}_i$ y $\mathcal{K}_{j+2} \subset \mathcal{K}_i$, resulta $(r^i)^T A r^j = 0$. Por simetría, la banda tiene ancho 1.

--- -->

# Convergencia de Gradiente Conjugado

¿Qué tan rápido converge la aproximación hacia $x^*$?

- En aritmética exacta, como los residuos no nulos son mutuamente ortogonales en $\mathbb{R}^n$, CG encuentra solución en **a lo sumo $n$ pasos**.
- En la práctica ($n \approx 10^5 - 10^7$), correr $n$ pasos es impensable, y los errores de redondeo destruyen la ortogonalidad exacta.
- El verdadero objetivo de CG es aproximar bien en $k \ll n$ iteraciones.

- Para $A$ SDP con $\kappa(A) = \frac{\lambda_{\max}(A)}{\lambda_{\min}(A)}$, se cumple la cota clásica:
  $$\|x^* - x^k\|_A \le 2 \left( \frac{\sqrt{\kappa(A)} - 1}{\sqrt{\kappa(A)} + 1} \right)^k \|x^* - x^0\|_A$$

---

# Interpretación de la Cota de Convergencia

Analicemos el factor de reducción del error $\rho = \frac{\sqrt{\kappa(A)} - 1}{\sqrt{\kappa(A)} + 1}$:

- $\kappa(A) \approx 1$: $\sqrt{\kappa(A)} \approx 1 \implies \rho \approx 0$.
- El error decae exponencialmente y convergemos en pocas iteraciones.

- $\kappa(A) \gg 1$: $\sqrt{\kappa(A)}$ es grande $\implies \rho \approx 1 - \frac{2}{\sqrt{\kappa(A)}} \approx 1$.
- La reducción de error por iteración es muy lenta.

> A diferencia de los métodos anteriores, CG depende de $\sqrt{\kappa(A)}$. La raíz cuadrada representa una buena aceleración cuando $\kappa(A)$ es grande.

---

# Agrupamiento de Autovalores (*Clustering*)

La cota con $\kappa(A)$ es un escenario pesimista de peor caso. La tasa real depende fuertemente de la **distribución espectral** de $A$:

- **Autovalores Idénticos o Discretos:**
  - Si $A$ tiene sólo $m$ autovalores distintos, CG converge en exactamente **a lo sumo $m$ pasos**, sin importar cuán grande sea $n$.
  - Si los autovalores forman $m$ agrupamientos densos (*clusters*), CG se comporta prácticamente como si resolviera un sistema de tamaño $m$.

- **La Clave del Precondicionamiento:**
  - Modificar el sistema $Ax = b$ multiplicando por $M^{-1} \approx A^{-1}$ de modo que $M^{-1}A$ tenga autovalores concentrados alrededor de 1 y $\kappa(M^{-1}A) \approx 1$.
  - Es la herramienta fundamental que permite resolver problemas gigantescos en la práctica.

---

# El Fenómeno de Convergencia Superlineal

En la práctica la convergencia de CG se acelera a medida que itera:

- **Mecanismo Espectral:**
  - La iteración de CG captura primero los autovalores y direcciones extremas del espectro (aproximaciones de Ritz).
  - A medida que se neutralizan estas componentes, el algoritmo opera sobre un subespacio con un **número de condición menor**

- **Efecto de Bola de Nieve:**
  - Al reducirse el $\kappa$, la tasa de convergencia local mejora progresivamente en lugar de mantenerse constante.
  - Esto explica por qué el error desciende muchas veces con una curva cóncava pronunciada hacia abajo (convergencia superlineal).

---

# Resumen: Lo Esencial de Gradiente Conjugado

| Concepto | Expresión Matemática | Significado Práctico |
| :--- | :---: | :--- |
| **Subespacio** | $\mathcal{K}_k(A, r^0) = \text{span}(p^1, \dots, p^k) = \text{span}(r^0, \dots, r^{k-1})$ | Los residuos y direcciones generan el mismo Krylov |
| **$A$-Ortogonalidad** | $(p^i)^T A p^j = 0 \quad (i \neq j)$ | Direcciones conjugadas: desacoplan la optimización |
| **Ortogonalidad de Residuos** | $r^k \perp \mathcal{K}_k, \quad (r^k)^T r^j = 0 \quad (k \neq j)$ | Proyección ortogonal de Galerkin sobre Krylov |
| **Optimalidad** | $\min_{y \in \mathcal{K}_k} \|x^* - y\|_A = \|x^* - x^k\|_A$ | Minimiza la norma energética del error en cada paso |
| **Recurrencia Corta** | $p^{k+1} = r^k + \tau_k p^k, \quad \tau_k = \frac{\|r^k\|_2^2}{\|r^{k-1}\|_2^2}$ | Memoria $O(n)$, 1 SpMV por paso, sin guardar historia |

