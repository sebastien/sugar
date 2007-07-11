#!/bin/sh
# NOTE: This script must be run from the Sugar/Dependencies directory
DPARSER=d-1.15-patched
mkdir dparser
pushd $DPARSER
	make
	cd python
	python setup.py build
	cp `find build -name "dparser.py"` ../../dparser
	cp `find build -name "dparser_swigc.so"` ../../dparser
popd
# EOF
