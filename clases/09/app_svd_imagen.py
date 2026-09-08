import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Configuración inicial de la página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Aproximación de Imágenes por SVD",
    page_icon="🖼️",
    layout="wide"
)

# -----------------------------------------------------------------------------
# Funciones auxiliares y caché
# -----------------------------------------------------------------------------
def generar_imagen_ejemplo():
    """Genera una imagen sintética de prueba si el usuario no sube ninguna."""
    w, h = 640, 480
    img = Image.new("L", (w, h), color=240)
    draw = ImageDraw.Draw(img)
    
    # Dibujar algunas formas geométricas y gradientes
    draw.ellipse([80, 60, 320, 300], fill=60, outline=0, width=4)
    draw.rectangle([250, 180, 520, 400], fill=140, outline=30, width=3)
    draw.polygon([(400, 50), (580, 200), (300, 220)], fill=100)
    
    # Texto representativo
    draw.text((120, 380), "SVD - FAMAF 2026", fill=20, font_size=36)
    return img

def redimensionar_si_es_necesario(img: Image.Image, max_alto: int = 480) -> Image.Image:
    """Redimensiona la imagen para que su alto no supere max_alto manteniendo el aspecto."""
    ancho, alto = img.size
    if alto > max_alto:
        nuevo_alto = max_alto
        nuevo_ancho = int(ancho * (max_alto / alto))
        img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    return img

@st.cache_data
def calcular_svd(matriz: np.ndarray):
    """
    Calcula la descomposición SVD A = U S V^T.
    Cacheada para evitar recalcular la SVD al mover el slider de k.
    """
    U, S, Vt = np.linalg.svd(matriz, full_matrices=False)
    return U, S, Vt

def reconstruir_matriz(U: np.ndarray, S: np.ndarray, Vt: np.ndarray, k: int) -> np.ndarray:
    """Reconstruye la aproximación de rango k: A_k = sum_{i=1}^k sigma_i u_i v_i^T."""
    Ak = U[:, :k] @ (S[:k, np.newaxis] * Vt[:k, :])
    Ak = np.clip(Ak, 0, 255).astype(np.uint8)
    return Ak

# -----------------------------------------------------------------------------
# Interfaz de usuario (Streamlit)
# -----------------------------------------------------------------------------
st.title("🖼️ Aproximación de Imágenes usando SVD")
st.markdown("""
Esta aplicación permite analizar cómo la **Descomposición en Valores Singulares (SVD)** permite aproximar una imagen 
en escala de grises reduciendo su rango y comprimiendo su información (Teorema de Eckart-Young).
""")

# Barra lateral para configuración y carga de archivos
with st.sidebar:
    st.header("⚙️ Configuración")
    archivo_subido = st.file_uploader("Carga tu propia imagen", type=["png", "jpg", "jpeg", "bmp", "webp"])
    
    max_alto_opcion = st.number_input(
        "Alto máximo deseado (px):", 
        min_value=100, 
        max_value=1080, 
        value=480, 
        step=40,
        help="Si la imagen supera este alto, se redimensionará para agilizar el cálculo de la SVD."
    )
    
    escala_log = st.checkbox("Escala logarítmica para valores singulares", value=True)

# Obtener la imagen de entrada (subida o de ejemplo)
if archivo_subido is not None:
    img_original = Image.open(archivo_subido)
else:
    st.info("💡 No se ha subido una imagen. Usando imagen sintética de prueba. Puedes subir la tuya desde la barra lateral.")
    img_original = generar_imagen_ejemplo()

# Convertir a escala de grises y redimensionar
img_grises = ImageOps.grayscale(img_original)
img_procesada = redimensionar_si_es_necesario(img_grises, max_alto=max_alto_opcion)

matriz_A = np.array(img_procesada, dtype=np.float64)
m, n = matriz_A.shape
rango_maximo = min(m, n)

# Calcular SVD (eficiente y en caché)
with st.spinner("Calculando descomposición SVD..."):
    U, S, Vt = calcular_svd(matriz_A)

# Selector del rango k
st.subheader("🎯 Selección del Rango $k$")
col_slider, col_num = st.columns([3, 1])

