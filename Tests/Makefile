# Sugar test makefile (02-Oct-2007)
TEST_DIR=tests
SOURCE_SG=$(filter-out bug-%,$(filter-out todo-%,$(wildcard *.sg)))
PRODUCT_JS=$(SOURCE_SG:%.sg=$(TEST_DIR)/js/%.js)
PRODUCT_AS=$(SOURCE_SG:%.sg=$(TEST_DIR)/as/%.as)
PRODUCT_PY=$(SOURCE_SG:%.sg=$(TEST_DIR)/py/%.py)
PRODUCT_PNUTS=$(SOURCE_SG:%.sg=$(TEST_DIR)/pnuts/%.pnuts)
SUGAR=sugar

.PHONY: all clean

all: $(PRODUCT_JS) $(PRODUCT_AS) $(PRODUCT_PY) $(PRODUCT_PNUTS)

clean:
	rm -rf $(TEST_DIR)

$(TEST_DIR)/js/%.js: %.sg $(TEST_DIR)/js
	$(SUGAR) -cljavascript $< > $@

$(TEST_DIR)/as/%.as: %.sg $(TEST_DIR)/as
	$(SUGAR) -clactionscript $< > $@

$(TEST_DIR)/py/%.py: %.sg $(TEST_DIR)/py
	$(SUGAR) -clpython $< > $@

$(TEST_DIR)/pnuts/%.pnuts: %.pnuts $(TEST_DIR)/pnuts
	$(SUGAR) -clpnuts $< > $@

$(TEST_DIR)/pnuts:
	mkdir -p $@

$(TEST_DIR)/js:
	mkdir -p $@

$(TEST_DIR)/as:
	mkdir -p $@

$(TEST_DIR)/py:
	mkdir -p $@

# EOF
