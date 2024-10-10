from general import * 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

datos_varianzas = pd.read_csv("../datos simulados/datos_varianzas.csv", sep='\t')
interes = [x  for x in range(5000,1_000_001) if 1000000%x==0]

def Test(datos_varianza, varianza):
    datos_loc = datos_varianza[datos_varianza['-1']==varianza]
    return [np.corrcoef(datos_loc['1'], datos_loc[str(tamGrupo)])[0][1] for tamGrupo in interes]

observaciones = list(zip(*[Test(datos_varianzas, var) for var in datos_varianzas['-1'].unique()]))
plt.figure(figsize = (30,10))
plt.plot(range(len(observaciones),0,-1),list(observaciones), '-o')
plt.xlabel("Número de grupos", fontsize=18)
plt.ylabel("Correlacion lineal con valor idealmente medido", fontsize=18)
plt.title("Mediciones aproximadas vs ideales con distintas varianzas",fontsize=30)
plt.xticks(range(len(observaciones),0,-1), labels=[1000000//x for x in interes], rotation = 90, fontsize=12)
plt.yticks(list(np.linspace(0,1,21)), minor=True)
plt.yticks(list(np.linspace(0,1,11)))
plt.legend(datos_varianzas['-1'].unique(), title = "$\sigma^2$", fontsize=18)
plt.grid(True,which="major",c="black", linewidth=1)
plt.grid(True,which="minor", linestyle="--")
# plt.show()
plt.savefig("../figuras/figura_4_mediciones_aproximadas_vs_ideal_varianza.png", bbox_inches='tight')

