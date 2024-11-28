from general import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

datos = pd.read_csv("../datos reales/percentiles_ingresos_PPA_2011.csv")
simulados = pd.read_csv("../datos simulados/datos_varianzas.csv", sep='\t')

def Sintetizador(tam = 100):
    def Sintesis(ingresos):
        sintesis = 0
        for ini in range(0,100,tam):
            rango = ingresos.iloc[ini:(ini+tam)]
            peso = np.sum(rango['pop_share'])
            avg_rango = np.sum(rango['avg_welfare'] * rango['pop_share'])/peso
            sintesis += np.log(avg_rango)*peso
        return sintesis
    return Sintesis

def GenerarMuestra(muestra):
    tams = list(filter(lambda x: 100%x==0, range(1,101)))
    series = [ [] for _ in range(len(tams))]
    mg = muestra.groupby(['country_code','year'])
    for grupo in mg.groups:
        sample = mg.get_group(grupo)
        if len(sample)!=100: continue
        for i in range(len(tams)):
            series[-1-i].append(Sintetizador(tams[i])(sample))
    return series

datos = datos[(datos['reporting_level']=='national')]
dg = datos.groupby(['welfare_type'])
ingresos = dg.get_group('income')
consumo  = dg.get_group('consumption')

var_ingresos = GenerarMuestra(ingresos)
var_consumo = GenerarMuestra(consumo)

fig, axs = plt.subplots(2,1, figsize=(30,20))

x = list(filter(lambda x : 100%x==0, range(1,101)))
x = list(map(str, x))
def Plot(ax, y, corr, label):
    xs = list(range(len(x)))
    ys = [corr(yi,y[-1]).correlation for yi in y]
    ax.plot(xs,ys, label = label, linewidth=5)

sg = simulados.groupby(['-1'])
for (i, corr) in enumerate([pearsonr, spearmanr]):
    Plot(axs[i], var_ingresos,corr, "Ingresos")
    Plot(axs[i], var_consumo,corr, "Consumo")
for s2 in [1,10]:
    vals = sg.get_group(s2).to_numpy().T[-(len(x)):]
    Plot(axs[0], vals,pearsonr, f"$\sigma^2={s2}$")
    Plot(axs[1], vals,spearmanr, f"$\sigma^2={s2}$")
for ax in axs:
    ax.set_xticks(range(len(x)), x, fontsize=16)
    ax.set_yticks(
        np.linspace(0.65,1,8),
        list(map(lambda x : f"{x:.2f}",np.linspace(0.65,1,8))),
        fontsize=16)
    ax.legend(fontsize=24)
    ax.set_xlabel("Número de Grupos (X)", fontsize=24)
    ax.grid(linewidth=3)
axs[0].set_ylabel("Pearson entre $BE_{X}$ y $BE_{100}$", fontsize=24)
axs[1].set_ylabel("Spearman entre $BE_{X}$ y $BE_{100}$", fontsize=24)
fig.suptitle("Correlación entre $BE_{X}$ y $BE_{100}$", fontsize=48)
fig.subplots_adjust(top=0.93) 

fig.savefig("../figuras/figura_14_correlacion_vs_100_empirica.png",bbox_inches='tight')