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
fig.suptitle('C.C.de Pearson del ingreso con la esperanza de vida', fontsize=40)

muestras = [muestras_ingreso, muestras_consumo]
nombres_m = ["ingresos","consumo"]
nombres =  ["Percentiles","Deciles","Quintiles","Total", "GNI per capita", "GNI PC corregido", "Mediana"]
estilos =  ['-','--','-.',':', (0,(2,3,1,2)), (0,(2,2,1,1,3,3)), None]

xticks = list(range(1994,2022))
xlabel_ticks = list(map(str, xticks))

yticks_mayor = np.linspace(0.40,0.9,11)
yticks_menor = np.linspace(0.40,0.9,21)

import random
def GenerarSeriesQuantilica(muestras, metrica, samples = 10):
    
    xs = list(sorted(muestras.keys()))
    yq1 = [[] for _ in range(len(nombres))]
    yq2 = [[] for _ in range(len(nombres))]
    yq3 = [[] for _ in range(len(nombres))]
    for x in xs:
        muestra = muestras[x]
        
        series = [[] for i in range(len(nombres))]
        
        random.seed(123456)
        remuestreos = [
            random.choices(muestra,k=len(muestra)) for _ in range(samples)
        ]
        for remuestreo in remuestreos:
            for i in range(len(nombres)):
                a = [float(item[1][i]) for item in remuestreo]
                b = [float(item[2]) for item in remuestreo]
                series[i].append(metrica(a,b))
        for i in range(len(nombres)):
            yq1[i].append(np.quantile(series[i],q=0.25))
            yq2[i].append(np.quantile(series[i],q=0.5 ))
            yq3[i].append(np.quantile(series[i],q=0.75))
            
        # for i in range(4):
        #    a = [item[1][i] for item in muestra]
        #    b = [float(item[2]) for item in muestra]
        #    series.append(metrica(a,b))
        # ys.append(tuple(series))
    return xs,yq1, yq2, yq3

cmap = plt.get_cmap('tab10')
for (ax,muestra,nombre_muestra) in zip(axs,muestras,nombres_m):
    xs, yq1, yq2, yq3 = GenerarSeriesQuantilica(muestra, lambda x,y : np.corrcoef(x,y)[0,1], samples=1000)
    for (i, nombre) in enumerate(nombres):
        color = cmap(i)
        ax.plot(xs,yq2[i], label = nombre, linewidth=3, c=color)
        ax.plot(xs,yq1[i], linewidth=2, linestyle='--', c=color)
        ax.plot(xs,yq3[i], linewidth=2, linestyle='--', c=color)
        ax.fill_between(xs, yq1[i], yq3[i], alpha=0.25, color=color)

    ax.set_ylabel("C.C. de Perason con Esperanza de Vida al nacer", fontsize=20)
    ax.set_xlabel("Año", fontsize=20)
    ax.set_title(f"Utilizando encuestas de {nombre_muestra}", fontsize = 28)
    ax.set_xticks(ticks = xticks, labels= xlabel_ticks, rotation=90, fontsize=18)
    # ax.set_xticks(ticks = xticks, labels=[None]*len(xticks))
    ax.set_yticks(ticks = yticks_mayor, minor=False, labels=list(map(lambda x: f"{x:.2f}", yticks_mayor)), fontsize=18)
    ax.set_yticks(ticks = yticks_menor, minor=True)
    ax.grid(c='black', linestyle='--')
    ax.grid(c='gray', linestyle='--', which='minor')
    #ax.set_facecolor('lightgray')
    ax.legend(fontsize=24)

# plt.show()
fig.savefig("../figuras/figura_20_empirico_todas_metricas_vs_evn_pearson_bootstrap.png",bbox_inches='tight')