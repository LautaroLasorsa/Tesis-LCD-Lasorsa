from general import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from scipy.stats import pearsonr, spearmanr

simulados = pd.read_csv("../datos simulados/datos_varianzas.csv", sep='\t')
sg = simulados.groupby(['-1'])

plt.figure(dpi=900, figsize=(9.6,4.8))
ng = list(filter(lambda x : 100%x==0, range(1,101)))
series = [ [] for _ in ng ]

for s2 in sg.groups:
    t = sg.get_group(s2).to_numpy().T[-(len(ng)):]
    for i in range(len(ng)):
        series[i].append(pearsonr(t[i],t[-1]).correlation)

for i in range(len(ng)):
    plt.plot(sg.groups.keys(),series[i], label=f"{ng[i]}",
            c = colormaps.get("plasma")(2*(i//2)/len(ng)),
            linestyle=["-","--"][i%2])

plt.ylim(0,1)
plt.yticks(np.linspace(0,1,11), minor = False)
plt.yticks(np.linspace(0,1,21), minor = True)
plt.grid()
plt.grid(linestyle='--', which='minor')
plt.xticks(range(1,11), sg.groups.keys())
plt.xlabel("$\sigma^2$")
plt.ylabel("Pearson")
plt.legend(ncol=3, title="Número grupos")
plt.title("$\sigma^2$ y correlación entre frente a usar 100 grupos")

plt.savefig("../figuras/figura_12_pearson_hasta_100_grupos.png",bbox_inches='tight')