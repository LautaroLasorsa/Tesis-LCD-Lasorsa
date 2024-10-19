include Figuras.mk
SCRIPTS_FIGURAS := $(wildcard scripts/figura*.py)
LISTA_FIGURAS= $(patsubst %.py, %, $(notdir $(SCRIPTS_FIGURAS)))
FIGURAS= $(addprefix figuras/,$(addsuffix .png,$(LISTA_FIGURAS)))

SCRIPTS_RESULTADOS := $(wildcard scripts/resultado*.py)
LISTA_RESULTADOS=$(patsubst %.py, %, $(notdir $(SCRIPTS_RESULTADOS)))
RESULTADOS= $(addprefix resultados/,$(addsuffix .tex,$(LISTA_RESULTADOS)))
 
show:
	echo $($(VARIABLE))

todo: tesis.pdf presentacion_parcial.pdf indice_comentado.pdf


indice_comentado.pdf: indice\ comentado/*.tex
	- cd "indice comentado" && lualatex indice_comentado.tex
	mv "indice comentado"/indice_comentado.pdf indice_comentado.pdf

presentacion_parcial.pdf: presentacion_parcial/*.tex $(FIGURAS) 
	- cd presentacion_parcial && lualatex presentacion_parcial.tex
	mv presentacion_parcial/presentacion_parcial.pdf presentacion_parcial.pdf 

tesis.pdf: Tesis/*.tex Tesis/logofcen.pdf Tesis/tesis.bib Tesis/tesis.cls $(FIGURAS) $(RESULTADOS)
	- rm Tesis/tesis.bbl Tesis/tesis.blg Tesis/tesis.aux Tesis/tesis.log Tesis/tesis.thm Tesis/tesis.toc
	- cd Tesis && lualatex tesis.tex
#	- cd Tesis && lualatex tesis.tex
	- cd Tesis && bibtex tesis.aux 
	- cd Tesis && lualatex tesis.tex 
	- cd Tesis && lualatex tesis.tex
	mv Tesis/tesis.pdf tesis.pdf
	
resultados: $(RESULTADOS)

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
figuras/figura_%.png: scripts/figura_%.py scripts/general.py
	@mkdir -p figuras  			 # Asegúrate de que la carpeta 'figuras' exista
	cd scripts && python3 ../$<  # Ejecutar el script correspondiente

resultados/resultado_%.tex: scripts/resultado_%.py scripts/general.py
	@mkdir -p resultados              # Asegúrate de que la carpeta 'resultados' exista
	cd scripts && python3 resultado_$*.py > ../resultados/resultado_$*.tex
