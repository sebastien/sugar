# This is a stub module that will compile the Sugar code into python and
# populate this module with it. It is a good example of how to write a Python
# module in Sugar 
import os, stat
import sugar.sugar as sugar
if not os.path.exists("_docommand.py") \
or os.stat("docommand.spy")[stat.ST_MTIME] > os.stat("_docommand.py")[stat.ST_MTIME]:
	f = file("_docommand.py","w")
	f.write(sugar.runAsString(["-clpy", "docommand.spy"]))
	f.close()
from _docommand import *
if __name__ == "__main__":
	import sys
	sys.exit(_docommand.__main__(sys.argv))
# TEMPLATE -----------------------------------------------------
# os.system("sugar -clpy ${SUGAR_SOURCE} > _{PYTHON_MODULE}.py")
# from _${PYTHON_MODULE} import *
# --------------------------------------------------------------
