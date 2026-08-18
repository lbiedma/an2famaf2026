---
marp: true
theme: default
paginate: true

---
# Análisis Numérico II / Álgebra Lineal Numérica
## Clase 03: Terminando Cholesky + Eliminación Gaussiana
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Algoritmo **(Descomposición de Cholesky Prod Ext)**
**Entrada:** Matriz "SDP" $A \in \mathbb{R}^{n \times n}$.
**Salida:** Matriz triangular superior $G \in \mathbb{R}^{n \times n}$ tal que $A = G^T G$.

Para $i=1,\dots,n$ definir:

1. $g_{ii} = \sqrt{a_{ii}}$
2. Si $i < n$ entonces
    - $\mathcal{J} = \{ i+1, \dots, n \}$
    - $g_{i\mathcal{J}} = A_{i\mathcal{J}} / g_{ii}$
    - $A_{\mathcal{J}\mathcal{J}} \leftarrow A_{\mathcal{J}\mathcal{J}} - G_{i\mathcal{J}}^T G_{i\mathcal{J}}$
3. Retornar $G$.

*¿Este algoritmo se puede romper? ¿Cómo?*

---

# Algoritmo **(Descomposición de Cholesky)**
## Conteo Operacional

Siguiendo la lógica de la implementación por filas y columnas:

- **Actualización de la diagonal ($G_{ii}$):** Requiere un producto interno de vectores de longitud $i-1$, una resta y una raíz cuadrada. El costo acumulado es de aproximadamente **$n^2$ flops**
- **Actualización fuera de la diagonal ($G_{iJ}$):** Es la parte más costosa debido a un bucle triplemente anidado que realiza productos y sumas para cada elemento. Este bloque suma aproximadamente **$n^3/3$ flops**

---

# Conteo Total y Complejidad

El número exacto de operaciones para el algoritmo de producto interior es:
$$Costo = \frac{n^3}{3} + \frac{n^2}{2} + \frac{7n}{6}$$

**Resultados Clave:**
- La complejidad computacional dominante es **$O(n^3/3)$**.
- Las divisiones ($n^2/2$) y las raíces cuadradas ($n$) tienen un impacto insignificante en matrices de gran porte.

---

# Cómo usamos todo lo aprendido para resolver un sistema lineal Ax = b?

1. El procedimiento requiere sustituir $A$ por nuestra descomposición $G^T G$

$$Ax = b \iff G^T G x = b$$

2. Luego agrupamos los factores

$$G^T (G x) = b$$

3. Sea
$$y = Gx$$

4. Resolvemos $G^T y = b$

5. Resolvemos $Gx = y$

---

# Algoritmo **(Resolución de Sistema Lineal SDP)**
**Entrada:** Sistema Lineal SDP $A \in \mathbb{R}^{n \times n}$ y vector $b \in \mathbb{R}^n$.
**Salida:** Vector solución $x \in \mathbb{R}^n$.

1. Calcular la descomposición Cholesky de $A$: $A = G^T G$.
2. Resolver el sistema triangular inferior $G^T y = b$ para $y$ (sustitución hacia adelante).
3. Resolver el sistema triangular superior $Gx = y$ para $x$ (sustitución hacia atrás).
4. Retornar $x$.

_Cuántas operaciones estamos haciendo?_

---

# Un poco de Historia...

- Cholesky (1875–1918) era oficial de artillería e ingeniero geodesta del Service Géodésique de l'Armée Français.
- Propuesto en 1910 para resolver sistemas lineales provenientes de métodos de mínimos cuadrados en topografía.
- Cholesky no alcanzó a publicar su método, murió en la Primera Guerra Mundial :'((
- Ernest Benoit, compañero de Cholesky, lo publicó en 1924.
![bg right:20% height:40%](cholesky.webp)


---

# Aplicación y Costo Computacional

- Resolvemos sistemas lineales $Ax = b$ descomponiendo el problema en dos sistemas triangulares: $G^T y = b$ y $Gx = y$.
- Este método es fundamental en ingeniería y física, por ejemplo, para modelar la **distribución de temperatura** en una placa de acero.
- El costo operacional de la descomposición de Cholesky es de aproximadamente **$O(n^3/3)$ flops**.
- Spoiler: este algoritmo requiere aproximadamente la **mitad de operaciones** que una eliminación gaussiana.

