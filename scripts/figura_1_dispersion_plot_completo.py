from general import * 

datos = pd.read_csv('../datos simulados/datos.csv')
columnas = [str(1000000//int(x)) for x in datos.columns]
y = list(zip(*datos.iloc))

y2 = []
x2 = []
for (yy,xx) in zip(y, columnas):
    y2.extend(yy)
    x2.extend([xx]*len(yy))

import matplotlib.ticker as ticker
fig, axs = plt.subplots(2,1, figsize=(20,22))
fig.suptitle("Medición del Bienestar Económico Per Capita en datos simulados", fontsize=28)
for ax in axs:
    ax.scatter(x2, y2, color = "red", alpha = 0.025)
    ax.set_xlabel("Número de grupos", fontsize=22)
    ax.tick_params(axis='x', rotation = 90)
    ax.tick_params(labelsize=18)
    ax.grid()

axs[0].set_ylabel("Bienestar Económico Per Capita", fontsize=22)
axs[1].set_ylabel("Bienestar Económico Per Capita (log)", fontsize=22)
axs[1].set_yscale('log')
axs[1].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=11))
axs[1].yaxis.set_major_formatter(ticker.LogFormatter())
fig.subplots_adjust(top=0.95) 

fig.savefig("../figuras/figura_1_dispersion_plot_completo.png", bbox_inches='tight')