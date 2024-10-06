from general import * 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

datos = pd.read_csv('../datos simulados/datos.csv')
columnas = [str(1000000//int(x)) for x in datos.columns]
y = list(zip(*datos.iloc))

plt.figure(figsize = (20,6))
plt.plot(list(reversed(columnas[1:])),
         list(reversed([np.corrcoef(y[i],y[0])[0,1] for i in range(1,len(y))])), '-o')
plt.grid()
plt.xlabel("Número de grupos", fontsize=12)
plt.ylabel("Correlacion lineal con valor idealmente medido", fontsize=12)
plt.title("Midiciones aproxiadas vs Medición ideal", fontsize=18)
plt.xticks(rotation = 90)
plt.savefig("../figuras/figura_3_mediciones_aproximadas_vs_ideal.png", bbox_inches='tight')