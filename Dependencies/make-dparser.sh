#!/bin/bash
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
echo ===========================================================
echo NOTE: Please copy '../../dparser/*' to one of this location
echo ===========================================================
echo $PYTHONPATH | sed 's|:|\n|g' | sort
echo ===========================================================
echo For example:
echo $ cp '../../dparser/*' `echo $PYTHONPATH|cut -d':' -f1`
echo ===========================================================
# EOF
