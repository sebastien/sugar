import sys
from glob import glob
from sugar import main as sugar
for p in glob("*.s*"):
    print sugar.run(["-cljs", "-t",p])
# EOF
