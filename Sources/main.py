#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   SweetC                       <http://www.ivy.fr/sweetc>
# Author            :   Sébastien Pierre                     <sebastien@ivy.fr>
# License           :   BSD License (revised)
# -----------------------------------------------------------------------------
# Creation date     :   02-Aug-2005
# -----------------------------------------------------------------------------

import os, sys, shutil
import grammar

__version__ = "0.3.8"

DESCRIPTION = """\
SweetC v.%s

SweetC is an interpreter and a compiler for an object-oriented superset of
the C language.
 
Type 'sweetc --help' for more information.
""" % (__version__)

# ------------------------------------------------------------------------------
#
# Run method
#
# ------------------------------------------------------------------------------

def run( args ):
	"""The run method can be used to execute a SweetC command from another
	Python script without having to spawn a shell."""
	
	# If no argument is given, we simply print the description
	if len(args) == 0:
		print DESCRIPTION
		return
	# Otherwise, we are in interpreter mode
	sources     = [ args[0] ]
	parser      = grammar.Parser(verbose=False)
	source, module = parser.parse(sources[0])
	from lambdafactory.modelwriter import Writer as Writer
	w = Writer()
	print w.write(module)

# ------------------------------------------------------------------------------
#
# Main
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	run(sys.argv[1:])

# EOF
