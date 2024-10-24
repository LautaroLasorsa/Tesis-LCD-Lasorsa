from general import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

esperanza_vida = pd.read_csv("../datos reales/esperanza_vida.csv").drop("Series Code", axis=1)
def Cambiar(s : str):
    if s[-1]==']': return s[:4]
    return s

esperanza_vida.columns = list(map(Cambiar, esperanza_vida.columns))
esperanza_vida[esperanza_vida=='..'] = pd.NA

gni_ppa = pd.read_csv("../datos reales/gni_ppa_2021_per_capita.csv")
gni_ppa.columns = list(map(Cambiar, gni_ppa.columns))
gni_ppa[gni_ppa=='..'] = pd.NA


coltotal = esperanza_vida['Series Name'].unique()[2]
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

        gni = gni_ppa[~gni_ppa[str(year)].isna()]
        paises = set(paises).intersection(gni['Country Code'].unique())
        paises = list(paises) 
    
        if len(paises) < umbral: continue
        
        grupos_in = datos_anio.groupby('country_code')
        
        muestras[year] = []
        
        esp_vida.set_index('Country Code', inplace=True)
        gni.set_index('Country Code', inplace=True)

        for country in paises:
            tams = (1,10,20,100)
            muestra = []
            for (i,tam) in enumerate(tams):
                muestra.append(Sintetizador(tam)(grupos_in.get_group(country)))
            muestra.append(np.log(float(gni.loc[country][str(year)])))
            
            A = np.exp(muestra[0]-muestra[-1])
            muestra.append(np.log(float(gni.loc[country][str(year)]) * A))

            muestra.append(np.log(np.quantile(grupos_in.get_group(country)['avg_welfare'], q=0.5)))
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

muestras_ingreso = GenerarMuestra(percentiles_ingresos_ni,total,20)
muestras_consumo = GenerarMuestra(percentiles_ingresos_comp,total,20)

fig, axs = plt.subplots(2,1, figsize=(24,20))
fig.subplots_adjust(top=0.90) 
fig.suptitle('C.C.de Spearman del ingreso con la esperanza de vida', fontsize=40)

muestras = [muestras_ingreso, muestras_consumo]
nombres_m = ["ingresos","consumo"]
nombres =  ["Percentiles","Deciles","Quintiles","Total", "GNI per capita", "GNI PC corregido", "Mediana"]
estilos =  ['-','--','-.',':', (0,(2,3,1,2)), (0,(2,2,1,1,3,3)), (0,(3,1))]

xticks = list(range(1994,2022))
xlabel_ticks = list(map(str, xticks))

yticks_mayor = np.linspace(0.55,0.9,8)
yticks_menor = np.linspace(0.55,0.9,15)

def GenerarSeries(muestras, metrica):
    xs = list(sorted(muestras.keys()))
    ys = []
    for x in xs:
        muestra = muestras[x]
        series = []
        for i in range(len(muestra[0][1])):
            a = [float(item[1][i]) for item in muestra]
            b = [float(item[2]) for item in muestra]
            series.append(metrica(a,b))
        ys.append(tuple(series))
    return xs,ys

for (ax,muestra,nombre_muestra) in zip(axs,muestras,nombres_m):
    xs, ys = GenerarSeries(muestra, lambda x,y : spearmanr(x,y).correlation)
    for (i, nombre, estilo) in zip(range(len(nombres)),nombres,estilos):
        ax.plot(xs,[y[i] for y in ys], label = nombre, linestyle=estilo, marker='x', linewidth=3, markersize = 15, markeredgewidth=3)
    
    ax.set_ylabel("C.C. de Spearman con Esperanza de Vida al nacer", fontsize=20)
    ax.set_xlabel("Año", fontsize=20)
    ax.set_title(f"Utilizando encuestas de {nombre_muestra}", fontsize = 28)
    ax.set_xticks(ticks = xticks, labels= xlabel_ticks, rotation=90, fontsize=18)
    # ax.set_xticks(ticks = xticks, labels=[None]*len(xticks))
    ax.set_yticks(ticks = yticks_mayor, minor=False, labels=list(map(lambda x: f"{x:.2f}", yticks_mayor)), fontsize=18)
    # ax.set_yticks(ticks = yticks_menor, labels=("" for _ in yticks_menor), linestyle=(0,(2,1)), minor=True)
    ax.grid(c='black', linestyle='--')
    ax.set_facecolor('lightgray')
    ax.legend(fontsize=24)


fig.savefig("../figuras/figura_21_empirico_todas_metricas_vs_evn_spearman.png",bbox_inches='tight')