#!/bin/env python
import os, sys, re

__doc__ = """\
Cleans the given Sugar source files by :

- Converting empty lines that only contains spaces to empty lines
- Gettin rid of trailing spaces
"""

RE_EMPTY_LINE     = re.compile("s+")

def clean_sugar_text( text ):
	res = []
	for line in text.split("\n"):
		if not line or RE_EMPTY_LINE.match(line):
			res.append("")
		else:
			while line and line[-1] in "\t ":
				line = line[:-1]
			res.append(line)
	res = "\n".join(res)
	if res:return res[:-1]
	else: return res

	text = RE_EMPTY_LINES.sub(text,"")
	return RE_TRAILING_SPACES.sub(text,"")

if __name__ == "__main__":
	for a in sys.argv[1:]:
		print "Cleaning", a
		text = open(a,'r').read()
		open(a,'w').write(clean_sugar_text(text))
# EOF
