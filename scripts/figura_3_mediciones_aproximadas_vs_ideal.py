from general import * 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, kendalltau

datos = pd.read_csv('../datos simulados/datos.csv')
columnas = [str(1000000//int(x)) for x in datos.columns]
y = list(zip(*datos.iloc))

plt.figure(figsize = (20,7.8))
plt.plot(list(reversed(columnas[1:])),
         list(reversed([np.corrcoef(y[i],y[0])[0,1] for i in range(1,len(y))])), marker='o', label = "Pearson")

plt.plot(list(reversed(columnas[1:])),
         list(reversed([spearmanr(y[i],y[0]).correlation for i in range(1,len(y))])), marker='X', linestyle=(0,(3,3)), label = "Spearman")

plt.plot(list(reversed(columnas[1:])),
         list(reversed([kendalltau(y[i],y[0]).correlation for i in range(1,len(y))])), marker='D', linestyle=(0,(1,1)),label = "Kendall")

plt.grid()
plt.xlabel("Número de grupos", fontsize=14)
plt.ylabel("Correlación lineal con valor idealmente medido", fontsize=14)
plt.title("Midiciones aproxiadas vs Medición ideal", fontsize=24)
plt.xticks(rotation = 90)
plt.legend(fontsize=16)
plt.savefig("../figuras/figura_3_mediciones_aproximadas_vs_ideal.png", bbox_inches='tight', dpi = 400)