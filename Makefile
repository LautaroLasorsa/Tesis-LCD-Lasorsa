FIGURA1=figura_1_dispersion_plot_completo
FIGURA2=figura_2_violin_plot_completo
FIGURA3=figura_3_mediciones_aproximadas_vs_ideal
FIGURA4=figura_4_mediciones_aproximadas_vs_ideal_varianza
FIGURA5=figura_5_dist_conjuntas_var_y_cgrupos

LISTA_FIGURAS= $(FIGURA1) $(FIGURA2) $(FIGURA3) $(FIGURA4) $(FIGURA5)
FIGURAS= $(addprefix figuras/,$(addsuffix .png,$(LISTA_FIGURAS)))

show:
	echo $($(VARIABLE))

# Regla para generar el PDF de la tesis
tesis.pdf: Tesis/*.tex Tesis/logofcen.pdf Tesis/tesis.bib Tesis/tesis.cls $(FIGURAS)
	cd Tesis && lualatex tesis.tex
	mv Tesis/tesis.pdf tesis.pdf

# Regla para construir todas las figuras
figuras: $(FIGURAS)
figura: figuras/$(FIGURA$(FIGURA)).png

# Regla para limpiar las figuras generadas
clear-figuras:
	rm -f figuras/*.png

# Regla para generar figuras a partir de scripts
figuras/%.png: scripts/%.py scripts/general.py
	@mkdir -p figuras  			 # Asegúrate de que la carpeta 'figuras' exista
	cd scripts && python3 ../$<  # Ejecutar el script correspondiente