with col_slider:
    k_default = min(25, rango_maximo)
    k = st.slider("Número de valores singulares ($k$):", min_value=1, max_value=rango_maximo, value=k_default, step=1)

with col_num:
    st.metric(r"Rango Máximo $\min(m, n)$", f"{rango_maximo}")

# Reconstruir imagen con rango k
matriz_Ak = reconstruir_matriz(U, S, Vt, k)

# Métricas de compresión y precisión
energia_total = np.sum(S**2)
energia_retenida = np.sum(S[:k]**2)
pct_energia = (energia_retenida / energia_total) * 100

# Tamaño en memoria (número de floats)
floats_original = m * n
floats_k = k * (m + n + 1)
pct_compresion = (1 - (floats_k / floats_original)) * 100

sigma_k_plus_1 = S[k] if k < rango_maximo else 0.0

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Dimensiones", f"{m} × {n} px")
col_m2.metric(r"Energía Retenida ($\sum \sigma_i^2$)", f"{pct_energia:.2f} %")
col_m3.metric("Ahorro de Memoria", f"{pct_compresion:.1f} %" if pct_compresion > 0 else "0 %")
col_m4.metric(r"Error 2 ($\|A - A_k\|_2 = \sigma_{k+1}$)", f"{sigma_k_plus_1:.2f}")

st.divider()

# Visualización comparativa de imágenes
col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"### 📷 Imagen Original ($m \\times n = {m} \\times {n}$)")
    st.image(matriz_A.astype(np.uint8), use_container_width=True)

with col_right:
    st.markdown(f"### 🧮 Aproximación de Rango $k = {k}$")
    st.image(matriz_Ak, use_container_width=True)

# Pestañas adicionales para gráficos y teoría
tab_graficos, tab_error, tab_teoria = st.tabs(["📊 Gráfico de Valores Singulares", "🔥 Mapa de Error Residual", "📘 Teoría SVD"])

with tab_graficos:
    fig, ax = plt.subplots(figsize=(10, 4))
    indices = np.arange(1, rango_maximo + 1)
    
    if escala_log:
        ax.semilogy(indices, S, color='#2563EB', linewidth=2, label=r'Valores singulares $\sigma_i$')
    else:
        ax.plot(indices, S, color='#2563EB', linewidth=2, label=r'Valores singulares $\sigma_i$')
        
    ax.axvline(x=k, color='#DC2626', linestyle='--', linewidth=2, label=f'Rango seleccionado k = {k}')
    ax.set_xlabel('Índice $i$', fontsize=11)
    ax.set_ylabel(r'Valor singular $\sigma_i$' + (' (escala log)' if escala_log else ''), fontsize=11)
    ax.set_title('Decaimiento de los Valores Singulares', fontsize=13, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    st.pyplot(fig)

with tab_error:
    st.markdown("### Diferencia Absoluta $|A - A_k|$")
    error_matriz = np.abs(matriz_A - matriz_Ak.astype(np.float64))
    
    fig_err, ax_err = plt.subplots(figsize=(8, 4))
    im = ax_err.imshow(error_matriz, cmap='magma')
    plt.colorbar(im, ax=ax_err, label='Diferencia absoluta en intensidad')
    ax_err.set_title(f"Error Residual para k = {k}", fontsize=12, fontweight='bold')
    ax_err.axis('off')
    st.pyplot(fig_err)

with tab_teoria:
    st.markdown(r"""
    ### 📖 Descomposición en Valores Singulares (SVD)
    Toda matriz $A \in \mathbb{R}^{m \times n}$ se descompone como:
    $$ A = U \Sigma V^T = \sum_{i=1}^r \sigma_i u_i v_i^T $$

    ### 🏆 Teorema de Eckart-Young
    La mejor aproximación de rango $k$ (con $k < r$) para la matriz $A$ en la norma espectral $\| \cdot \|_2$ es:
    $$ A_k = \sum_{i=1}^k \sigma_i u_i v_i^T $$

    La norma del error de aproximación satisface exactamente:
    $$ \|A - A_k\|_2 = \sigma_{k+1} $$
    """)
