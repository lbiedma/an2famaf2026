# Análisis Numérico II / Álgebra Lineal Numérica
## FAMAF - Universidad Nacional de Córdoba (2026)

Este repositorio contiene el material de la materia **Análisis Numérico II / Álgebra Lineal Numérica** de la Facultad de Matemática, Astronomía, Física y Computación (FAMAF) de la Universidad Nacional de Córdoba. Aquí encontrarás las clases teóricas, las pizarras en PDF, códigos de ejemplo en Python, enunciados de los trabajos prácticos y sus respectivas resoluciones sugeridas.

---

### 👥 Equipo Docente
* **Teóricos:** Dr. Luis Biedma (lbiedma@unc.edu.ar - Of. 309)
* **Prácticos:** Lic. Claudio Armas (claudio.armas@unc.edu.ar - Of. 324)

---

## 🗺️ Mapa de Navegación del Repositorio

A continuación se presentan los accesos rápidos a todo el material disponible en el repositorio.

### 📚 Clases Teóricas y Material Asociado

Las diapositivas teóricas se encuentran escritas en formato Markdown preparadas para presentarse con [Marp](https://marp.app/) y también exportadas a formato PDF. Se incluye la pizarra digital de las explicaciones y códigos relevantes desarrollados.

| Clase | Tema Principal | Diapositivas | Documento PDF | Recursos / Códigos de Clase |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Motivación y Preliminares**<br>• Presentación de la materia e información administrativa.<br>• Repaso de Álgebra Lineal (sistemas, matrices, determinantes).<br>• Sistemas triangulares y algoritmo de sustitución. | [Slide Markdown](clases/01/01_motivacion_preliminares.md) | [Descargar PDF](clases/01/01_motivacion_preliminares.pdf) | • Código de sustitución: [sustitucion.py](clases/01/sustitucion.py)<br>• Gráfico explicativo: [sol_trinf_compare.png](clases/01/sol_trinf_compare.png) |
| **02** | **Descomposición de Cholesky**<br>• Sistemas Simétricos Definidos Positivos (SDP).<br>• Teoremas de existencia y propiedades.<br>• Algoritmo de Cholesky (producto externo). | [Slide Markdown](clases/02/02_descomposicion_cholesky.md) | [Descargar PDF](clases/02/02_descomposicion_cholesky.pdf) | • Pizarra digital: [pizarra.pdf](clases/02/pizarra.pdf)<br>• Gráfico: [cholesky_prod_ext.png](clases/02/cholesky_prod_ext.png) |
| **03** | **Cholesky y Eliminación Gaussiana**<br>• Costo de Cholesky y aplicación práctica (Ec. del Calor 2D).<br>• Algoritmo de Eliminación Gaussiana tradicional.<br>• Operaciones elementales y matrices multiplicadoras. | [Slide Markdown](clases/03/03_cholesky_gauss.md) | [Descargar PDF](clases/03/03_cholesky_gauss.pdf) | • Pizarra digital: [pizarra.pdf](clases/03/pizarra.pdf)<br>• Código de prueba: [cholesky_circumference.py](clases/03/cholesky_circumference.py)<br>• Gráfico Ec. Calor: [ec_calor.png](clases/03/ec_calor.png)<br>• Ilustración: [cholesky.webp](clases/03/cholesky.webp) |
| **04** | **Descomposición LU Tradicional y con Pivoteo**<br>• Formulación de la descomposición LU.<br>• Algoritmo LU in-place.<br>• Inestabilidad numérica y pivoteo parcial (matriz de permutación). | [Slide Markdown](clases/04/04_lu_pivoteo.md) | [Descargar PDF](clases/04/04_lu_pivoteo.pdf) | • Pizarra digital: [pizarra.pdf](clases/04/pizarra.pdf)<br>• Test de inestabilidad: [inestabilidad_lu.py](clases/04/inestabilidad_lu.py)<br>• Esquema de almacenamiento: [esquema_lu_inplace.png](clases/04/esquema_lu_inplace.png) |
| **05** | **Sensibilidad de Sistemas Lineales**<br>• Estabilidad numérica e introducción de normas vectoriales y matriciales.<br>• Axiomas de normas y normas inducidas.<br>• Número de condición de una matriz. | [Slide Markdown](clases/05/05_sensibilidad_sistemas_lineales.md) | [Descargar PDF](clases/05/05_sensibilidad_sistemas_lineales.pdf) | • Test de mal condicionamiento: [ejemplo_mal_condicionamiento.py](clases/05/ejemplo_mal_condicionamiento.py)<br>• Gráfico de normas: [compara_normas.png](clases/05/compara_normas.png) |
| **06** | **Errores Numéricos y Residuos Mínimos**<br>• Normas matriciales y norma dual.<br>• Análisis de errores y cota del error en función de $\kappa(A)$.<br>• Introducción a residuos mínimos y matrices ortogonales. | [Slide Markdown](clases/06/06_errores_numericos_residuos_minimos.md) | [Descargar PDF](clases/06/06_errores_numericos_residuos_minimos.pdf) | • Pizarra digital QR: [pizarra_descomposicion_qr.pdf](clases/06/pizarra_descomposicion_qr.pdf) |
| **07** | **Descomposición QR**<br>• Transformaciones ortogonales en mínimos cuadrados.<br>• Rotaciones de Givens.<br>• Transformaciones y reflexiones de Householder. | [Slide Markdown](clases/07/07_descomposicion_qr.md) | [Descargar PDF](clases/07/07_descomposicion_qr.pdf) | • Pizarra digital: [pizarra.pdf](clases/07/pizarra.pdf)<br>• Gráficos: [definicion_ortogonal.png](clases/07/definicion_ortogonal.png), [rotacion.png](clases/07/rotacion.png), [solucion_cuadrados_minimos.png](clases/07/solucion_cuadrados_minimos.png) |
| **08** | **QR, Cuadrados Mínimos y Estabilidad**<br>• Algoritmo de Householder y QR completo.<br>• Resolución de sistemas sobredeterminados (Mínimos Cuadrados).<br>• Teorema de estabilidad de QR vs. Ecuaciones Normales.<br>• Comparación LU vs. QR. | [Slide Markdown](clases/08/qr_cuadrados_minimos.md) | [Descargar PDF](clases/08/qr_cuadrados_minimos.pdf) | • Script interactivo Givens: [qr_givens_interactivo.py](clases/08/qr_givens_interactivo.py)<br>• Demostración de estabilidad: [estabilidad_qr_vs_normales.py](clases/08/estabilidad_qr_vs_normales.py) |
| **09** | **Descomposición en Valores Singulares (SVD)**<br>• Los 4 subespacios fundamentales y relaciones de ortogonalidad.<br>• Existencia y formulación de la SVD ($A = U \Sigma V^T$).<br>• Relación con autovalores de $A^T A$ y $A A^T$.<br>• Normas matriciales ($\|A\|_2$, $\|A\|_F$) y valores singulares.<br>• Teorema de Eckart-Young (aproximación óptima de bajo rango).<br>• Aplicaciones: compresión de datos y PCA. | [Slide Markdown](clases/09/descomposicion_svd.md) | [Descargar PDF](clases/09/09_descomposicion_svd.pdf) | • Compresión de imágenes con SVD: [app_svd_imagen.py](clases/09/app_svd_imagen.py)<br>• Gráfico de transformación geométrica: [transformacion_svd.png](clases/09/transformacion_svd.png)<br>• Imagen de prueba: [rafa.jpg](clases/09/rafa.jpg) |
| **10** | **SVD: Aplicaciones y Cuadrados Mínimos**<br>• Cuadrados mínimos en sistemas con deficiencia de rango.<br>• Solución de norma mínima y caracterización geométrica ($x^* \perp N(A)$).<br>• Pseudoinversa de Moore-Penrose ($A^+$).<br>• Algoritmo de resolución por SVD. | [Slide Markdown](clases/10/svd_cuadrados_minimos.md) | [Descargar PDF](clases/10/svd_cuadrados_minimos.pdf) | • Pizarra digital: [pizarra.pdf](clases/10/pizarra.pdf)<br>• Comparación de métodos de CM: [compara_cuadrados_minimos.png](clases/10/compara_cuadrados_minimos.png) |
| **11** | **Autovalores y Autovectores**<br>• Definición formal de autovalores y autovectores en $\mathbb{C}^{n \times n}$.<br>• Repaso de fundamentos teóricos.<br>• Propiedades algebraicas y geométricas. | - | [Descargar PDF](clases/11/clase.pdf) | • Pizarra digital: [clase.pdf](clases/11/clase.pdf) |

---

### 📝 Prácticos y Soluciones

Sección con las guías de prácticos oficiales y los códigos y cuadernos Jupyter correspondientes a sus soluciones.

#### [📂 Práctico 0](practicos/practico0/) (Repaso de Programación y Álgebra Lineal)
* 📄 Enunciado oficial de la guía: [practico_0.pdf](practicos/practico0/practico_0.pdf)
* 💻 Ejercicios resueltos:
  * [sol_ej1.ipynb](practicos/practico0/sol_ej1.ipynb) - Jupyter Notebook con la resolución y análisis del Ejercicio 1.
  * [sol_ej2.ipynb](practicos/practico0/sol_ej2.ipynb) - Jupyter Notebook con la resolución del Ejercicio 2.
  * [sol_ej5.py](practicos/practico0/sol_ej5.py) - Solución del Ejercicio 5 escrita en script puro de Python.
  * [sol_ej7.py](practicos/practico0/sol_ej7.py) - Solución del Ejercicio 7 escrita en script puro de Python.

#### [📂 Práctico 1](practicos/practico1/) (Descomposición de Cholesky y LU)
* 📄 Enunciado oficial de la guía: [practico_1.pdf](practicos/practico1/practico_1.pdf)
* 💻 Ejercicios resueltos:
  * [ejercicio_1b.py](practicos/practico1/ejercicio_1b.py) - Implementación de la solución del Ejercicio 1b.
  * [ejercicio_2.ipynb](practicos/practico1/ejercicio_2.ipynb) - Resolución y simulaciones del Ejercicio 2 en Jupyter Notebook.
  * [ejercicio_4.ipynb](practicos/practico1/ejercicio_4.ipynb) - Resolución detallada del Ejercicio 4 en Jupyter Notebook.
  * [ejercicio_5.py](practicos/practico1/ejercicio_5.py) - Script de soporte con la resolución del Ejercicio 5.

#### [📂 Práctico 2](practicos/practico2/) (Sensibilidad, Normas y LU)
* 📄 Enunciado oficial de la guía: [practico_2.pdf](practicos/practico2/practico_2.pdf)
* 💻 Ejercicios resueltos:
  * [ejercicio_1.ipynb](practicos/practico2/ejercicio_1.ipynb) - Resolución en Jupyter Notebook del Ejercicio 1.
  * [ejercicio_2.ipynb](practicos/practico2/ejercicio_2.ipynb) - Resolución en Jupyter Notebook del Ejercicio 2.
  * [ejercicio_3.ipynb](practicos/practico2/ejercicio_3.ipynb) - Resolución en Jupyter Notebook del Ejercicio 3.
  * [ejercicio_5.py](practicos/practico2/ejercicio_5.py) - Solución del Ejercicio 5 en script de Python (Eliminación Gaussiana).
  * [ejercicio_6.py](practicos/practico2/ejercicio_6.py) - Implementación del algoritmo de factorización LU in-place (`dlu`).
  * [ejercicio_7.ipynb](practicos/practico2/ejercicio_7.ipynb) - Resolución en Jupyter Notebook del Ejercicio 7.
  * [ejercicio_10.py](practicos/practico2/ejercicio_10.py) - Implementación de Eliminación Gaussiana con pivoteo parcial (`egaussp`).
  * [ejercicio_11.py](practicos/practico2/ejercicio_11.py) - Script de prueba y validación del Ejercicio 11.
  * [ejercicio_12.py](practicos/practico2/ejercicio_12.py) - Script de prueba y validación del Ejercicio 12.
  * [ejercicio_15.py](practicos/practico2/ejercicio_15.py) - Análisis de sensibilidad, condicionamiento y gráficos del Ejercicio 15.

#### [📂 Práctico 3](practicos/practico3/) (Ortogonalidad, QR y Mínimos Cuadrados)
* 📄 Enunciado oficial de la guía: [practico_3.pdf](practicos/practico3/practico_3.pdf)
* 💻 Ejercicios resueltos:
  * [ejercicio_1.ipynb](practicos/practico3/ejercicio_1.ipynb) - Resolución en Jupyter Notebook del Ejercicio 1.
  * [ejercicio_5.ipynb](practicos/practico3/ejercicio_5.ipynb) - Resolución en Jupyter Notebook del Ejercicio 5.
  * [ejercicio_10.py](practicos/practico3/ejercicio_10.py) - Script con resolución y ajustes del Ejercicio 10.
  * [ejercicio_11.py](practicos/practico3/ejercicio_11.py) - Script con resolución y gráficos del Ejercicio 11.
* 📊 Datasets y archivos adjuntos:
  * [A_dataset.txt](practicos/practico3/A_dataset.txt) - Matriz de datos para ejercicios de mínimos cuadrados.
  * [b_dataset.txt](practicos/practico3/b_dataset.txt) - Vector de términos independientes.

#### [📂 Práctico 4](practicos/practico4/) (Cuadrados Mínimos)
* 📄 Enunciado oficial de la guía: [practico_4.pdf](practicos/practico4/practico_4.pdf)
* 💻 Ejercicios resueltos:
  * [ejercicio_3.py](practicos/practico4/ejercicio_3.py) - Implementación de descomposición QR mediante rotaciones de Givens.
  * [ejercicio_10.py](practicos/practico4/ejercicio_10.py) - Carga y procesamiento de datos para regresión polinomial.
* 📊 Datasets y archivos adjuntos:
  * [datos_p4ej12.npz](practicos/practico4/datos_p4ej12.npz) - Dataset comprimido en NumPy para el Ejercicio 12.
  * [y_mes1.txt](practicos/practico4/y_mes1.txt) - Mediciones del mes 1.
  * [y_mes2.txt](practicos/practico4/y_mes2.txt) - Serie de mediciones del mes 2.

---

### ⚙️ Herramientas de Uso Frecuente

#### Visualización de Diapositivas (Marp)
Las diapositivas están creadas bajo la especificación **Marp**. Puedes editarlas o visualizarlas localmente mediante la extensión oficial de **Marp for VS Code** o corriendo el compilador CLI:
```bash
# Compilar una clase a PDF
npx @marp-team/marp-cli@latest clases/XX/clase_XX.md --pdf

# Iniciar servidor de previsualización interactiva
npx @marp-team/marp-cli@latest clases/XX/clase_XX.md -p
```

#### Ejecución de Jupyter Notebooks y Entorno de Python
Para ejecutar los archivos `.ipynb` y los scripts `.py` sin problemas de dependencias, se recomienda inicializar un entorno virtual de Python 3 y realizar la instalación de los paquetes fundamentales (`numpy`, `scipy`, `matplotlib`, `jupyter`, `streamlit`, `pillow`):

```bash
# Crear entorno virtual
python -m venv env

# Activar el entorno virtual
# En Windows (PowerShell):
.\env\Scripts\activate
# En macOS/Linux:
source env/bin/activate

# Instalar dependencias
pip install numpy scipy matplotlib jupyter streamlit pillow

# Iniciar Jupyter Notebook
jupyter notebook
```

#### 🖼️ Aplicación Interactiva de Compresión SVD (Streamlit)
Para correr la demo interactiva de compresión y aproximación de bajo rango de imágenes con SVD ([app_svd_imagen.py](clases/09/app_svd_imagen.py)):

```bash
# Ejecutar la aplicación con Streamlit
streamlit run clases/09/app_svd_imagen.py
```

Se abrirá automáticamente una ventana en el navegador web (por defecto en `http://localhost:8501`) donde podrás:
* Cargar cualquier imagen en formato `.png`, `.jpg`, `.jpeg`, `.bmp` o `.webp` (o usar la imagen sintética generada por defecto).
* Ajustar interactivamente el número de valores singulares ($k$) mediante una barra deslizante para observar la reconstrucción $A_k = \sum_{i=1}^k \sigma_i u_i v_i^T$.
* Visualizar el decaimiento del espectro de valores singulares $\sigma_i$ (en escala lineal o logarítmica).
* Comparar el error de aproximación en norma 2 ($\|A - A_k\|_2 = \sigma_{k+1}$) y la tasa de compresión y almacenamiento en bytes.
