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

muestras_ingreso = GenerarMuestra(percentiles_ingresos_ni,total,20)
muestras_consumo = GenerarMuestra(percentiles_ingresos_comp,total,20)

fig, axs = plt.subplots(2,1, figsize=(24,20))
fig.subplots_adjust(top=0.90) 
fig.suptitle('C.C.de Pearson del ingreso con la esperanza de vida', fontsize=40)

muestras = [muestras_ingreso, muestras_consumo]
nombres_m = ["ingresos","consumo"]
nombres =  ["Percentiles","Deciles","Quintiles","Total"]
estilos =  ['-','--','-.',':']

xticks = list(range(1991,2022))
xlabel_ticks = list(map(str, xticks))

yticks_mayor = np.linspace(0.6,0.9,7)
yticks_menor = np.linspace(0.6,0.9,13)

def GenerarSeries(muestras, metrica):
    xs = list(sorted(muestras.keys()))
    ys = []
    for x in xs:
        muestra = muestras[x]
        series = []
        for i in range(4):
            a = [item[1][i] for item in muestra]
            b = [float(item[2]) for item in muestra]
            series.append(metrica(a,b))
        ys.append(tuple(series))
    return xs,ys

for (ax,muestra,nombre_muestra) in zip(axs,muestras,nombres_m):
    xs, ys = GenerarSeries(muestra, lambda x,y : np.corrcoef(x,y)[0,1])
    for (i, nombre, estilo) in zip(range(4),nombres,estilos):
        ax.plot(xs,[y[i] for y in ys], label = nombre, linestyle=estilo, marker='x', linewidth=3, markersize = 15, markeredgewidth=3)
    
    ax.set_ylabel("C.C. de Perason con Esperanza de Vida al nacer", fontsize=20)
    ax.set_xlabel("Año", fontsize=20)
    ax.set_title(f"Utilizando encuestas de {nombre_muestra}", fontsize = 28)
    ax.set_xticks(ticks = xticks, labels= xlabel_ticks, rotation=90, fontsize=18)
    # ax.set_xticks(ticks = xticks, labels=[None]*len(xticks))
    ax.set_yticks(ticks = yticks_mayor, minor=False, labels=list(map(lambda x: f"{x:.2f}", yticks_mayor)), fontsize=18)
    ax.set_yticks(ticks = yticks_menor, minor=True)
    ax.grid(c='black', linestyle='--')
    ax.set_facecolor('lightgray')
    ax.legend(fontsize=24)

fig.savefig("../figuras/figura_6_pearson_ingreso_consumo_esp_vida_total.png",bbox_inches='tight')