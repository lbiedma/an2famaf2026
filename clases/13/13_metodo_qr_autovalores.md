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
## Clase 13: Iteración QR para Autovalores
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Motivación: De las potencias a la versión matricial

El **método de las potencias** halla autovalores y autovectores de a uno en uno, pero requiere:
- Iniciar con un $q^0$ con coordenada no nula en la dirección dominante (difícil de verificar en la práctica).

**Idea clave:**
- Si $Q \in \mathbb{R}^{n \times n}$ es ortogonal, sus columnas generan $\mathbb{R}^n$.
- Por lo tanto, alguna columna de $Q$ tiene coordenada no nula en la dirección dominante.
- En vez de correr potencias columna por columna, consideramos una **versión matricial**:

$$
\begin{aligned}
\text{Potencia:}& \quad z^k = A q^{k-1} \quad\longrightarrow\quad Z_k = A Q_{k-1} \quad (Q_0 \text{ ortogonal}) \\
\text{Escalado:}& \quad q^k = z^k / \sigma_k \quad\longrightarrow\quad \text{Preservar } \operatorname{Im}(Z_k) \text{ con } Q_k \text{ ortogonal}
\end{aligned}
$$

El escalado matricial se obtiene con la descomposición QR: $Z_k = Q_k R_k$.

---

# Método de iteraciones ortogonales

**Esquema iterativo:**
0. Dar $Q_0 \in \mathbb{R}^{n \times n}$ ortogonal y $k = 1$.
1. Definir $Z_k = A Q_{k-1}$.
2. Obtener $Q_k, R_k$ tal que $Q_k R_k = Z_k$ con la descomposición QR de $Z_k$.
3. Hacer $k \leftarrow k + 1$ y regresar al paso 1.

**Propiedades:**
- Genera sucesiones $\{Q_k\}$ ortogonales y $\{R_k\}$ triangulares superiores:
  $$
  R_k = Q_k^T Z_k = Q_k^T A Q_{k-1}
  $$
- Como $\|Q_k\|_2 = 1$, tomando subsucesiones se obtiene que $R_k$ converge a $Q^T A \hat{Q}$ triangular superior, donde $Q$ y $\hat{Q}$ son puntos límite de $Q_k$ y $Q_{k-1}$.

---

# La sucesión $T_k$ y el obstáculo del espectro real

Si en el método de iteraciones ortogonales definimos:
$$
T_k = Q_k^T A Q_k
$$
Tomando límite se obtendría $T = Q^T A Q$ con $Q$ ortogonal. Si $T$ fuera triangular superior, **sus autovalores estarían en la diagonal**.

> **Obstáculo fundamental:**
> Todas las matrices anteriores son reales, pero una matriz $A \in \mathbb{R}^{n \times n}$ **no necesariamente tiene todos sus autovalores reales**.
> En $\mathbb{R}$, no siempre existe una matriz semejante que sea triangular superior pura.

**Estrategia:**
1. Demostrar la existencia de la descomposición triangular en $\mathbb{C}$ (**Teorema de Schur**).
2. Deducir la **iteración QR** a partir de las iteraciones ortogonales.
3. Adaptar las ideas para matrices con coeficientes reales (**Schur Real**).

---

# Teorema de Schur (en $\mathbb{C}$)

**Teorema 6.9 (Descomposición de Schur):**
Si $A \in \mathbb{C}^{n \times n}$, existe $Q \in \mathbb{C}^{n \times n}$ unitaria tal que:
$$
T = Q^* A Q \quad \text{es triangular superior.}
$$

**Demostración (Inducción en $n$):**
- **Base ($n=1$):** Inmediato ($A = a \in \mathbb{C}$, tomando $Q = 1 \implies T = a$).
- **Paso inductivo:** Sea $(\lambda, v)$ con $A v = \lambda v$, $\|v\|_2 = 1$.
  Por Gram–Schmidt completamos $v$ a una base ortonormal $U = [v \quad V] \in \mathbb{C}^{n \times n}$ unitaria:
  $$
  U^* A U = \begin{bmatrix} v^* \\ V^* \end{bmatrix} [A v \quad A V] = \begin{bmatrix} \lambda & w^* \\ 0 & B \end{bmatrix}
  $$
  donde $w^* = v^* A V \in \mathbb{C}^{1 \times (n-1)}$ y $B = V^* A V \in \mathbb{C}^{(n-1) \times (n-1)}$.

---

# Demostración del Teorema de Schur (cont.)

