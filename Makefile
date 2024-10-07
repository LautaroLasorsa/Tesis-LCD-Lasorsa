include Figuras.mk
SCRIPTS := $(wildcard scripts/figura*.py)
LISTA_FIGURAS= $(patsubst %.py, %, $(notdir $(SCRIPTS)))
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