![bg right:30% height:80%](ec_calor.png)

---

# Antes de Pasar a Una Nueva Descomposición

Además de ver un producto matricial por bloques, es útil verlo como "producto exterior" (outer product). 

Si tengo dos matrices $B$ y $C$, $A = BC$ puede verse como:

- $a_{ij} = \sum_{k=1}^n b_{ik} c_{kj}$, producto interno entre la fila i de $B$ y la columna j de $C$

Pero también lo podemos ver como:

- $A = \sum_{k=1}^n B_{:,k} C_{k,:}$, donde $B_{:,k}$ es la columna k de $B$ y $C_{k,:}$ es la fila k de $C$.

En vez de verla elemento por elemento, estamos viendo a $A$ como una suma de matrices. _Qué rango tienen?_

---

# Un Ejemplo Concreto

$$A = \underbrace{\begin{pmatrix} b_{11} \\ b_{21} \end{pmatrix}}_{B_{:,1}} \underbrace{\begin{pmatrix} c_{11} & c_{12} \end{pmatrix}}_{C_{1,:}} + \underbrace{\begin{pmatrix} b_{12} \\ b_{22} \end{pmatrix}}_{B_{:,2}} \underbrace{\begin{pmatrix} c_{21} & c_{22} \end{pmatrix}}_{C_{2,:}}$$

Primero, calculamos las dos matrices de rango uno:

$$\begin{pmatrix} b_{11}c_{11} & b_{11}c_{12} \\ b_{21}c_{11} & b_{21}c_{12} \end{pmatrix} + \begin{pmatrix} b_{12}c_{21} & b_{12}c_{22} \\ b_{22}c_{21} & b_{22}c_{22} \end{pmatrix}$$

Luego, las sumamos para obtener el resultado final:

$$A = \begin{pmatrix} b_{11}c_{11} + b_{12}c_{21} & b_{11}c_{12} + b_{12}c_{22} \\ b_{21}c_{11} + b_{22}c_{21} & b_{21}c_{12} + b_{22}c_{22} \end{pmatrix}$$

---

# Por qué es importante esta perspectiva? 🤔

Aunque parezca más compleja, la perspectiva del producto exterior es crucial para el diseño de algoritmos.

- Muestra cómo se puede construir una matriz de forma **iterativa**.
- Muchos algoritmos de factorización (como vimos con Cholesky) se basan en la idea de "despegar" o restar estas componentes de rango uno de la matriz original, una a la vez, para revelar su estructura subyacente.
- Usaremos exactamente esta idea para deducir el próximo algoritmo.

---
# Se acuerdan de Eliminación Gaussiana?

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
<div>

Sea $A = \begin{bmatrix} 1 & 4 & 7 \\ 2 & 5 & 8 \\ 3 & 6 & 10 \end{bmatrix}$.

</div>
<div>

Multiplicamos f1 por -2 y se la restamos a f2, multiplicamos f1 por -3 y se la restamos a f3. Luego, multiplicamos f2 por -2 y se la restamos a f3:

$$ \begin{bmatrix} 1 & 4 & 7 \\ 2 & 5 & 8 \\ 3 & 6 & 10 \end{bmatrix} \quad \longrightarrow \quad \begin{bmatrix} 1 & 4 & 7 \\ 0 & -3 & -6 \\ 0 & -6 & -11 \end{bmatrix} \quad \longrightarrow \quad \begin{bmatrix} 1 & 4 & 7 \\ 0 & -3 & -6 \\ 0 & 0 & 1 \end{bmatrix}.$$

</div>
</div>

---

# Transformaciones de Gauss

Si deseo transformar la columna $k$ de $A$, en un vector con $x_i = 0$ para $i = k+1, \dots, n$ sin alterar los elementos anteriores, defino

$$ M_k = I - v^k (e^k)^T $$

donde $v^k = \begin{bmatrix} 0 & \dots & 0 & a_{k+1,k}/a_{kk} & \dots & a_{n,k}/a_{kk} \end{bmatrix}^T$ y $e^k$ es el k-ésimo vector canónico.
