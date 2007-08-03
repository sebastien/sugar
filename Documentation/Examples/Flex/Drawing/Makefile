SUGAR=sugar
SUGAR_FLAGS="-cRlas"
FLEX=mxmlc
FLEX_FLAGS= --show-actionscript-warnings=false
BUILD=.build
PROGRAM=drawing
PROGRAM_SWF=$(PROGRAM).swf
PROGRAM_MXML=$(PROGRAM).mxml
FLASHPLAYER=open

SOURCES=$(wildcard *.sas)

.PHONY: all clean

all: $(PROGRAM_SWF)

run:
	$(FLASHPLAYER) $(PROGRAM_SWF)
	
clean:
	rm -rf $(BUILD) $(PROGRAM_SWF)
	
$(BUILD):
	mkdir $(BUILD)

$(PROGRAM_SWF): $(PROGRAM_MXML) $(SOURCES) $(BUILD)
	$(SUGAR) -cRlas $(SUGAR_FLAGS) -o$(BUILD) $(SOURCES)
	cp $(PROGRAM_MXML) $(BUILD)
	cd $(BUILD) && $(FLEX) $(FLEX_FLAGS) $<
	cp $(BUILD)/$(PROGRAM_SWF) .

# EOF
