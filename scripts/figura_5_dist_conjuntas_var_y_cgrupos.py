from general import *
import matplotlib.pyplot as plt
import numpy as np

datos_varianzas = pd.read_csv("../datos simulados/datos_varianzas.csv", sep='\t')


def Grafico(ax, varianza, grupoX, grupoY):
    datos = datos_varianzas[datos_varianzas["-1"]==varianza]
    x = datos[grupoX]
    y = datos[grupoY]
    # Crear el gráfico hexbin
    h = ax.hexbin(x, y, gridsize=30, cmap="Blues", mincnt=1)
    ax.set_title(f"Varianza = {varianza}", fontsize=19)
    ax.set_xlabel(f"{1_000_000//int(grupoX)} grupos", fontsize=16)
    ax.set_ylabel(f"{1_000_000//int(grupoY)} grupos", fontsize=16)
    ax.grid(alpha=0.25, linestyle='--')
    #ax.axis('equal')
    return h  # Retornar el objeto hexbin

# Crear subgráficos
fig, axs = plt.subplots(3, 2, figsize=(19, 24))

# Llamar a la función Grafico y guardar el objeto hexbin
h1 = Grafico(axs[0, 0], 1, '1', '1000000')
h2 = Grafico(axs[0, 1], 1, '1', '200000')
h3 = Grafico(axs[1, 0], 5, '1', '1000000')
h4 = Grafico(axs[1, 1], 5, '1', '200000')
h5 = Grafico(axs[2, 0], 10, '1', '1000000')
h6 = Grafico(axs[2, 1], 10, '1', '10000')

# Agregar una colorbar debajo de todos los hexbin
# cbar = fig.colorbar(h1, ax=axs, orientation='horizontal', pad=0.02)
# cbar.set_label('Densidad de puntos', fontsize=12)

fig.suptitle("Distribución conjunta con distintas varianzas y cantidades de grupos",fontsize=28)
fig.subplots_adjust(top=0.93) 

#plt.tight_layout()  # Ajustar el espacio entre subgráficos
fig.savefig("../figuras/figura_5_dist_conjuntas_var_y_cgrupos.png",bbox_inches='tight')

