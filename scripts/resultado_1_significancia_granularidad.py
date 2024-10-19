from general import * 
from scipy.stats import spearmanr, pearsonr, kendalltau

datos = pd.read_csv('../datos simulados/datos.csv')

x = list(reversed([1000000//int(x) for x in datos.columns][1:]))
y = list(zip(*datos.iloc))

y_pearson = list(reversed([pearsonr(y[i],y[0]).correlation for i in range(1,len(y))]))
y_spearman = list(reversed([spearmanr(y[i],y[0]).correlation for i in range(1,len(y))]))
y_kendall =  list(reversed([kendalltau(y[i],y[0]).correlation for i in range(1,len(y))]))

(p_ro, p_p) = spearmanr(x, y_pearson)
(s_ro, s_p) = spearmanr(x, y_spearman)
(k_ro, k_p) = spearmanr(x, y_kendall)

print(f"""
\\begin{{tabular}}{{|c|c|c|}}
\\hline
Metrica & Correlación & p-valor \\\\ 
\\hline
Pearson    & {p_ro}   & {p_p:f}   \\\\ 
Spearman   & {s_ro}   & {s_p:f}   \\\\ 
Kendall    & {k_ro}   & {k_p:f}   \\\\ 
\\hline
\\end{{tabular}}
""")