- Por hipótesis inductiva sobre $B$, existe $\tilde{U} \in \mathbb{C}^{(n-1) \times (n-1)}$ unitaria tal que $\tilde{U}^* B \tilde{U} = \tilde{T}$ es triangular superior.
- Definimos la matriz unitaria:
  $$
  Q = U \begin{bmatrix} 1 & 0 \\ 0 & \tilde{U} \end{bmatrix} \in \mathbb{C}^{n \times n}
  $$
- Efectuando el producto por bloques:
  $$
  Q^* A Q = \begin{bmatrix} 1 & 0 \\ 0 & \tilde{U}^* \end{bmatrix} \begin{bmatrix} \lambda & w^* \\ 0 & B \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & \tilde{U} \end{bmatrix} = \begin{bmatrix} \lambda & w^* \tilde{U} \\ 0 & \tilde{T} \end{bmatrix} = T
  $$
  que es triangular superior. $\blacksquare$

*Estructura:* $T = D + N$, donde $D$ contiene los autovalores y $N$ es estrictamente triangular superior (nilpotente).

---

# De iteraciones ortogonales a iteraciones QR

Queremos generar $T_k = Q_k^* A Q_k$ sin arrastrar las matrices de la iteración ortogonal:

1. **Por un lado:**
   $$
   T_{k-1} = Q_{k-1}^* A Q_{k-1} = Q_{k-1}^* Z_k = Q_{k-1}^* (Q_k R_k) = (Q_{k-1}^* Q_k) R_k
   $$
   Como $U_k = Q_{k-1}^* Q_k$ es unitaria y $R_k$ es triangular superior:
   $$
   \boxed{T_{k-1} = U_k R_k \quad \text{es la descomposición QR de } T_{k-1}}
   $$

2. **Por otro lado:**
   $$
   T_k = Q_k^* A Q_k = Q_k^* A Q_{k-1} (Q_{k-1}^* Q_k) = Q_k^* Z_k U_k = (Q_k^* Q_k R_k) U_k = \boxed{R_k U_k}
   $$

> **¡Regla del producto inverso!**
> Para pasar de $T_{k-1}$ a $T_k$: calculamos la QR de $T_{k-1}$ y multiplicamos los factores al revés.

---

# Método de iteraciones QR

**Esquema iterativo:**
0. Dar $U_0$ unitaria, definir $T_0 = U_0^* A U_0$ (típicamente $U_0 = I \implies T_0 = A$) y $k = 1$.
1. Obtener $U_k, R_k$ tal que $U_k R_k = T_{k-1}$ con la descomposición QR de $T_{k-1}$.
2. Definir $T_k = R_k U_k$.
3. Hacer $k \leftarrow k + 1$ y regresar al paso 1.

**Propiedades:**
- **Semejanza unitaria:** $T_k = R_k U_k = U_k^* T_{k-1} U_k = \dots = Q_k^* A Q_k$, donde $Q_k = U_0 U_1 \cdots U_k$.
- Si $|\lambda_1| > |\lambda_2| > \dots > |\lambda_n|$, $\{T_k\}$ converge a una matriz $T$ **triangular superior** con los autovalores en la diagonal.
- No requiere almacenar $\{Q_k\}$ ni calcular potencias explícitas.

---

# Algoritmo QR en código y relación con $A^k$

```python
T = A.copy()
for k in range(num_iter):
    U, R = np.linalg.qr(T)
    T = R @ U
```

**Relación con potencias $A^k$:**
Definiendo $\tilde{Q}_k = U_1 U_2 \cdots U_k$ y $\tilde{R}_k = R_k R_{k-1} \cdots R_1$:
$$
A^k = \tilde{Q}_k \tilde{R}_k
$$
- La iteración QR produce la misma sucesión de factores $R$ que la iteración ortogonal iniciada con $Q_0 = I$.
- El algoritmo genera implícitamente la descomposición QR de la potencia $A^k$.

---

# Descomposición de Schur en $\mathbb{R}$

¿Qué ocurre si trabajamos exclusivamente con matrices y aritmética en $\mathbb{R}$?

**Teorema 6.10 (Descomposición de Schur en $\mathbb{R}$):**
Si $A \in \mathbb{R}^{n \times n}$, existe $Q \in \mathbb{R}^{n \times n}$ ortogonal tal que:
$$
Q^T A Q = \begin{bmatrix}
R_{11} & R_{12} & \cdots & R_{1s} \\
0 & R_{22} & \cdots & R_{2s} \\
\vdots & \ddots & \ddots & \vdots \\
0 & \cdots & 0 & R_{ss}
\end{bmatrix}
$$
donde cada bloque diagonal $R_{ll}$ es:
- $R_{ll} \in \mathbb{R}^{1 \times 1}$: autovalor real de $A$.
- $R_{ll} \in \mathbb{R}^{2 \times 2}$: con autovalores complejos conjugados $(\lambda, \bar{\lambda})$.

