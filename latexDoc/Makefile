TITLE = machineLearning

SRCS = $(TITLE).tex \
	$(TITLE).bib

all: 
	pdflatex $(TITLE); 
	bibtex $(TITLE);
	pdflatex $(TITLE);
	pdflatex $(TITLE);

clean:
	-rm -f $(TITLE).dvi $(TITLE).ps $(TITLE).aux $(TITLE).bbl 
	-rm -f $(TITLE).blg $(TITLE).log $(TITLE).pdf $(TITLE).lof $(TITLE).toc $(TITLE).lot