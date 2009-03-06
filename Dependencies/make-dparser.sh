#!/bin/bash
# NOTE: This script must be run from the Sugar/Dependencies directory
DPARSER=d-1.15-patched
if [ $PYTHONPATH ]; then
	PPATH=$PYTHONPATH
else
	PPATH=`python -c "import sys;print ':'.join(filter(lambda x:x and x.find('.egg') == -1,sys.path))"`
fi

mkdir dparser
pushd $DPARSER
	make
	cd python
	python setup.py build
	cp `find build -name "dparser.py"` ../../dparser
	cp `find build -name "dparser_swigc.so"` ../../dparser
popd
# FIXME: In some cases, there is no PYTHONPATH
echo ===========================================================
echo NOTE: Please copy '../../dparser/*' to one of this location
echo ===========================================================
echo $PPATH | sed 's|:|\n|g' | sort
echo ===========================================================
echo For example:
echo $ cp 'dparser/*' `echo $PPATH|cut -d':' -f1`
echo ===========================================================
# EOF