La matriz $Q^T A Q$ es **cuasi-triangular superior** (o forma de Schur real).

---

# Demostración de Schur Real (Idea)

Inducción en el número $k$ de pares de autovalores complejos conjugados:
- Si $\lambda = \gamma + i\mu \in \mathbb{C}$ ($\mu \neq 0$) tiene autovector $y + i z \neq 0$ con $y, z \in \mathbb{R}^n$:
  $$
  A(y + i z) = (\gamma + i\mu)(y + i z) = \gamma y - \mu z + i(\mu y + \gamma z)
  $$
- Agrupando parte real e imaginaria:
  $$
  A [y \quad z] = [y \quad z] \begin{bmatrix} \gamma & \mu \\ -\mu & \gamma \end{bmatrix} = [y \quad z] S
  $$
- Los vectores $y, z$ son **linealmente independientes** en $\mathbb{R}^n$.
- Factorizando $[y \quad z] = \hat{Q} \begin{bmatrix} \hat{R} \\ 0 \end{bmatrix}$ (QR con $\hat{R} \in \mathbb{R}^{2 \times 2}$ no singular):
  $$
  \hat{Q}^T A \hat{Q} = \begin{bmatrix} \hat{R}_{11} & \hat{R}_{12} \\ 0 & \hat{R}_{22} \end{bmatrix} \quad \text{con } \hat{R}_{11} = \hat{R} S \hat{R}^{-1}
  $$
- Los autovalores de $\hat{R}_{11}$ son $\gamma \pm i\mu$. Se aplica hipótesis inductiva sobre $\hat{R}_{22}$.

---

# Aceleración con shifts

Sin shift, el bloque subdiagonal inferior $T_{k,21}$ decae con razón $\approx |\lambda_n| / |\lambda_{n-1}|$.

Con shift $\mu$, iteramos sobre $A - \mu I$; la tasa para el último autovalor pasa a ser

$$
\frac{|\lambda_n - \mu|}{|\lambda_{n-1} - \mu|}.
$$

**Shift de Rayleigh:** $\mu_k = (T_k)_{nn}$. Si $\mu_k \approx \lambda_n$, el numerador es pequeño $\Rightarrow$ convergencia **rápida** (cuadrática en la práctica) del elemento $T_k[n,n-1]$ hacia cero.

---

# Autovectores desde Schur

Si $A = Q T Q^H$ y $T \boldsymbol v = \lambda \boldsymbol v$, entonces $\boldsymbol x = Q \boldsymbol v$ satisface $A \boldsymbol x = \lambda \boldsymbol x$.

Para $T$ triangular superior, $(T - \lambda I)\boldsymbol v = 0$ se resuelve por **sustitución hacia atrás** en bloques: $\lambda$ distinta de autovalores de bloques diagonales inferiores $\Rightarrow$ componentes libres acotadas; fijar $v_i = 1$ en la fila singular y resolver el bloque superior.

Costo dominante tras tener $T$: $O(n^2)$ por autovector (sistemas triangulares) más $O(n^2)$ para $\boldsymbol x = Q \boldsymbol v$.

---

# Costo del QR ingenuo

- QR denso de $n \times n$: $O(n^3)$ por paso.
- $k$ pasos: $O(k n^3)$ — **impracticable** para $n$ grande.

**Enfoque estándar en dos fases:**

1. **Reducción** (una vez): similaridad unitaria $A \to H$ (Hessenberg) o $A \to T$ (tridiagonal, si $A$ es simétrica). Costo $O(n^3)$.
2. **Iteración QR con shifts** sobre la forma reducida: $O(n^2)$ o $O(n)$ por paso.

Total típico: $O(n^3)$ frente a $O(n^4)$ del QR denso iterado.

---

# Forma de Hessenberg superior

$H \in \mathbb{R}^{n \times n}$ es **Hessenberg superior** si $h_{ij} = 0$ para $i > j + 1$:

$$
H = \begin{pmatrix}
\times & \times & \cdots & \times \\
\times & \times & \cdots & \times \\
0 & \times & \ddots & \vdots \\
\vdots & \ddots & \ddots & \times
\end{pmatrix}
$$

