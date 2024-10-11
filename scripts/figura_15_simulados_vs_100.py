from general import *

def Normalizador(data):
    data = np.array(data).T
    for i in range(len(data)):
        data[i] -= data[i,0]
    return data.T

simulados = pd.read_csv("../datos simulados/datos_varianzas.csv", sep='\t')

from scipy.stats import pearsonr, spearmanr

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
Plot(ax, vals,     pearsonr, f"Simulados (Pearson)", col = "blue", linestyle="-")
Plot(ax, vals_norm,pearsonr, f"Simulados estandarizados (Pearson)",col = "orange", linestyle="-")
Plot(ax, vals,     spearmanr, f"Simulados (Spearman)",col = "blue", linestyle="--")
Plot(ax, vals_norm,spearmanr, f"Simulados estandarizados (Spearman)",col = "orange", linestyle="--")
ax.set_xticks(range(len(x)), x, fontsize=19)
yticks = np.linspace(0.99,1,11)
ax.set_yticks( yticks,
        list(map(lambda x : f"{x:.3f}",yticks)),
        fontsize=19, minor = False)
#ax.set_yticks(np.linspace(0,1,21), minor=True)
ax.legend(fontsize=24)
ax.set_xlabel("Número de Grupos", fontsize=24)
ax.grid(linewidth=4, which="major")
ax.grid(linewidth=2, which="minor")


ax.set_ylabel("Correlación vs 100 grupos", fontsize=24)
fig.suptitle("Correlación vs tomar 100 grupos", fontsize=48)

SaveFig(fig)
