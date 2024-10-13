from general import *
from scipy.stats import spearmanr, pearsonr

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
ingresos = dg.get_group(('income',))
consumo  = dg.get_group(('consumption',))

var_ingresos = GenerarMuestra(ingresos)
var_consumo = GenerarMuestra(consumo)

def Normalizador(data):
    data = np.array(data).T
    for i in range(len(data)):
        data[i] -= data[i,0]
    return data.T

simulados = pd.read_csv("../datos simulados/datos_varianzas.csv", sep='\t')

fig, ax = plt.subplots(1,1, figsize=(30,10))

x = list(filter(lambda x : 100%x==0, range(1,101)))
x = list(map(str, x))
def Plot(ax, y, corr, label, col, linestyle):
    xs = list(range(len(x)))
    ys = [corr(yi,y[-len(x)]).correlation for yi in y[-len(x):]]
    ax.plot(xs,list(reversed(ys)), label = label, linewidth=5, c = col, linestyle=linestyle)

sg = simulados.groupby(['-1'])

vals = simulados.to_numpy().T[1:]
# vals = sg.get_group((9,)).to_numpy().T[1:] #simulados.to_numpy().T[1:]
vals_norm = Normalizador(vals)

series = (
    (vals, "Simulados"),
    (vals_norm, "Simulados estandarizados"),
    (var_ingresos, "Ingresos"),
    (var_consumo, "Consumo")
)

colores = ["blue","orange","red","green"]

for serie, col in zip(series,colores):
    Plot(ax, serie[0], pearsonr, f"{serie[1]} (Pearson)", col, '-')
    Plot(ax, serie[0], spearmanr, f"{serie[1]} (Spearman)", col, '--')

ax.set_xticks(range(len(x)), x, fontsize=19)
yticks = np.linspace(0.99,1,11)
ax.set_yticks( yticks,
        list(map(lambda x : f"{x:.3f}",yticks)),
        fontsize=19, minor = False)
#ax.set_yticks(np.linspace(0,1,21), minor=True)
ax.legend(fontsize=24, loc=(-0.005,-0.25), ncols=4)
ax.set_xlabel("Número de Grupos", fontsize=24)
ax.grid(linewidth=4, which="major")
ax.grid(linewidth=2, which="minor")


ax.set_ylabel("Correlación vs 100 grupos", fontsize=24)
fig.suptitle("Correlación vs tomar 100 grupos", fontsize=48)

SaveFig(fig)
