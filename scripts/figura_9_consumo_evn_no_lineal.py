from general import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

esperanza_vida = pd.read_csv("../datos reales/esperanza_vida.csv").drop("Series Code", axis=1)
def Cambiar(s : str):
    if s[-1]==']': return s[:4]
    return s

esperanza_vida.columns = list(map(Cambiar, esperanza_vida.columns))
esperanza_vida[esperanza_vida=='..'] = pd.NA

colmujer = esperanza_vida['Series Name'].unique()[0]
colhombre = esperanza_vida['Series Name'].unique()[1]
coltotal = esperanza_vida['Series Name'].unique()[2]

mujeres = esperanza_vida[esperanza_vida['Series Name']==colmujer]
hombres = esperanza_vida[esperanza_vida['Series Name']==colhombre]
total = esperanza_vida[esperanza_vida['Series Name']==coltotal]

percentiles_ingresos = pd.read_csv("../datos reales/percentiles_ingresos_PPA_2011.csv")

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

def GenerarMuestra(datos_originales, evida, umbral):
    muestras = dict()
    for year in sorted(datos_originales['year'].unique()):
        datos_anio = datos_originales[datos_originales['year']==year]
        paises = datos_anio['country_code'].unique()
        
        paises = list(filter(lambda x : 
            sum(datos_anio['country_code']==x)==100, paises
        ))
        esp_vida = evida[~ total[str(year)].isna()]
        paises = set(paises).intersection(esp_vida['Country Code'].unique())
        paises = list(paises) 

        if len(paises) < umbral: continue
        
        grupos_in = datos_anio.groupby('country_code')
        
        muestras[year] = []
        
        esp_vida.set_index('Country Code', inplace=True)

        for country in paises:
            tams = (1,10,20,100)
            muestra = []
            for (i,tam) in enumerate(tams):
                muestra.append(Sintetizador(tam)(grupos_in.get_group(country)))
            muestras[year].append((country,muestra, esp_vida.loc[country][str(year)]))
    return muestras

percentiles_ingresos_ni = percentiles_ingresos[
    np.array(percentiles_ingresos['welfare_type']=='income') &
    np.array(percentiles_ingresos['reporting_level']=='national')
]

percentiles_ingresos_comp = percentiles_ingresos[
    np.array(percentiles_ingresos['welfare_type']=='consumption') &
    np.array(percentiles_ingresos['reporting_level']=='national')
]

muestras_ingreso = GenerarMuestra(percentiles_ingresos_ni,total,30)
muestras_consumo = GenerarMuestra(percentiles_ingresos_comp,total,30)

import random
def GenerarSeriesQuantilica(muestras, metrica, samples = 10):
    
    xs = list(sorted(muestras.keys()))
    yq1 = [[] for _ in range(4)]
    yq2 = [[] for _ in range(4)]
    yq3 = [[] for _ in range(4)]
    for x in xs:
        muestra = muestras[x]
        
        series = [[] for i in range(4)]
        
        random.seed(123456)
        remuestreos = [
            random.choices(muestra,k=len(muestra)) for _ in range(samples)
        ]
        for remuestreo in remuestreos:
            for i in range(4):
                a = [item[1][i] for item in remuestreo]
                b = [float(item[2]) for item in remuestreo]
                series[i].append(metrica(a,b))
        for i in range(4):
            yq1[i].append(np.quantile(series[i],q=0.25))
            yq2[i].append(np.quantile(series[i],q=0.5 ))
            yq3[i].append(np.quantile(series[i],q=0.75))
            
        # for i in range(4):
        #    a = [item[1][i] for item in muestra]
        #    b = [float(item[2]) for item in muestra]
        #    series.append(metrica(a,b))
        # ys.append(tuple(series))
    return xs,yq1, yq2, yq3

from scipy import stats
# from minepy import MINE
import dcor

def Spearman(x, y):
    corr, _ = stats.spearmanr(x,y)
    return corr

def Kendall(x, y):
    corr, _ = stats.kendalltau(x,y)
    return corr

#def MIC(x, y):
#    mine = MINE()
#    mine.compute_score(x,y)
#    return mine.mic()

metricas = [
    (Spearman, "Correlación de Spearman"),
    (Kendall, "$\\tau$ de Kendall"),
   # (dcor.distance_correlation, "correlación de distancias"),
   #  (MIC, "Coeficiente de Información Maximal")
]

fig, axs = plt.subplots(len(metricas),1, figsize=(24,10 * len(metricas)))
fig.subplots_adjust(top=0.90) 
fig.suptitle('Consumo vs EVN con resampleo', fontsize=40)

muestra = muestras_consumo
#muestras = [muestras_ingreso, muestras_consumo]
#nombres_m = "Ingresos"
nombres =  ["Percentiles","Deciles","Quintiles","Total"]
# estilos =  ['-','--','-.',':']

xticks = list(range(2002,2022))
xlabel_ticks = list(map(str, xticks))

yticks_mayor = np.linspace(0.25,0.95,15)
yticks_menor = np.linspace(0.25,0.95,29)


cmap = plt.get_cmap('tab10')
for (ax,(metrica, nombre_metrica)) in zip(axs,metricas):
    xs, yq1, yq2, yq3 = GenerarSeriesQuantilica(muestra, metrica, samples=1000)
    for (i, nombre) in enumerate(nombres):
        color = cmap(i)
        ax.plot(xs,yq2[i], label = nombre, linewidth=3, c=color)
        ax.plot(xs,yq1[i], linewidth=2, linestyle='--', c=color)
        ax.plot(xs,yq3[i], linewidth=2, linestyle='--', c=color)
        ax.fill_between(xs, yq1[i], yq3[i], alpha=0.25, color=color)

    ax.set_ylabel(f"{nombre_metrica} con EVN", fontsize=20)
    ax.set_xlabel("Año", fontsize=20)
    ax.set_title(f"Utilizando {nombre_metrica}", fontsize = 28)
    ax.set_xticks(ticks = xticks, labels= xlabel_ticks, rotation=90, fontsize=18)
    # ax.set_xticks(ticks = xticks, labels=[None]*len(xticks))
    ax.set_yticks(ticks = yticks_mayor, minor=False, labels=list(map(lambda x: f"{x:.2f}", yticks_mayor)), fontsize=18)
    ax.set_yticks(ticks = yticks_menor, minor=True)
    ax.grid(c='black', linestyle='--')
    ax.grid(c='gray', linestyle='--', which='minor')
    #ax.set_facecolor('lightgray')
    ax.legend(fontsize=24)

fig.savefig("../figuras/figura_9_consumo_evn_no_lineal.png",bbox_inches='tight')