- Máximo de ceros alcanzable en **finitos** pasos de similaridad ortogonal.
- **Invariante** bajo un paso QR: si $H_k = Q R$, entonces $H_{k+1} = R Q$ sigue siendo Hessenberg.

---

# Reducción a Hessenberg

Objetivo: $H = Q^T A Q$ con $Q$ ortogonal.

- $n-2$ reflectores de **Householder** $Q_1, \ldots, Q_{n-2}$: en la columna $k$, ceros en filas $k+2, \ldots, n$.
- Patrón: $Q_k A Q_k^T$ (izquierda y derecha) preserva ceros ya introducidos en columnas anteriores.

Costo: $\approx \frac{10}{3} n^3$ flops si se forma $Q$ explícitamente; $\approx \frac{4}{3} n^3$ si solo se necesita $H$.

La similaridad **no cambia autovalores**.

---

# QR en matrices Hessenberg

**Paso 1:** $H = Q R$ con $n-1$ **rotaciones de Givens** que anulan $H_{k+1,k}$ — costo $O(n^2)$.

**Paso 2:** $H_{\text{nuevo}} = R Q$ aplicando $G_k^T$ por la derecha sin formar $Q$ explícitamente — $O(n^2)$.

Un paso completo: $O(n^2)$. Encontrar todos los autovalores suele requerir $O(n)$ pasos (con deflación) $\Rightarrow$ fase iterativa $O(n^3)$.

---

# Iteración QR con shift

Sobre $T_k$ en forma Hessenberg (inicialmente $T_0 = H$):

1. Elegir $\mu$ (p. ej. $\mu = T_k[n,n]$).
2. Factorizar $T_k - \mu I = U_k R_k$.
3. Actualizar $T_{k+1} = R_k U_k + \mu I$.

Equivalencia: $T_{k+1} = U_k^H T_k U_k$ (similaridad unitaria).

En código: `Qk, Rk = qr(Tk - mu*I); Tk = Rk @ Qk + mu*I`.

---

# Deflación

Cuando $|T_k[n, n-1]|$ es despreciable:

$$
T_k \approx \begin{pmatrix} A_{11} & A_{12} \\ 0 & \lambda_n \end{pmatrix}
$$

- Registrar $\lambda_n \approx T_k[n,n]$.
- Repetir el algoritmo sobre el bloque $(n-1) \times (n-1)$ superior izquierdo.

El shift acelera la convergencia de la fila inferior; la deflación **reduce el tamaño** del problema en cada autovalor encontrado.

---

# Simétricas vs. no simétricas reales

| | **Simétrica real** | **No simétrica real** |
| --- | --- | --- |
| Autovalores | Reales | Reales o pares complejos conjugados |
| Fase 1 | Tridiagonal ($\approx \frac{4}{3}n^3$) | Hessenberg ($\approx \frac{10}{3}n^3$) |
| Shift | Uno real (Wilkinson) | Doble (Francis, implícito) |
| Costo / paso | $O(n)$ | $O(n^2)$ |
| Convergencia | Cúbica (Wilkinson) | Cuadrática |
| Forma límite | Diagonal | Schur triangular (bloques $2\times2$ si hay complejos) |

---

# Wilkinson y Francis (idea)

**Simétrica:** shift de **Wilkinson** = autovalor del bloque $2 \times 2$ inferior más cercano a $T_{nn}$; evita fallos del shift $T_{nn}$ en casos patológicos.

**No simétrica:** shift simple real puede **oscilar** si el autovalor “inferior” es complejo. **Paso doble de Francis:** shifts $\mu_1, \mu_2$ = autovalores del bloque $2 \times 2$ inferior; “bulge chasing” con aritmética real only.

En la práctica: `numpy.linalg.eigh` (simétricas) vs. `numpy.linalg.eig` (generales).

---

# Resumen

1. **Iteración ortogonal:** $A Q_k = Q_{k+1} R_{k+1}$; subespacios = potencias; $T_k = Q_k^H A Q_k$ tiende a Schur.
2. **Iteración QR:** QR($T_k$) y $T_{k+1} = R U$; equivalente a ortogonalizar $A^k$ sin calcular $A^k$.
3. **Hessenberg + shifts + deflación:** algoritmo estándar $O(n^3)$ para todos los autovalores.
4. **Simétricas:** tridiagonal + shift de Wilkinson, mucho más barato por iteración.

**Lectura:** [Eric Darve, NLA — QR iteration](https://ericdarve.github.io/NLA/content/qr_iteration.html) y secciones enlazadas.
