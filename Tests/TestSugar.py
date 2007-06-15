import sys
from glob import glob
from sugar import sugar
for p in glob("*.s*"):
    print sugar.run(["-t",p])
