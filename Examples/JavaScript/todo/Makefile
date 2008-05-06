SUGAR=sugar
PAMELA=pamela
SOURCES_PAML =$(wildcard *.paml)
SOURCES_SJS  =$(wildcard *.sjs)
PRODUCT_PAML =$(SOURCES_PAML:%.paml=%.html)
PRODUCT_SJS  =$(SOURCES_SJS:%.sjs=%.js)

all: $(PRODUCT_SJS) $(PRODUCT_PAML)
	echo Created: $(PRODUCT_PAML) $(PRODUCT_SJS)

%.js: %.sjs
	$(SUGAR) -cljavascript $< > $@

%.html: %.paml
	$(PAMELA) $< > $@
