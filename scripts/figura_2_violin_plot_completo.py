import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datos = pd.read_csv('../datos simulados/datos.csv')
columnas = [str(1000000//int(x)) for x in datos.columns]
y = list(zip(*datos.iloc))
ymin = min([min(yy) for yy in y])
y = [np.array(yi)-ymin for yi in y]
quants = (0.25,0.5,0.75)
quantiles = [ [np.quantile(yi,q=quant) for yi in y] for quant in quants]

import matplotlib.ticker as ticker
fig, axs = plt.subplots(2,1, figsize=(20,22))
fig.suptitle("Medición del Bienestar Económico Per Capita en datos simulados", fontsize=28)
for ax in axs:
    ax.violinplot(y, showmedians=True)
    for (quant, quantil) in zip(quants,quantiles):
        ax.plot(range(1,len(columnas)+1),quantil, label=f"Cuantil {quant}", linewidth=3)
    #ax.scatter(x2, y2, color = "red", alpha = 0.025)
    ax.set_xticks(range(1,len(columnas)+1), columnas, rotation = 90)
    ax.set_xlabel("Número de grupos", fontsize=22)
    ax.tick_params(axis='x', rotation = 90)
    ax.tick_params(labelsize=18)
    ax.set_ylim(1e-10,0.55)
    ax.grid()
    ax.legend(fontsize=18)

axs[0].set_ylabel("Bienestar Económico Per Capita", fontsize=22)
axs[1].set_ylabel("Bienestar Económico Per Capita (log)", fontsize=22)
axs[1].set_yscale('log')
axs[1].yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=11))
axs[1].yaxis.set_major_formatter(ticker.LogFormatter())
fig.subplots_adjust(top=0.95) 

fig.savefig("../figuras/figura_2_violin_plot_completo.png", bbox_inches='tight')