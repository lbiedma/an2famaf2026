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
  * [ejercicio_5.py](practicos/practico2/ejercicio_5.py) - Solución del Ejercicio 5 en script de Python.

#### [📂 Práctico 3](practicos/practico3/) (Ortogonalidad, QR y Mínimos Cuadrados)
* 📄 Enunciado oficial de la guía: [practico_3.pdf](practicos/practico3/practico_3.pdf)
* 📊 Datasets y archivos adjuntos:
  * [A_dataset.txt](practicos/practico3/A_dataset.txt) - Matriz de datos para ejercicios de mínimos cuadrados.
  * [b_dataset.txt](practicos/practico3/b_dataset.txt) - Vector de términos independientes.

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
Para ejecutar los archivos `.ipynb` y los scripts `.py` sin problemas de dependencias, se recomienda inicializar un entorno virtual de Python 3 y realizar la instalación de los paquetes fundamentales (`numpy`, `scipy`, `matplotlib`, `jupyter`):

```bash
# Crear entorno virtual
python -m venv env

# Activar el entorno virtual
# En Windows (PowerShell):
.\env\Scripts\activate
# En macOS/Linux:
source env/bin/activate

# Instalar dependencias
pip install numpy scipy matplotlib jupyter

# Iniciar Jupyter Notebook
jupyter notebook
```
