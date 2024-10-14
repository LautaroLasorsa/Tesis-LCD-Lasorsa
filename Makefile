include Figuras.mk
SCRIPTS := $(wildcard scripts/figura*.py)
LISTA_FIGURAS= $(patsubst %.py, %, $(notdir $(SCRIPTS)))
FIGURAS= $(addprefix figuras/,$(addsuffix .png,$(LISTA_FIGURAS)))

show:
	echo $($(VARIABLE))

todo: tesis.pdf presentacion_parcial.pdf


indice_comentado.pdf: indice\ comentado/*.tex
	- cd "indice comentado" && lualatex indice_comentado.tex
	mv "indice comentado"/indice_comentado.pdf indice_comentado.pdf

presentacion_parcial.pdf: presentacion_parcial/*.tex $(FIGURAS) 
	- cd presentacion_parcial && lualatex presentacion_parcial.tex
	mv presentacion_parcial/presentacion_parcial.pdf presentacion_parcial.pdf 

# Regla para generar el PDF de la tesis
tesis.pdf: Tesis/*.tex Tesis/logofcen.pdf Tesis/tesis.bib Tesis/tesis.cls $(FIGURAS)
	- cd Tesis && lualatex tesis.tex
	mv Tesis/tesis.pdf tesis.pdf

# Regla para construir todas las figuras
figuras: $(FIGURAS)
figura: figuras/$(FIGURA$(FIGURA)).png

# Regla para limpiar las figuras generadas
clear-figuras:
	rm -f figuras/*.png

commit:
	python3 clear.py
	git add .
	git commit -m "$(MENSAJE)"
	git push

# Regla para generar figuras a partir de scripts
figuras/%.png: scripts/%.py scripts/general.py
	@mkdir -p figuras  			 # Asegúrate de que la carpeta 'figuras' exista
	cd scripts && python3 ../$<  # Ejecutar el script correspondiente
