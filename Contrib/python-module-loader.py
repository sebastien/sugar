# This is a stub module that will compile the Sugar code into python and
# populate this module with it. It is a good example of how to write a Python
# module in Sugar 
#
# To use it, simply replace MODULE by the name of your module, which must have
# the same name as your python module, except with the 'spy' extension:
#
# mymodule.py              (this file with MODULE=mymodule)
# mymodule.spy             (the Sugar file)
#
# Now, when importing 'mymodule' from Python, 'mymodule.spy' will be compiled to
# the '_mymodule.py' module, which will then be loaded by the 'mymodule.py'
# module.
import os, stat
import sugar.sugar as sugar
if not os.path.exists("_MODULE.py") \
or os.stat("MODULE.spy")[stat.ST_MTIME] > os.stat("_MODULE.py")[stat.ST_MTIME]:
	f = file("_MODULE.py","w")
	f.write(sugar.runAsString(["-clpy", "MODULE.spy"]))
	f.close()
from _MODULE import *
if __name__ == "__main__":
	import sys
	sys.exit(_MODULE.__main__(sys.argv))
# EOF
