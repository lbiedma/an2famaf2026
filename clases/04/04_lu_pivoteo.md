---
marp: true
theme: default
paginate: true

---

# Análisis Numérico II / Álgebra Lineal Numérica
## Clase 04: Descomposición LU Tradicional y con Pivoteo
![height:50%](https://www.famaf.unc.edu.ar/documents/3264/Logo_FAMAF_UNC_color.png)

---

# Descomposición LU

Tenemos un conjunto de Transformaciones de Gauss que aplicamos a izquierda para obtener una matriz triangular superior $U$.

$$ U = M_{n-1} \dots M_1 A $$

Entonces, si $M_k = I - v_k e_k^T$ con $v_k$ vector de multiplicadores:

$$ A = (M_{n-1} \dots M_1)^{-1} U = M_1^{-1} \dots M_{n-1}^{-1} U $$

Definimos $L = M_1^{-1} \dots M_{n-1}^{-1}$ y cada $M_k^{-1}$ es de la forma $I + v_k e_k^T$

---

# Teorema **(Existencia y Unicidad de la Descomposición LU)**

Sea $A \in \mathbb{R}^{n \times n}$. Si $det(A_k) \neq 0$ para toda submatriz principal de tamaño $k \in \{1, \dots, n\}$, entonces existe una factorización única de $A$ de la forma

$$ A = L U $$

donde $L \in \mathbb{R}^{n \times n}$ es una matriz triangular inferior con $L_{ii} = 1$ para todo $i \in \{1, \dots, n\}$, y $U \in \mathbb{R}^{n \times n}$ es una matriz triangular superior.

---

# Demostración de Existencia: Estrategia

Procedemos por **inducción** sobre el paso $k$ de la Eliminación Gaussiana. Queremos demostrar que los pivotes $a_{kk}^{(k-1)}$ nunca se anulan.

- **Caso Base ($k=1$):**
  La submatriz principal de orden 1 es $A_1 = [a_{11}]$. Como $\det(A_1) \neq 0$, se deduce que el primer pivote **$a_{11} \neq 0$**. Esto garantiza que la primera transformación de Gauss $M_1$ está bien definida.

- **Hipótesis Inductiva:**
  Suponemos que ha sido posible realizar con éxito los primeros $k-1$ pasos de la eliminación, transformando la matriz original en:
  $$A^{(k-1)} = M_{k-1} \dots M_1 A$$

---

# Paso Inductivo: Estructuración por Bloques

Debemos garantizar que el pivote de la etapa actual, $a_{kk}^{(k-1)}$, sea distinto de cero. 

Definamos la matriz acumulada de transformaciones de Gauss como:
$$\Gamma = M_{k-1} \dots M_1$$

Como cada $M_i$ es **triangular inferior unitaria**, el producto $\Gamma$ también posee esta estructura. Si particionamos la ecuación $A^{(k-1)} = \Gamma A$ analizando el bloque superior izquierdo de tamaño $k \times k$, obtenemos:

$$A^{(k-1)}_{1:k, 1:k} = \Gamma_{1:k, 1:k} A_k$$

---

# Paso Inductivo: El Rol de los Determinantes

Aplicando la propiedad del determinante al producto de bloques de tamaño $k \times k$:

$$\det(A^{(k-1)}_{1:k, 1:k}) = \det(\Gamma_{1:k, 1:k}) \cdot \det(A_k)$$

Dado que $\Gamma_{1:k, 1:k}$ es una matriz triangular inferior unitaria, su determinante es idénticamente **$1$**. Por lo tanto:

$$\det(A^{(k-1)}_{1:k, 1:k}) = \det(A_k)$$

Por hipótesis del teorema, sabemos que $\det(A_k) \neq 0$, lo que implica que el bloque $A^{(k-1)}_{1:k, 1:k}$ es **no singular**.

---

# Paso Inductivo: Conclusión de la Existencia

Como la submatriz $A^{(k-1)}_{1:k, 1:k}$ es triangular superior (debido a los $k-1$ pasos de eliminación ya completados), su determinante se calcula simplemente como el producto de sus elementos diagonales:

$$\det(A^{(k-1)}_{1:k, 1:k}) = a_{11}^{(0)} \cdot a_{22}^{(1)} \dots a_{kk}^{(k-1)}$$

Dado que este producto es distinto de cero ($\det(A_k) \neq 0$), **ninguno de sus factores puede ser nulo**.

Por lo tanto, **$a_{kk}^{(k-1)} \neq 0$**, el pivote está bien definido y el proceso de inducción queda completo. Al final, se obtiene $A = LU$.

---

# Demostración de Unicidad

Supongamos que existen dos factorizaciones distintas para la matriz $A$:
$$A = L_1 U_1 \quad \text{y} \quad A = L_2 U_2$$

Como $A$ es no singular, tanto $L_i$ como $U_i$ son invertibles. Igualando ambas expresiones:
$$L_1 U_1 = L_2 U_2 \implies L_2^{-1} L_1 = U_2 U_1^{-1}$$

- El lado izquierdo ($L_2^{-1} L_1$) es el producto de matrices triangulares inferiores unitarias, por lo que es **triangular inferior unitaria**.
- El lado derecho ($U_2 U_1^{-1}$) es el producto de matrices triangulares superiores, por lo que es **triangular superior**.

La única matriz que es simultáneamente triangular superior y triangular inferior unitaria es la **matriz identidad $I$**.

---

# Conclusión de la Unicidad

Por lo tanto, se debe cumplir la igualdad:

$$L_2^{-1} L_1 = I \implies L_1 = L_2$$

Y de igual manera:

$$U_2 U_1^{-1} = I \implies U_1 = U_2$$

Lo que demuestra que **la descomposición LU (cuando existe) es única**.

---

# Algoritmo **(Factorización LU)**
**Entrada:** Matriz $A \in \mathbb{R}^{n \times n}$ con $det(A_k) \neq 0$ para toda submatriz principal de tamaño $k \in \{1, \dots, n\}$.
**Salida:** Matrices $L \in \mathbb{R}^{n \times n}$ y $U \in \mathbb{R}^{n \times n}$ tales que $A = L U$.

1. Inicializar $L = I$ y $U = A$.
2. Para $k = 1 \dots n-1$, definir
    - $\mathcal{I} = \{ k+1, \dots, n \}$
    - $\mathcal{J} = \{ k, \dots, n \}$
    - $v_{\mathcal{I}} = U_{\mathcal{I},k} / u_{k,k}$
    - $L_{\mathcal{I},k} = v_{\mathcal{I}}$
    - $U_{\mathcal{I},\mathcal{J}} \leftarrow U_{\mathcal{I},\mathcal{J}} - v_{\mathcal{I}} U_{k,\mathcal{J}}$
3. Retornar $L$, $U$.

---

![](esquema_lu_inplace.png)
