from general import *
import numpy as np
import pandas as pd
datos = pd.read_csv('../datos reales/percentiles_ingresos_PPA_2011.csv')
datos = datos[datos['reporting_level'] == 'national']
datos_in = datos[datos['welfare_type']=='income']
datos_co = datos[datos['welfare_type']=='consumption']
plt.figure(figsize=(30,10))
years = datos['year'].unique()
dg = datos_co.groupby(['year'])
years = list(sorted(years))
plt.axhline(y=20, c = 'black', linewidth=4, linestyle='--',zorder=10)
plt.bar(np.array(years)-0.15, [sum(datos_in['year']==year)//100 for year in years], color='lightblue', width= 0.3, label="Ingresos", zorder=11)
plt.bar(np.array(years)+0.15, [sum(datos_co['year']==year)//100 for year in years], color='orange'   , width= 0.3, label="Consumo", zorder=11)
plt.xticks(years, years, rotation=90, fontsize=16)
plt.legend(fontsize=32, loc='upper left')
plt.yticks(list(range(0,70,10)),fontsize=18, minor=False)
plt.yticks(list(range(0,65,5)),fontsize=18, minor=True)
plt.title("Disponibilidad de datos a lo largo del tiempo según tipo de encuesta", fontsize=42)
plt.ylabel("Países sobre los cuales hay datos", fontsize=20)
plt.xlabel("Año",fontsize=20)
plt.grid(linewidth=2, which='major', zorder=-4)
plt.grid(linewidth=1.5, linestyle='--',which='minor', zorder=-5)
plt.xlim(1962,2024)

plt.savefig("../figuras/figura_10_disponibilidad_datos.png",bbox_inches='tight')
