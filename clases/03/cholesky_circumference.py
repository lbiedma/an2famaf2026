import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def generar_spd_aleatoria():
    """Genera una matriz 2x2 Simétrica y Definida Positiva."""
    # Construcción A = M^T * M para asegurar que sea SPD [1, 2]
    M = np.random.randn(2, 2)
    A = M.T @ M 
    # Añadimos una pequeña identidad para evitar matrices casi singulares
    A += 0.1 * np.eye(2)
    return A

def actualizar_trama(event=None):
    """Lógica para generar la matriz y actualizar los gráficos."""
    A = generar_spd_aleatoria()
    
    # Generar puntos de la circunferencia unidad [3]
    theta = np.linspace(0, 2*np.pi, 200)
    circunferencia = np.array([np.cos(theta), np.sin(theta)])
    
    # Aplicar la transformación lineal y = Ax [3]
    elipse = A @ circunferencia
    
    # Obtener autovalores y autovectores para ilustrar los ejes [4]
    evals, evecs = np.linalg.eigh(A)
    
    # Limpiar y redibujar
    ax.clear()
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Dibujar circunferencia unidad
    ax.plot(circunferencia[0, :], circunferencia[1, :], 'k--', label='Circunferencia Unidad')
    
    # Dibujar elipse transformada
    ax.plot(elipse[0, :], elipse[1, :], 'b-', linewidth=2, label='Transformación (Ax)')
    ax.fill(elipse[0, :], elipse[1, :], 'blue', alpha=0.1)
    
    # Dibujar los autovectores escalados por autovalores (ejes de la elipse) [3, 4]
    for i in range(2):
        v = evecs[:, i] * evals[i]
        ax.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, 
                  color='red', width=0.015, label=f'Autovector {i+1}' if i==0 else "")

    ax.set_title(f"Matriz SPD Aleatoria:\n{np.round(A, 3)}")
    ax.legend(loc='upper right', fontsize='small')
    
    # Ajustar límites de la pantalla
    limit = np.max(np.abs(elipse)) + 0.5
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    plt.draw()

# --- Configuración de la interfaz ---
fig, ax = plt.subplots(figsize=(7, 7))
plt.subplots_adjust(bottom=0.2)

# Botón para regenerar
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
btn = Button(ax_button, 'Generar Matriz')
btn.on_clicked(actualizar_trama)

# Ejecución inicial
actualizar_trama()
plt.show()
