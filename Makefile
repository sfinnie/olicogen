INPUT=input
INTERMEDIATE=intermediate
OUTPUT=output

.PHONY: all
all: $(patsubst $(INPUT)/%.tex,$(OUTPUT)/%.pdf,$(wildcard $(INPUT)/*.tex))

$(OUTPUT)/%.pdf: $(INPUT)/%.tex
	pdflatex -quiet -aux-directory=$(INTERMEDIATE) -output-directory=$(OUTPUT) $<

.PHONY: clean
clean:
	rm -rf $(OUTPUT)/*.* $(INTERMEDIATE)/*.*


